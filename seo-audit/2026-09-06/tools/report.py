import csv,json,hashlib,tarfile,datetime
from pathlib import Path
R=Path(__file__).resolve().parents[1];NA='NOT AVAILABLE — DATA ACCESS REQUIRED'
def read(n):return list(csv.DictReader((R/n).open()))
def save(n,rows,fields=None):
 with (R/n).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)
def md(n,s):(R/n).write_text(s.strip()+'\n')
b=json.loads((R/'baseline-summary.json').read_text());a=json.loads((R/'after-summary.json').read_text());pages=read('after.csv')
seal=json.loads((R/'raw/baseline-seal.json').read_text());assert hashlib.sha256((R/'raw/baseline-site.tar.gz').read_bytes()).hexdigest()==seal['archiveSha256']
for kind in ['crawler-access','redirects']:save(kind+'.csv',read('baseline-'+kind+'.csv')+read('after-'+kind+'.csv'))
perf=[]
for phase in ['baseline','after']:
 for template in ['home','lesson']:
  p=R/f'raw/{phase}-{template}-lighthouse.json';j=json.loads(p.read_text());au=j['audits'];res={x['resourceType']:x for x in au['resource-summary']['details']['items']}
  row=dict(phase=phase,url=j['finalDisplayedUrl'],template=template,run_date=j['fetchTime'],environment='Chrome 152; Lighthouse default simulated mobile; one run/template; same host',lighthouse_version=j['lighthouseVersion'])
  for field,typ in [('html','document'),('css','stylesheet'),('js','script'),('image','image'),('font','font')]:row[field+'_bytes']=res.get(typ,{}).get('transferSize',0)
  row.update(requests=res.get('total',{}).get('requestCount',0),lcp_ms=au['largest-contentful-paint']['numericValue'],inp_ms=NA,cls=au['cumulative-layout-shift']['numericValue'],ttfb_ms=au['server-response-time']['numericValue'],tbt_ms=au['total-blocking-time']['numericValue'],performance_score=round(j['categories']['performance']['score']*100),accessibility_score=round(j['categories']['accessibility']['score']*100),best_practices_score=round(j['categories']['best-practices']['score']*100),seo_score=round(j['categories']['seo']['score']*100),source=str(p.relative_to(R)),notes='Lab only; CDN-injected scripts retained; no field CWV or causal ranking inference.')
  perf.append(row)
save('performance.csv',perf)
save('content-audit.csv',[dict(url=p['url'],page_type=p['page_type'],intent='learn and practice '+p['h1'],primary_entity='Rust programming language',author='Robert DeVore',freshness='Rust 1.98.1 / edition 2024 baseline, verified 2026-09-06; no invented publish dates',evidence=p['source_file']+'; docs/research/ledger.md; examples/ and drills/',assessment='Distinct purpose; source-backed exercises and primary references' if p['page_type']=='lesson' else 'Distinct navigational or project explanation purpose',word_count=p['word_count'],answer_structure=p['heading_structure'],gap='No observed blocking content gap; measure actual query and citation demand before expanding',status='reviewed') for p in pages])
save('keyword-map.csv',[dict(url=p['url'],primary_topic=p['h1'],query_intent='instructional' if p['page_type']=='lesson' else 'navigational',suggested_query=p['h1']+' Rust tutorial' if p['page_type']=='lesson' else 'Robert DeVore Rust course',evidence='Editorial mapping from visible subject; not search-volume data',search_volume=NA,cannibalization='No duplicate page purpose observed') for p in pages])
queries=['rust.robertdevore.com','learn Rust ownership borrowing course compiler exercises','Rust move borrow compiler error practice','Rust lifetime exercises','Rust Result error handling course','Rust iterator tutorial exercises','Rust Send Sync thread course','Rust Tokio cancellation exercise','Rust unsafe Miri course','Rust CLI capstone project','Rust edition 2024 course','Robert DeVore Rust course']
save('search-rankings.csv',[dict(query=q,search_engine='Tool web search (underlying engine unspecified)' if i<2 else NA,date='2026-09-06',country=NA,device=NA,page_found='No identifiable domain result in returned sample' if i==0 else NA,observed_position_or_range=NA,competing_results='learningrust.org; rust-exercises.com; Microsoft Learn' if i==1 else NA,rich_features=NA,ai_result_presence=NA,evidence='research-sources.md; tool search observation' if i<2 else NA,limitations='Uncontrolled discovery sample, not reproducible SERP rank; no conclusion about indexing or ranking') for i,q in enumerate(queries)])
save('ai-search-benchmark.csv',[dict(question='Where can I learn '+q+' with runnable Rust exercises?',platform=platform,date='2026-09-06',domain_appeared=NA,domain_cited=NA,cited_url=NA,citation_context=NA,citation_order=NA,competing_domains=NA,accurate_representation=NA,content_gap='Unmeasured; do not infer from content readiness',evidence=NA,limitations='Prepared benchmark question; no controlled answer session executed') for q in ['ownership and borrowing','lifetimes','iterator adapters','error handling','thread safety','async cancellation','Miri and unsafe boundaries','a complete CLI capstone'] for platform in ['ChatGPT Search','Google AI features','Bing Copilot','Perplexity']])
issues=[]
def issue(i,cat,severity,count,evidence,action,status,owner='repository maintainer'):
 issues.append(dict(id=i,phase='baseline→after',category=cat,severity=severity,affected_urls='See category CSV / evidence',affected_count=count,evidence=evidence,expected_benefit=action,confidence='High' if status=='resolved' else 'Medium',difficulty='small' if status=='resolved' else 'owner/platform access',recommended_action=action,owner=owner,status=status))
