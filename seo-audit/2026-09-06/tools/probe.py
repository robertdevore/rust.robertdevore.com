import csv,json,sys,urllib.request,urllib.error,concurrent.futures,datetime
from pathlib import Path
root=Path(__file__).resolve().parents[1];phase=sys.argv[1];origin='https://rust.robertdevore.com';receipts=[]
def request(pair):
 url,ua=pair;chain=[]
 class Handler(urllib.request.HTTPRedirectHandler):
  def redirect_request(self,req,fp,code,msg,headers,newurl):chain.append({'source':req.full_url,'status':code,'target':newurl});return super().redirect_request(req,fp,code,msg,headers,newurl)
 try:
  with urllib.request.build_opener(Handler).open(urllib.request.Request(url,headers={'User-Agent':ua}),timeout=15) as r:return {'url':url,'ua':ua,'status':r.status,'final_url':r.url,'chain':chain,'headers':dict(r.headers),'sample':r.read(120).decode('utf8',errors='replace')}
 except urllib.error.HTTPError as e:return {'url':url,'ua':ua,'status':e.code,'chain':chain,'final_url':e.url,'headers':dict(e.headers)}
 except Exception as e:return {'url':url,'ua':ua,'status':0,'chain':chain,'final_url':url,'error':str(e)}
uas=['Googlebot','bingbot','OAI-SearchBot','ChatGPT-User','GPTBot','Claude-SearchBot','Claude-User','ClaudeBot','PerplexityBot']
paths=['/robots.txt','/sitemap.xml','/','/course/03-ownership/'];pairs=[(origin+p,ua) for ua in uas for p in paths]
variants=[origin+'/', 'http://rust.robertdevore.com/', origin+'/course/03-ownership',origin+'/course/03-ownership?ref=audit',origin+'/course/03-ownership/?ref=audit',origin+'/index.html',origin+'/course/03-ownership/index.html',origin+'/not-a-real-page/', 'https://www.rust.robertdevore.com/','http://www.rust.robertdevore.com/']
pairs.extend((u,'RustCourseAudit/1.0') for u in variants)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:receipts=list(pool.map(request,pairs))
(root/'raw'/f'{phase}-edge.json').write_text(json.dumps(receipts,indent=2))
with (root/f'{phase}-crawler-access.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['phase','url','user_agent','http_status','robots_policy','verification','limitations']);w.writeheader()
 for r in receipts[:len(uas)*len(paths)]:w.writerow(dict(phase=phase,url=r['url'],user_agent=r['ua'],http_status=r['status'],robots_policy='existing wildcard Allow: /; unchanged',verification='accessible' if r['status']==200 else 'indeterminate',limitations='Spoofed UA from audit host; does not prove verified-bot IP access or actual crawl/indexing.'))
with (root/f'{phase}-redirects.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['phase','source_url','source_variant','http_status','target_url','chain_length','final_status','canonical_target','query_preserved','verification','issues']);w.writeheader()
 for r in receipts[len(uas)*len(paths):]:w.writerow(dict(phase=phase,source_url=r['url'],source_variant=r['url'],http_status=r['chain'][0]['status'] if r['chain'] else r['status'],target_url=r['final_url'],chain_length=len(r['chain']),final_status=r['status'],canonical_target=r['final_url'].split('?')[0],query_preserved='ref=audit' in r['final_url'] if 'ref=audit' in r['url'] else 'n/a',verification='observed' if r['status'] else 'DNS/TLS/network unavailable',issues=r.get('error','')))
print(json.dumps([{'url':r['url'],'status':r['status'],'chain':r['chain']} for r in receipts if r['ua']=='RustCourseAudit/1.0' or r['status']!=200],indent=2))
