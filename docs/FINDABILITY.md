# Findability: Getting Schrödinger's Civilization Into Search

This is a runbook for making the publication findable by anyone who looks for it, with the Translator's Tale first. It does not advertise the site. It tells search engines the site exists and leaves ranking to them.

Each factual statement below was checked at the time of preparation, or is quoted from the source named beside it. The rest — what is likely to rank, which searches are more distinctive — is judgment, not measurement. The files for the optional IndexNow step (Step 3) are in [`findability/`](findability/).

---

## 1. State at Preparation

The live release was checked from a browser on 2026-09-17 at 01:56 UTC.

**What was checked:**

- **Build provenance.** Every one of the 92 files under `https://benamuwo.me/schrodingers_civ/` was hashed. They were compared with a build of `45387eb` plus the discovery-layer changes to `scripts/build.mjs`, which were uncommitted at the time. 91 files matched byte for byte. The 92nd, `assets/source-manifest.json`, differed for one reason: that release also published a macOS `assets/.DS_Store`. Builds from this change onward exclude dotfiles.
- **No blocking headers.** All 92 files answered `200`, and none carried an `X-Robots-Tag` header. The build emits no `<meta name="robots">`.
- **Canonical host.** Every page declares `https://benamuwo.me/schrodingers_civ/…` (no `www`) as canonical. `www.benamuwo.me/schrodingers_civ/tale/` was also checked: it serves the Tale and declares the same canonical.
- **Sitemap.** `https://benamuwo.me/schrodingers_civ/sitemap.xml` lists 35 URLs: the 30 pages plus the two PDFs and three Markdown editions. The blog's `robots.txt` references this sitemap.
- **Structured data.** Pages carry schema.org JSON-LD (WebSite, Book, Chapter, ScholarlyArticle). The two paper pages also carry Google Scholar `citation_*` tags.

**Not established:** whether any search engine has indexed the site. Three queries to one web search service, run earlier that hour, returned no `benamuwo.me` page. That shows the site was absent from that one service at that moment, and nothing more; the GitHub README already links to the site, so engines may have found it.

## 2. Limits

- **Inclusion is the engine's decision.** Google's documentation says requesting a crawl "does not guarantee that inclusion in search results will happen instantly or even at all," and that crawling "can take anywhere from a few days to a few weeks." ([Ask Google to recrawl](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl))
- **Canonical is a signal, not a command.** Google describes `rel="canonical"` as "a strong signal," weaker than a redirect, so it keeps the final say over which URL it shows. ([Consolidate duplicate URLs](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls))
- **The bare titles collided with other works at preparation.** In the same search service, "Schrödinger's Civilization" alone returned Civilization VI's *Erwin Schrödinger* pages. "The Translator's Tale" alone returned Helen Fry's *Nuremberg: The Translator's Tale* (Yale UP), Emen's novel of that name, and a 2004 NPR piece. Two-term searches are more distinctive, for example:
  - `Translator's Tale Schrödinger's Civilization`
  - `Translator's Tale Claim Transmission Atlas`
  - a chapter title plus `Translator's Tale`

  Whether these surface the Tale depends on indexing, which this runbook cannot guarantee.
- **"Schrödinger's Cat's Tail" is a crowded query.** On 2026-09-17, in the same search service, it returned Springer's *Tails of Schrödinger's Cat*, a ResearchGate paper subtitled *Twisting the Tail of Schrödinger's Cat*, and Wikipedia's *Schrödinger's cat*. The Tale's own text never mentions Schrödinger, a cat, a tail or a box, so the alternate title (§6) is the page's only connection to that query. Established reference pages are likely to outrank it for the unquoted phrase.

## 3. Steps, Tale First

### Step 1: Google Search Console (Google)

