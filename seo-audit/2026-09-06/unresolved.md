# Unresolved recommendations

No P0/P1 defect observed in the tested scope. No deployment blocker.

EDGE-01: default Python-urllib/3.10 receives 403 for the homepage, course-index.json, a lesson Markdown export, llms-full.txt and both bundled assets. Browser, Node fetch and named audit/crawler clients pass. This limits generic agent retrieval despite permissive robots. Exact rule/product cause is unknown without Cloudflare Security Events. Owner should review a narrowly scoped access policy; no broad security disablement is proposed. Evidence: raw/production-schema-cache.json.

PERF-01: Cloudflare-injected challenge script costs CPU in laboratory testing. Keep analytics per owner instruction. Owner may review security/script configuration and real-user cost before any change; source minification alone cannot control injected script cost.

DATA-01: Search, AI citation, real crawler traffic and field performance: NOT AVAILABLE — DATA ACCESS REQUIRED. Do not promise visibility outcomes or infer no indexing from one search sample.

HOST-01: nested www.rust.robertdevore.com does not resolve/serve successfully from the audit host. It is not linked, canonical, or in the sitemap. Configure only if the owner intends that alias.

Google rich-result eligibility was not tested through the hosted validator; JSON-LD parsing and factual graph assertions passed. This is not a guarantee of search display. Anthropic policy document retrieval failed; only empirical UA results are reported.
