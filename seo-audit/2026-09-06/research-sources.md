# Current primary guidance · retrieved 2026-09-06

| Source | Classification | Supported conclusion / implementation limit |
|---|---|---|
| [Google generative AI guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) | Official guidance | Crawlable, useful original content and sound SEO remain foundational. Google does not use llms.txt for special ranking treatment. Search Console generative-AI inclusion must be verified by the owner; account state unavailable here. |
| [Google AI features](https://developers.google.com/search/docs/appearance/ai-features) | Official requirements/recommendations | Indexing/snippet eligibility and crawl access matter; no guarantee of inclusion. |
| [Google structured data](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data) | Official recommendation | JSON-LD communicates entities; markup must reflect visible facts. |
| [Google breadcrumb markup](https://developers.google.com/search/docs/appearance/structured-data/breadcrumb) | Official feature contract | Use ordered, named breadcrumb items and canonical URLs matching navigation. |
| [Google retired displays](https://developers.google.com/search/blog/2025/06/simplifying-search-results) | Official change | Course Info rich-result display was retired; Schema.org Course semantics do not imply rich-result eligibility. |
| [Canonical consolidation](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls) | Official recommendation | Keep canonical signals aligned; supplemental downloadable formats should identify their canonical HTML. |
| [Schema.org Course](https://schema.org/Course), [LearningResource](https://schema.org/LearningResource) | Vocabulary definition | Course and lesson entity types fit this content; no invented provider organization, awards, ratings, or completion guarantees. |
| [OpenAI crawlers](https://developers.openai.com/api/docs/bots) | Official crawler documentation | OAI-SearchBot, ChatGPT-User, and GPTBot have distinct discovery/fetch/training purposes. Preserve the existing owner policy. |
| [Perplexity crawlers](https://docs.perplexity.ai/docs/resources/perplexity-crawlers) | Official crawler documentation | Search crawling is distinct from user-triggered retrieval. A spoofed UA probe is not proof of real crawler access. |
| [Bing AI Performance](https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview) | Official product documentation | Citation/grounding reports are available to verified owners; aggregate citations are not rankings or authority scores. |
| [IndexNow](https://www.indexnow.org/documentation) | Official protocol | Optional change notifications require host verification; acceptance does not guarantee indexing. No submission claimed in this audit. |
| [Kujo Howl](https://github.com/kujolang/howl) | Source-backed tool contract | Local README and CLI help inspected; renders real source into deterministic artifacts, never executes Rust or improves ranking by itself. |

The Anthropic support URL returned a retrieval error; no policy conclusion is based on its unavailable content. Claude UA probes are empirical only. No training-crawler policy, analytics setting, DNS record, WAF rule, or external search-console configuration is changed by this audit.

Additional primary references: [Cloudflare static redirects](https://developers.cloudflare.com/workers/static-assets/redirects/) documents permanent asset redirects; query forwarding verified empirically. First-party comparison samples: [Learning Rust ownership](https://learningrust.org/lessons/06-ownership) and [100 Exercises to Learn Rust](https://rust-exercises.com/100-exercises/). Observed practice-oriented structure; no competitor ranking or quality superiority claim.
