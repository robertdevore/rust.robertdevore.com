# Edge access and measurement follow-up · 2026-09-06

Status: pending owner dashboard action; do not mark the access issue resolved.

## Confirmed cause and prepared fix

A default Python-urllib/3.10 request to /course-index.json returned HTTP 403, body `error code: 1010`, Ray a3706f5e3be10013 at 21:06:00 UTC. Cloudflare firewallEventsAdaptive independently identifies that exact request as action=block, source=bic, ruleId=bic. Browser Integrity Check is enabled; the zone has no explicit user-agent blocking rules.

Prepared configuration: browser-integrity-rule.json. Match only GET/HEAD on rust.robertdevore.com; set bic=false only. This removes browser-signature filtering for public read requests, preserving other protection and analytics. Zone ruleset listing showed no existing http_config_settings entrypoint. POST to the rulesets endpoint failed with Cloudflare API error10000 Authentication error; no rule was created. The owner was asked to deploy it through Configuration Rules. Re-read configuration before any retry to prevent duplication. Verify with unmodified Python urllib, all canonical HTML/Markdown routes and named crawler probes after deployment.

[Cloudflare BIC](https://developers.cloudflare.com/waf/tools/browser-integrity-check/) supports hostname-specific configuration exceptions; [error1010](https://developers.cloudflare.com/support/troubleshooting/http-status-codes/cloudflare-1xxx-errors/error-1010/) identifies browser-signature filtering. Retrieved 2026-09-06.

## Performance boundary

Cloudflare bot configuration reports fight_mode=true and enable_js=true. The [current free Bot Fight Mode contract](https://developers.cloudflare.com/bots/get-started/bot-fight-mode/) does not support hostname/path skip rules, and its JavaScript detections cannot independently be disabled. Removing that cost would require changing zone-wide protection (affecting other sites) or a different plan/configuration. Neither change was made. Analytics do not need to be disabled to resolve BIC.

## Newly available measurements

GraphQL Analytics is accessible through the connected Cloudflare API even though configuration writes are unauthorized. Previous audit data unavailability is a historical access observation, superseded for the following datasets by rum.json.

Window: 2026-09-06 00:00:00 UTC through 21:10:00 UTC exclusive, requestHost exactly rust.robertdevore.com. rumPageloadEventsAdaptiveGroups reports count439 and sum.visits437. rumWebVitalsEventsAdaptiveGroups reports count428, P75 LCP312000microseconds (312ms), INP112000microseconds (112ms), CLS0. Units verified through schema introspection. These are launch-day telemetry including automated browser QA and owner visits. They do not represent organic users, unique human visitors, or a clean28-day field cohort. Counts and percentiles are different event aggregates, not paired measurements per visitor.

Search Console/Bing Webmaster verified-property coverage was requested from the owner. Search rankings and AI citations remain NOT AVAILABLE — DATA ACCESS REQUIRED. Exploratory exact-domain/name web searches produced no identifiable course result in the returned sample; this is not proof of no indexing. Search visibility cannot be manufactured immediately on launch day. Preserve the original audit and compare future equal windows.

## Query contract

Cloudflare GraphQL POST /graphql, viewer.accounts filtered by accountTag; both RUM datasets filtered by requestHost, datetime_geq, datetime_lt. Aggregate only, no private visitor-level data stored. Source permissions: account analytics read; firewall event read. See rum.json for response.