1. At <https://search.google.com/search-console>, choose **Add property → Domain** and enter `benamuwo.me`.
2. Verify ownership with the DNS `TXT` record Google shows. A Domain property "includes all subdomains (m, www, and so on) and multiple protocols," and requires DNS verification. ([Search Console Help: add a property](https://support.google.com/webmasters/answer/34592))
3. Under **Sitemaps**, submit `https://benamuwo.me/schrodingers_civ/sitemap.xml`.
4. Under **URL Inspection**, request indexing in this order:
   1. `https://benamuwo.me/schrodingers_civ/tale/`
   2. `https://benamuwo.me/schrodingers_civ/tale/prologue/`
   3. `https://benamuwo.me/schrodingers_civ/`

   Then continue down [`findability/urls-tale-first.txt`](findability/urls-tale-first.txt). Google says: "There's a quota for submitting individual URLs and requesting a recrawl multiple times for the same URL won't get it crawled any faster." The sitemap covers any URL not requested by hand.
5. Monitor progress with the Index Status report or the URL Inspection tool, which are the two tools Google's recrawl documentation names for this.

### Step 2: Bing Webmaster Tools (Bing)

At <https://www.bing.com/webmasters>, choose **Import from Google Search Console**. Bing's announcement describes this as importing "verified sites and sitemaps" with no separate verification. ([Bing Webmaster Blog, Sept 2019](https://blogs.bing.com/webmaster/september-2019/import-sites-from-search-console-to-bing-webmaster-tools)) Then confirm the sitemap from Step 1 is listed under **Sitemaps**.

### Step 3 (Optional): IndexNow

A single submission is shared with every participating engine. ([IndexNow documentation](https://www.indexnow.org/documentation)) The published participant list names Bing, Yandex, Seznam, Naver, Yep, the Internet Archive and Amazonbot. ([indexnow.org/searchengines.json](https://www.indexnow.org/searchengines.json))

Because the Internet Archive participates, submitting may lead to the pages being archived beyond the site's own lifetime. Skip this step if visibility should last only while the site is up.

1. **Install the key.** On the droplet, add the single `location` block from [`findability/nginx-indexnow-key.conf`](findability/nginx-indexnow-key.conf) to the HTTPS server block that serves `benamuwo.me`. Then run:

   ```bash
   sudo nginx -t && sudo systemctl reload nginx
   ```

   The snippet was checked with `nginx -t` and a live request on a local nginx 1.24, not in the droplet's own configuration. `nginx -t` on the droplet is the real test.
2. **Confirm the key is served.** This must print exactly `bb04f9030ee793b9013b131113bf5e1c`:

   ```bash
   curl -s https://benamuwo.me/bb04f9030ee793b9013b131113bf5e1c.txt
   ```
3. **Submit.** From the repo root, run:

   ```bash
   bash docs/findability/submit-indexnow.sh
   ```

   The script submits nothing unless the key is live and exact, every URL answers `200`, and every URL is under `https://benamuwo.me/schrodingers_civ/`. Per the IndexNow documentation, a `202` response means the URLs were received and key validation is pending.

### Step 4: Check Back

After a week or two, run **URL Inspection** on `https://benamuwo.me/schrodingers_civ/tale/` in Search Console. It reports whether the page is indexed and which canonical Google selected.

## 4. Keeping It Findable

These would take pages out of search, and nothing in this runbook prevents them:

- **Pages stop answering.** Per `DEPLOY.md`, a `503` means the release files are missing.
- **Crawling is blocked.** A `robots.txt` rule could disallow `/schrodingers_civ/`.
- **Pages are marked `noindex`.**
- **The canonical host changes.** Changing `ORIGIN` again changes every canonical URL, so each engine must re-consolidate every page.

## 5. Chapter Titles

In each chapter's `<title>`, `og:title` and `twitter:title`, the chapter name is followed by `· The Translator's Tale`. The `<title>` reads, for example:

> Before The Constellations · The Translator's Tale — Schrödinger's Civilization

**Basis.** Google's title-link documentation lists "Content in `<title>` elements" first among the sources for the title shown in results. The same documentation does not describe titles as a ranking factor. ([Influencing title links](https://developers.google.com/search/docs/appearance/title-link)) The change puts the Tale's name in the titles of 24 of the 30 HTML pages. Whether that raises the Tale's visibility is not established.

**Verified when introduced:** in all 23 chapters, only those three fields changed, and each `<body>` stayed byte-identical.

## 6. The Tale's Alternate Title

The Tale carries the alternate title **Schrödinger's Cat's Tail**, set once as `TALE_ALIAS` in `scripts/build.mjs`. It is there so the Tale can match searches that combine or blur "Schrödinger's cat", "Schrödinger's Civilization", "tale" and "tail".

**Where it appears:**

| Page | Place | Visible to readers? |
| --- | --- | --- |
| `/tale/` | `<title>`, `og:title`, `twitter:title`: *The Translator's Tale; or, Schrödinger's Cat's Tail* | Browser tab and share cards |
| `/tale/` | Hero eyebrow above the heading | Yes |
| `/tale/` | Meta, `og:` and `twitter:` descriptions | Snippets and share cards |
| `/tale/` | JSON-LD `Book.alternateName` | No; mirrors the visible eyebrow |
| `/` | Tale card eyebrow | Yes |
| 23 chapters | Meta, `og:` and `twitter:` descriptions | Snippets and share cards |

Each page shows the phrase to readers at most once.

**Guardrails.** Keep future edits inside these limits:

- **No hidden or repeated text.** Google's spam policies define keyword stuffing as "filling a web page with keywords or numbers in an attempt to manipulate rankings," and name hidden text, such as a font size or opacity of 0, as a violation. Sites that violate them "may rank lower in results or not appear in results at all." ([Spam policies](https://developers.google.com/search/docs/essentials/spam-policies))
- **Structured data must describe visible content.** Google's structured-data policies say: "Don't mark up content that is not visible to readers of the page." ([General structured data guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)) If the eyebrow text is removed, remove the alias from `alternateName` too.
- **No keywords meta tag.** Google "doesn't use the keywords meta tag." ([SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide))
- **Descriptions are for snippets.** Google says snippets are "primarily created from the page content itself," with the meta description used when it describes the page better. It does not describe descriptions as a ranking factor. ([Snippets](https://developers.google.com/search/docs/appearance/snippet))

**Verified when introduced:**

- **Chapters:** only the three description fields changed, and `<body>` is byte-identical.
- **Home:** only the Tale card eyebrow changed.
- **Tale index:** only its title, description, `alternateName` and hero eyebrow changed.
- **Rendering:** the phrase was visible at the same size and colour as the surrounding eyebrow text at 375 px and 1280 px wide, with no horizontal scrolling. On mobile both eyebrows wrap to two lines.
- **Build:** build and check pass.

**Not established:** that any search engine ranks the Tale for these searches. Before the change, the words "cat" and "tail" did not appear on `/tale/` at all; now they do. That makes a match possible; it does not guarantee one.

## 7. Observed at Preparation, Not Changed

- The landing page `<title>` repeats itself: *Schrödinger's Civilization — Schrödinger's Civilization*.
- `audit/` and `audit/paper/` share one title.
- The JSON-LD names the author "Ben Amuwo" on the WebSite, Book, Chapter and Atlas-paper entries, and "Benjamin Amuwo" on the Audit-paper entry. The visible site footer and `LICENSE-CONTENT.md` both use "Benjamin Amuwo".

## 8. Localized Tale Pages (On)

`scripts/build.mjs` generates eight localized landing pages for the Tale at `tale/<code>/`. The switch is `TALE_LOCALES_ENABLED`; it shipped as `false` in commit `e57918e` and was set to `true` on 2026-10-05 at the author's instruction. With it off, the build output is identical to a build without the feature, file for file.

**Languages:** Français (`fr`), Español (`es`), Português (`pt`), Deutsch (`de`), Русский (`ru`), 日本語 (`ja`), 한국어 (`ko`), 简体中文 (`zh-Hans`). They were chosen as widely used web languages in which "Schrödinger's cat" is a common phrase. Russian and Korean also pair with the IndexNow participants Yandex and Naver. The list is data in `src/content/tale-locales.json` and can be changed there.

**What each page contains,** all in its own language:

- a distinct `<title>` and description
- a translated heading and lede
- six paragraphs of summary drawn from the site's own English material: what the Tale is, what the Atlas audited and what it found, what the Minded-Language Audit examines, the Prologue's reading key, the English title's pun, and a statement that the chapters themselves are in English
- links to the English Prologue, the English chapter index and the project home
- a row of links to the other language versions

The chapters are not translated. The site navigation and footer stay in English. The English Tale index gains matching `hreflang` links and an "About this tale in other languages" row; nothing else on it changes.

### Why These Are Localized Pages and Not Doorway Pages

Google's spam policies name doorway abuse as "Generating pages to funnel visitors into the actual usable or relevant portion of a site," and scaled content abuse as generating many pages "through automated transformations like… translating." ([Spam policies](https://developers.google.com/search/docs/essentials/spam-policies)) Classification is Google's decision, not ours. These are the design choices made against it:

| Decision | Reason |
| --- | --- |
| One page per language, not one per chapter | 8 new pages, not 184. Nothing here is generated at scale. |
| Substantive, language-specific summaries | 560–1,186 characters of main content per page, excluding whitespace, each saying something a reader could not get from the English page without reading English. |
| No machine-translated chapters | The 23 chapters stay English-only. No page is a translated duplicate of another page. |
| Reciprocal `hreflang` plus `x-default` | This is Google's documented signal for "localized version," the opposite of an unrelated doorway. ([Localized versions](https://developers.google.com/search/docs/specialty/international/localized-versions)) |
| Self-referencing canonicals | Each page claims only itself. None tries to inherit the English page's signals. |
| A visible language row on every Tale page | Readers can move between versions by hand. |
| No automatic redirects or IP/`Accept-Language` sniffing | Google asks that users and crawlers not be redirected by inferred language. |
| Structured data that matches what is visible | Each page carries one `WebPage` entity: its own name, description, URL and `inLanguage`, `isPartOf` the site, `about` the English Book. |
| Honest framing in the text | Each page says, in its own language, that the chapters and papers are in English. |

### Known Weaknesses

1. **No native speaker has read these pages.** Claude (an AI) wrote them from the site's English wording. They were then checked twice by other model instances given the eight locales cold, with no sight of the English, and asked to back-translate literally and flag defects. Those passes found real errors — a German subtitle that read "barely making it to the stars", a subjectless Portuguese verb, a Chinese gloss that said "humankind" where it meant "the human", and five languages naming the downloadable papers as five different categories — and 23 corrections were applied on 2026-10-05. The record is in [`findability/tale-locales-backtranslation.md`](findability/tale-locales-backtranslation.md). A machine checking a machine is not a native reader: `tale-locales.json` keeps `"status": "draft-unreviewed"`, and the build prints a warning on every run while it does. Set it to `"reviewed"` only after a person who speaks the language has read the page.
2. **Google judges language by visible text.** Google says it "uses the visible content of your page to determine its language" and does not use `lang` attributes. Each page carries English proper names and English navigation, so detection is likely but not certain. ([Managing multilingual sites](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites))
3. **Translated titles were not checked for collisions.** "The Translator's Tale" collides in English (§2); the same may be true in other languages.
4. **The Japanese and Chinese pages are the shortest** at 811 and 677 characters of main content.
5. **The pun does not survive translation.** Each page explains *tale*/*tail* rather than reproducing it.

### To Switch Off

Set `const TALE_LOCALES_ENABLED=false;` in `scripts/build.mjs`, rebuild and redeploy. The eight URLs then 404 and leave the sitemap. Do this only if they have not been indexed; removing indexed pages is worse than never publishing them.

### Verified 2026-10-05, on a clean build of `e57918e` plus this change

- **Build and check:** `node scripts/build.mjs` reports 39 routes; `node scripts/check.mjs` passes (one `h1` per page, 2,134 local links resolve, asset hashes match).
- **Diff against the locales-off build:** the only changes are the 8 new pages, `routes.json`, `sitemap.xml`, and the English Tale index, which gains the `hreflang` links and the language row and nothing else.
- **`hreflang`:** each of the 9 Tale pages lists the same 10 entries (English, 8 locales, `x-default`), fully qualified, each listing itself, with a self-referencing canonical.
- **`<html lang>`** matches each page's `hreflang` code; each page carries `og:locale` plus 8 `og:locale:alternate`.
- **Distinctness:** the highest word overlap between any two localized pages is 45 %, between Spanish and Portuguese, which is cognate vocabulary in two closely related languages. No page is a translation of another page in the set.
- **Main content:** 560–1,186 characters per page, excluding whitespace.
- **Structured data:** each localized page carries one `WebPage` entity giving its own name, description, URL and `inLanguage`, `isPartOf` the site and `about` the English Book. Every field describes something visible on the page.
- **French typography:** narrow no-break spaces (U+202F) before `:`, `%` and inside `« »`, 10 occurrences in the main content, no stray punctuation at line start.
- **Rendering:** French at 375 px and Japanese at 1280 px, no horizontal overflow, no console errors. CJK glyphs come from the reader's system fonts; the site's stack has none.
- **Sitemap:** parses as XML, 43 URLs, all 8 localized pages present.

**Not established:** that any of these pages will be indexed or ranked, that Google will classify them as intended, or that the translations are accurate enough to publish. The back-translations supplied with this change are the author's means of checking the second point.