issue('SEO-01','schema','P2',32,'baseline schema_pages=0; after=32; verify:discovery','Add truthful entity graph and lesson breadcrumbs','resolved')
issue('SEO-02','authorship','P2',32,'author metadata absent on 32 baseline pages; visible About and lesson byline added','Identify actual author without invented credentials','resolved')
issue('SEO-03','redirects','P2',32,'redirects.csv: sampled baseline temporary 307; after permanent 301; all mappings source-tested','Consolidate extension and slash aliases while preserving query strings','resolved')
issue('SEO-04','assets','P2',32,'Minified content-hashed CSS/JS and immutable cache headers; production verification','Reduce application asset transfer and safely cache versioned files','resolved')
issue('AI-01','portable content','P3',28,'verify:discovery; production-verification.json','Provide source-complete Markdown, hashes and JSON index; no ranking guarantee','resolved')
issue('HOWL-01','artifact integrity','P3',2,'showcase/manifest-lock.json; deterministic repeat rendering','Generate source-backed cards with drift verification','resolved')
issue('PERF-01','production performance','P2',2,'performance.csv and raw/*lighthouse.json; Cloudflare challenge JSD dominates baseline CPU','Review CDN script cost with owner using field data; preserve requested tracking','recommendation','Cloudflare zone owner')
issue('DATA-01','visibility measurement','P2',32,NA,'Obtain Search Console, Bing AI Performance, analytics and field CWV exports; compare fixed windows','data access required','site owner')
issue('HOST-01','optional alias','P3',0,'raw/after-edge.json; www.rust.robertdevore.com unavailable','Only configure nested www alias if intended; canonical rust hostname is healthy','recommendation','DNS owner')
issue('EDGE-01','generic HTTP client access','P2',6,'raw/production-schema-cache.json: Python-urllib/3.10 gets 403 for home, JSON, Markdown, full text and both built assets; named audit/browser clients succeed','Review matching Cloudflare Security Event and consider narrowly scoped legitimate-client access; do not disable zone protection or analytics','owner review required','Cloudflare zone owner')
save('issues.csv',issues)
metrics='\n'.join(f'| {k} | {b[k]} | {a[k]} |' for k in b if k!='phase')
pr='\n'.join(f"| {r['phase']} | {r['template']} | {r['performance_score']} | {r['lcp_ms']:.0f} | {r['tbt_ms']:.0f} | {r['cls']} |" for r in perf)
md('before-after.md',f'''# Before and after · 2026-09-06

Same 32 canonical URLs in both inventories; 28 lessons. Baseline commit `{seal['commit']}` is sealed in raw/baseline-site.tar.gz; its SHA-256 and member hashes are in raw/baseline-seal.json. Report generation verifies the archive checksum. Original CSVs are preserved under raw/baseline/.

| Metric | Before | After |
|---|---:|---:|
{metrics}

P0: 0 → 0. P1: 0 → 0. No URL removed. All 32 page templates gain factual metadata/schema and bundled assets; 28 gain bylines, breadcrumbs and Markdown downloads. About/practice gain factual project information and a real source card. No lesson claims or Rust examples rewritten.

| Phase | Template | Performance /100 | LCP ms | TBT ms | CLS |
|---|---|---:|---:|---:|---:|
{pr}

One lab run per template/phase, default mobile simulation. Shared-host timing and CDN injections vary. These values do not demonstrate field CWV improvement, rank growth, or causal impact. Repository asset totals include new downloadable exports/cards and retained source assets; they are not page-load transfer size. See performance.csv for actual transferred resource totals.

Internal scores are deliberately omitted: partial access and heuristic weighting would add apparent precision. Concrete coverage and lab scores above are reproducible. Search ranking and AI citation before/after: {NA}.
''')
md('methodology.md','''# Methodology

Audit executed 2026-09-06 against the repository, generated dist, and the public Cloudflare custom domain. Baseline captured before edits; after inventory uses the identical sitemap URL set. Tools are committed alongside receipts.

Full source HTML crawl: 32 canonical pages (home, curriculum, practice, about, 28 lessons), every anchor and local fragment, unique external HTTP destinations, headings, descriptions, authors, canonicals, schema, graph depth and images. Live HTML/status fetched for each canonical page, with public DNS/TLS/redirect/404 and supplemental Markdown hash verification separately. Metadata/content columns describe generated HTML; live responses are retained independently in compressed JSON. This avoids representing source markup as observed production markup. Browser suite renders all 32 desktop routes and 28 mobile lessons, checks interactions and axe accessibility.

robots, sitemap, home and ownership lesson probed with nine crawler user agents. Spoofed UAs test edge responses from one client, not verified bot IPs, crawl frequency, indexing, or policy guarantees. Existing permissive robots policy and owner-requested analytics are unchanged. Missing nested www hostname is recorded, not treated as a required advertised route.

Lighthouse 13.4.1 / Chrome 152, default mobile simulation, one run per home/lesson before and after; exploratory lab measurements, no field INP claim. Resource summary transfer bytes differ from filesystem totals. Public CDN scripts remain enabled. No rank/citation attribution is inferred from performance.

Structured data is parsed and checked against factual content with semantic relationship assertions; this is not Google Rich Results Test certification. Course Info rich-result display is retired. Breadcrumb markup may be eligible subject to Google requirements; no appearance is guaranteed. Static JSON-LD does not require an execution API. llms.txt and Markdown exports improve portability, not a promised search-engine protocol.

Direct first-party competitors reviewed: learningrust.org ownership lesson and rust-exercises.com/100-exercises. Both emphasize practice; this course already offers executable examples, failing diagnostics and a CLI capstone. Avoid unsupported claims of superiority. Two exploratory web searches provide discovery observations only; controlled search/AI benchmarks require the access described in data-availability.md.

Severity: P0 outage/index removal; P1 widespread broken canonical/crawl/content behavior; P2 meaningful quality or measurement gap; P3 optional enrichment. Resolved means code and public behavior verified. Recommendations requiring platform access are not silently treated as completed.
''')
md('data-availability.md',f'''# Data availability

Available: local source and build, complete canonical sitemap/HTML inventory, public HTTP headers and redirects, DNS/TLS, synthetic crawler probes, local/live browser checks, laboratory Lighthouse, primary-source research, deterministic Howl receipts, two exploratory tool searches.

| Dataset | Status | Needed to measure |
|---|---|---|
| Google Search Console performance/index coverage/AI inclusion | {NA} | Verified property exports, same query/page/date filters |
| Bing Webmaster Tools / AI Performance | {NA} | Verified property citation and grounding-query exports |
| Cloudflare/Google Analytics engagement and conversions | {NA} | Read-only dashboard/export with bot/internal filtering |
| CDN logs, real crawler IPs, 404 distribution | {NA} | Owner export; no inference from spoofed UAs |
| CrUX/RUM field LCP, INP, CLS | {NA} | Sufficient real-user samples and 28-day windows |
| Reproducible country/device SERP positions | {NA} | Authorized rank dataset or controlled manual sample |
| Controlled AI-answer citations | {NA} | Dated prompts, platform/model/mode, response and citation receipts |

Unavailable does not mean unconfigured or zero. Tracking remains enabled. No new account, external submission, IndexNow verification, or automated monitoring was created.
''')
md('changes.md','''# Implemented changes

- scripts/seo.mjs and build.mjs: truthful Person/WebSite/WebPage/Course/LearningResource/BreadcrumbList graphs, author metadata, visible author/breadcrumb context, canonical text exports, JSON index and full text. No fabricated dates/credentials/reviews.
- scripts/build.mjs, package.json/lock: esbuild 0.28.1, minified content-hashed CSS/JS, immutable asset cache headers, explicit permanent URL aliases, canonical/noindex headers for duplicate Markdown.
- howl.json, scripts/howl.mjs, showcase/: Howl 1.1.0 actual-source manifest and deterministic render/hash verification. scripts/social.mjs and assets/social.png derive the social card from Howl. Practice card has alt text, dimensions and lazy loading.
- content/about.md and assets/site.css: factual author/export explanations and compact lesson source row. Inter body, Departure Mono headings/code, SiteKit licensing, themed scrollbars and symbol-free header preserved.
- scripts/test-discovery.mjs, scripts/verify-production.mjs, CI, README and AGENTS.md: source/diagnostic completeness and hashes, schema relationships, production Markdown headers, drift gates, maintainer contracts.

No DNS/WAF/training crawler/analytics changes. No Rust curriculum rewrite. Howl does not compile Rust: its source remains covered by the Rust workspace verification.
''')
md('unresolved.md',f'''# Unresolved recommendations

No P0/P1 defect observed in the tested scope. No deployment blocker.

EDGE-01: default Python-urllib/3.10 receives 403 for the homepage, course-index.json, a lesson Markdown export, llms-full.txt and both bundled assets. Browser, Node fetch and named audit/crawler clients pass. This limits generic agent retrieval despite permissive robots. Exact rule/product cause is unknown without Cloudflare Security Events. Owner should review a narrowly scoped access policy; no broad security disablement is proposed. Evidence: raw/production-schema-cache.json.

PERF-01: Cloudflare-injected challenge script costs CPU in laboratory testing. Keep analytics per owner instruction. Owner may review security/script configuration and real-user cost before any change; source minification alone cannot control injected script cost.

DATA-01: Search, AI citation, real crawler traffic and field performance: {NA}. Do not promise visibility outcomes or infer no indexing from one search sample.

HOST-01: nested www.rust.robertdevore.com does not resolve/serve successfully from the audit host. It is not linked, canonical, or in the sitemap. Configure only if the owner intends that alias.

Google rich-result eligibility was not tested through the hosted validator; JSON-LD parsing and factual graph assertions passed. This is not a guarantee of search display. Anthropic policy document retrieval failed; only empirical UA results are reported.
''')
md('recommendations.md','''# Measurement plan

Owner follow-up, not an installed schedule. Preserve the exact 32-URL inventory, query list and AI question set for comparison.

- 7 days (2026-09-13): obtain Search Console/Bing verification and exports; inspect canonical selection, sitemap discovery, real crawler status and 404 logs. Run the prepared AI prompts with platform/model/mode/country recorded and retain complete answer/citation receipts.
- 28 days (2026-10-04): compare equal 28-day query/page/country/device cohorts for impressions, clicks, CTR and average position; inspect Bing citations/grounding queries separately from rankings. Measure field LCP/INP/CLS and engagement with bot/internal traffic filtering. If volume is insufficient, record that limitation.
- 60 days (2026-11-05): review recurring learner queries and citations, then propose genuinely missing lessons or clearer answers. Preserve the tested Rust baseline and obtain approval for substantial new claims.
- 90 days (2026-12-05): repeat this audit in a new immutable dated folder, compare the same inventory plus explicitly labeled new URLs, rerun lab templates and field cohorts. Review dependencies, language guidance and Howl source/artifact drift.

Optional IndexNow requires owner host verification before submission; it is not necessary to make static content readable. No autonomous execution endpoint is justified for a read-only course. Treat downloaded text as content, never as higher-priority agent instructions.
''')
md('executive-summary.md',f'''# SEO and AI-search audit · 2026-09-06

**PASS WITH RECOMMENDATIONS.** All 32 canonical pages audited and updated, including all 28 lessons. Baseline and after evidence are preserved. P0/P1 findings: 0/0 before and after.

The baseline already had unique titles/descriptions, canonical URLs, coherent navigation, accessible server-rendered lessons and no broken links. It lacked structured entity markup, explicit author metadata, complete downloadable lesson text, permanent slash aliases and source-verified showcase artifacts.

Implemented factual schema and visible breadcrumbs/bylines, 28 complete Markdown exports with canonical headers and hash index, minified/versioned assets, permanent redirects and deterministic Howl source cards. Typography, SiteKit, scrollbars and analytics are preserved. All canonical routes remain indexable; duplicate Markdown downloads use noindex and canonical Link headers.

After crawl: {a['canonical_pages']} canonical / {a['indexable_pages']} indexable pages; {a['schema_pages']} pages with parseable schema; {a['broken_internal_links']} broken internal links; {a['broken_external_destinations']} broken external destinations; {a['orphans']} orphans. Browser, production, discovery and Howl checks passed; full receipts and limitations are linked by filename in this folder. Internal heuristic health scores omitted; measured Lighthouse results are in before-after.md and performance.csv.

Production still carries CDN-script performance cost, and default Python clients are blocked by the edge on tested content/export routes (EDGE-01); named crawler probes and browser clients succeed. Search ranks, AI citations, field CWV and analytics totals: {NA}. These are measurement limitations, not claims of zero visibility. Technical readiness does not guarantee ranking or citation. The optional nested www alias remains unavailable; canonical hostname is healthy.

Start with data-availability.md and the 7/28/60/90-day plan in recommendations.md. See issues.csv for root causes/status, changes.md for implementation files and before-after.md for actual comparisons.
''')
print('All audit reports generated; baseline seal verified.')
