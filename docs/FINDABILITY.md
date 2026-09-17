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

## 8. Localized Tale Pages (Off by Default)

`scripts/build.mjs` can generate eight localized landing pages for the Tale, at `tale/<code>/`. They are cross-linked with `hreflang` and listed in the sitemap. The switch is `TALE_LOCALES_ENABLED`, and it ships as `false`. With it off, the build output is byte-identical to a build without this feature.

**Languages:** Français (`fr`), Español (`es`), Português (`pt`), Deutsch (`de`), Русский (`ru`), 日本語 (`ja`), 한국어 (`ko`), 简体中文 (`zh-Hans`). They were chosen as widely used web languages in which "Schrödinger's cat" is a common phrase. Russian and Korean also pair with IndexNow participants Yandex and Naver. This is a judgment call: the list is data in `src/content/tale-locales.json` and can be changed there.

**What each page contains,** all in its own language:

- a title and description
- a heading and short summary drawn from the site's own English wording: what the Tale is, what the Atlas studied, the Prologue's reading key, and the English title's pun
- links to the English Prologue, the English chapter index and the project home
- links to the other language versions

The chapters themselves are not translated. The site navigation and footer stay in English. When the switch is on, the English Tale index gains matching `hreflang` links and an "About this tale in other languages" row.

### Why It Ships Off

1. **The translations are unreviewed drafts.** An AI (Claude) wrote them, and no native speaker has checked them. `tale-locales.json` records this as `"status": "draft-unreviewed"`, and the build prints a warning if the pages are published in that state. The Tale's English pun (*tale*/*tail*) does not survive translation, so each page explains it rather than reproducing it.
2. **The pages sit near Google's doorway-abuse examples.** Google's spam policies list "Generating pages to funnel visitors into the actual usable or relevant portion of a site" as doorway abuse. Scaled content abuse includes generating many pages "through automated transformations like... translating." ([Spam policies](https://developers.google.com/search/docs/essentials/spam-policies)) These pages add a real summary in each language, but their main job is to send readers to English chapters. A violation can affect how the whole host ranks, and the Neurascape blog shares this host.
3. **The pages are short.** Their main content runs from roughly 90 to 190 word tokens, a crude count that undercounts Japanese and Chinese.
4. **Google judges language by visible text.** Google says it "uses the visible content of your page to determine its language" and does not use `lang` attributes. Each page carries English proper names (Claim Transmission Atlas, Schrödinger's Civilization) and English navigation, so detection is likely to succeed but is not certain. ([Managing multilingual sites](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites))
5. **Translated titles were not checked for collisions.** "The Translator's Tale" collides in English (§2), and the same may be true in other languages.

### To Switch It On

1. Have a native or fluent speaker review each locale in `src/content/tale-locales.json`. Then set its `"status"` to `"reviewed"`, or remove the locales that were not reviewed.
2. Set `const TALE_LOCALES_ENABLED=true;` in `scripts/build.mjs`.
3. Run `node scripts/build.mjs && npm run check`. The build should report 39 routes, and the check must pass.
4. Deploy per `DEPLOY.md` §A. Then add [`findability/urls-tale-locales.txt`](findability/urls-tale-locales.txt) to the URL list for Search Console or IndexNow.

### Verified When Introduced (2026-09-17)

- **Off:** the build output is identical to the previous build, file for file.
- **On:** the build reports 39 routes and the check passes (one heading per page, all local links resolve).
- **`hreflang`:** each of the 9 Tale pages lists the same 10 `hreflang` entries (English, 8 locales, `x-default`). Each page lists itself, which Google requires ("Each language version must list itself as well as all other language versions"), uses fully-qualified URLs, and has a self-referencing canonical. ([Localized versions](https://developers.google.com/search/docs/specialty/international/localized-versions))
- **Language attribute:** `<html lang>` matches each page's `hreflang` code.
- **English Tale index:** only the `hreflang` links and the language row were added.
- **Sitemap:** it parses as XML and lists 43 URLs.
- **Rendering:** French (375 px) and Japanese (1280 px) pages rendered without horizontal overflow or console errors, and the CJK glyphs rendered with system fonts. The site's own font stack has no CJK font, so readers' devices will supply one.

**Not established:** that any of these pages will be indexed or ranked, or that the translations are accurate enough to publish.
