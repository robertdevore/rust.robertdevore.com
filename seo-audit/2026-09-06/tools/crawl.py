import csv,json,hashlib,re,sys,urllib.request,urllib.error,urllib.parse,collections,concurrent.futures,datetime,gzip
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]; ORIGIN='https://rust.robertdevore.com';phase=sys.argv[1];site=Path(sys.argv[2] if len(sys.argv)>2 else 'dist');raw=ROOT/'raw'/phase;raw.mkdir(exist_ok=True)
def save(name,rows,fields=None):
 p=ROOT/name
 if not fields: fields=list(rows[0]) if rows else list(csv.DictReader(p.open()).fieldnames or []) if p.exists() else ['status']
 with p.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
def fetch(url,ua='RustCourseAudit/1.0'):
 chain=[]
 class Handler(urllib.request.HTTPRedirectHandler):
  def redirect_request(self,req,fp,code,msg,headers,newurl):chain.append({'url':req.full_url,'status':code,'location':newurl});return super().redirect_request(req,fp,code,msg,headers,newurl)
 try:
  with urllib.request.build_opener(Handler).open(urllib.request.Request(url,headers={'User-Agent':ua}),timeout=20) as r: body=r.read();return {'url':url,'status':r.status,'final_url':r.url,'headers':dict(r.headers),'chain':chain,'body':body.decode('utf8',errors='replace'),'bytes':len(body)}
 except urllib.error.HTTPError as e:return {'url':url,'status':e.code,'final_url':e.url,'headers':dict(e.headers),'chain':chain,'body':e.read().decode('utf8',errors='replace')}
 except Exception as e:return {'url':url,'status':0,'final_url':url,'headers':{},'chain':chain,'body':'','error':str(e)}
def typ(url):return 'lesson' if re.search('/course/\d',url) else 'course' if url.endswith('/course/') else 'home' if url==ORIGIN+'/' else 'about' if url.endswith('/about/') else 'practice'
sitemap=BeautifulSoup((site/'sitemap.xml').read_text(),'xml');urls=[x.text for x in sitemap.find_all('loc')];pages={};internal=[];external=[];images=[];rows=[]
for url in urls:
 rel=url.removeprefix(ORIGIN).lstrip('/');p=site/rel/'index.html';s=BeautifulSoup(p.read_text(),'html.parser');pages[url]=s
 for a in s.find_all('a',href=True):
  dest=urllib.parse.urljoin(url,a['href']);entry={'phase':phase,'source_url':url,'destination_url':dest,'anchor_text':a.get_text(' ',strip=True),'link_context':a.parent.name,'http_status':'','final_url':'','chain_length':0,'verification':'','rel':' '.join(a.get('rel',[])),'recommended_action':''}
  (internal if urllib.parse.urlparse(dest).netloc==urllib.parse.urlparse(ORIGIN).netloc else external).append(entry)
 for im in s.find_all('img'):
  images.append({'phase':phase,'url':url,'src':im.get('src'),'alt':im.get('alt'),'width':im.get('width'),'height':im.get('height'),'loading':im.get('loading','eager')})
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: live=dict(zip(urls,pool.map(fetch,urls)))
with gzip.open(raw/'production-pages.json.gz','wt') as f:json.dump(live,f)
externalurls=sorted(set(x['destination_url'].split('#')[0] for x in external if x['destination_url'].startswith('http')))
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: ext=dict(zip(externalurls,pool.map(fetch,externalurls)))
(raw/'external-receipts.json').write_text(json.dumps({k:{x:y for x,y in v.items() if x!='body'} for k,v in ext.items()},indent=2))
for x in internal:
 u=urllib.parse.urlparse(x['destination_url']);base=urllib.parse.urlunparse(u._replace(fragment='',query=''));path=site/u.path.lstrip('/');path=path/'index.html' if u.path.endswith('/') else path
 x['http_status']=200 if path.is_file() else 404;x['final_url']=base;x['verification']='valid' if path.is_file() else 'missing'
 if u.fragment and base in pages and not pages[base].find(id=urllib.parse.unquote(u.fragment)):x['verification']='missing fragment'
for x in external:
 r=ext.get(x['destination_url'].split('#')[0],{});x.update(http_status=r.get('status','not HTTP'),final_url=r.get('final_url',''),chain_length=len(r.get('chain',[])),verification='valid' if r.get('status')==200 else 'broken' if r.get('status') in [404,410] else 'indeterminate')
graph={u:set(x['destination_url'].split('#')[0].split('?')[0] for x in internal if x['source_url']==u) for u in urls};depth={ORIGIN+'/':0};q=collections.deque(depth)
while q:
 u=q.popleft()
 for v in graph.get(u,[]):
  if v in pages and v not in depth:depth[v]=depth[u]+1;q.append(v)
