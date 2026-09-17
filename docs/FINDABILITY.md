# Findability: Getting Schrödinger's Civilization Into Search

This is a runbook for making the publication findable by anyone who looks for it, with the Translator's Tale first. It does not advertise the site. It tells search engines the site exists and leaves ranking to them.

Every claim below was either checked at the time of preparation or is quoted from the source named beside it. The files for the optional IndexNow step (Step 3) are in [`findability/`](findability/).

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

## 6. Observed at Preparation, Not Changed

- The landing page `<title>` repeats itself: *Schrödinger's Civilization — Schrödinger's Civilization*.
- `audit/` and `audit/paper/` share one title.
- The JSON-LD names the author "Ben Amuwo" on the WebSite, Book, Chapter and Atlas-paper entries, and "Benjamin Amuwo" on the Audit-paper entry. The visible site footer and `LICENSE-CONTENT.md` both use "Benjamin Amuwo".