for url,s in pages.items():
 def meta(name):
  x=s.find('meta',attrs={'name':name}) or s.find('meta',attrs={'property':name});return x.get('content','') if x else ''
 canonical=s.find('link',rel='canonical');canonical=canonical.get('href','') if canonical else '';main=s.find('article') or s.find('main');text=main.get_text(' ',strip=True);types=[];errors=[]
 for block in s.find_all('script',type='application/ld+json'):
  try:
   j=json.loads(block.string or block.get_text());items=j.get('@graph',[j]);types.extend(t for x in items for t in ([x.get('@type')] if isinstance(x.get('@type'),str) else x.get('@type',[])))
  except Exception as e:errors.append(str(e))
 title=s.title.get_text() if s.title else '';desc=meta('description');r=live[url];links=[x for x in internal if x['source_url']==url];outs=[x for x in external if x['source_url']==url]
 rows.append(dict(phase=phase,url=url,source_file='content/lessons/'+url.rstrip('/').split('/')[-1]+'.md' if typ(url)=='lesson' else 'content/about.md' if typ(url)=='about' else 'scripts/build.mjs',page_type=typ(url),local_status=200,production_status=r['status'],indexable='noindex' not in meta('robots') and r['status']==200,robots_directives=meta('robots'),canonical=canonical,canonical_target_status=live.get(canonical,{}).get('status',0),title=title,title_length=len(title),meta_description=desc,description_length=len(desc),h1=' | '.join(h.get_text(' ',strip=True) for h in s.find_all('h1')),heading_structure=' | '.join(h.name+':'+h.get_text(' ',strip=True) for h in main.find_all(re.compile('^h[1-6]$'))),word_count=len(text.split()),lang=s.html.get('lang',''),published_date=meta('article:published_time'),modified_date=meta('article:modified_time'),author=meta('author'),breadcrumbs=bool(s.select('.breadcrumbs')),schema_types='|'.join(types),internal_inbound_links=sum(1 for x in internal if x['destination_url'].split('#')[0]==url),internal_outbound_links=len(links),external_outbound_links=len(outs),broken_internal_links=sum(x['verification']!='valid' for x in links),broken_external_links=sum(x['verification']=='broken' for x in outs),image_count=len(s.find_all('img')),missing_alt=sum(not x.has_attr('alt') for x in s.find_all('img')),missing_dimensions=sum(not x.has_attr('width') or not x.has_attr('height') for x in s.find_all('img')),page_depth=depth.get(url,''),orphan=url not in depth,sitemap_included=True,duplicate_title=False,duplicate_description=False,content_hash=hashlib.sha256(text.encode()).hexdigest(),issues='|'.join(errors),html_bytes=len(str(s).encode())))
for r in rows:
 r['duplicate_title']=sum(x['title']==r['title'] for x in rows)>1;r['duplicate_description']=sum(x['meta_description']==r['meta_description'] for x in rows)>1
save(phase+'.csv',rows);save('site-inventory.csv',rows);save('internal-links.csv',internal);save('external-links.csv',external);save('broken-links.csv',[x for x in internal+external if x['verification'] in ['broken','missing','missing fragment']],list(internal[0]));save('image-audit.csv',images,['phase','url','src','alt','width','height','loading'])
for name,keys in [('metadata-audit.csv',['phase','url','title','meta_description','h1','lang','author','duplicate_title','duplicate_description']),('indexability.csv',['phase','url','indexable','canonical','canonical_target_status','robots_directives','sitemap_included']),('schema-audit.csv',['phase','url','schema_types','issues']),('crawlability.csv',['phase','url','local_status','production_status','page_depth','orphan'])]:save(name,rows,keys)
summary={'phase':phase,'canonical_pages':len(rows),'indexable_pages':sum(r['indexable'] for r in rows),'missing_titles':sum(not r['title'] for r in rows),'missing_descriptions':sum(not r['meta_description'] for r in rows),'duplicate_titles':sum(r['duplicate_title'] for r in rows),'duplicate_descriptions':sum(r['duplicate_description'] for r in rows),'missing_canonicals':sum(not r['canonical'] for r in rows),'h1_problems':sum(len(pages[u].find_all('h1'))!=1 for u in urls),'broken_internal_links':sum(r['broken_internal_links'] for r in rows),'broken_external_destinations':len(set(x['destination_url'] for x in external if x['verification']=='broken')),'indeterminate_external_destinations':len(set(x['destination_url'] for x in external if x['verification']=='indeterminate')),'orphans':sum(r['orphan'] for r in rows),'deeper_than_three':sum(isinstance(r['page_depth'],int) and r['page_depth']>3 for r in rows),'schema_pages':sum(bool(r['schema_types']) for r in rows),'schema_parse_errors':sum(bool(r['issues']) for r in rows),'missing_author_metadata':sum(not r['author'] for r in rows),'missing_alt':sum(r['missing_alt'] for r in rows),'missing_dimensions':sum(r['missing_dimensions'] for r in rows),'external_destinations':len(externalurls),'assets_bytes':sum(p.stat().st_size for p in (site/'assets').rglob('*') if p.is_file())}
(ROOT/(phase+'-summary.json')).write_text(json.dumps(summary,indent=2));(raw/'pages.json').write_text(json.dumps(rows,indent=2));print(json.dumps(summary,indent=2))
