[Project website](https://www.benamuwo.me/schrodingers_civ/) · [Research repository](https://github.com/RavenSeldon/schrodingers_civ)

# Schrödinger's Civilization

A static research publication site: the Minded-Language Audit dossier and complete paper, the Claim Transmission Atlas explorer and complete paper, and all 23 illustrated chapters of The Translator's Tale.

## Build and preview

Requires Node 22+ and npm. Run from the website folder:

```sh
npm ci
npm run build
npm run check
npm run preview
```

Open **http://127.0.0.1:4173/schrodingers_civ/**. Preview listens only on the local machine; set `PORT` if 4173 is occupied. Stop it with Ctrl+C. Every route is a real HTML page; no backend, account, build service or service worker is required.

```sh
# In a second terminal, with preview still running:
npx playwright install chromium
npm run test:browser
npm run package
```

Build uses only versioned `src/` files and the pinned `marked` dependency. Network access is needed for initial dependency/browser installation, not ordinary builds or reading the site. `npm run package` creates source and deploy ZIPs in `release/`.

## What to deploy

Deploy **only `dist/`**, beneath the existing domain's `/schrodingers_civ/` path. Do not publish the workspace root, `src/originals/`, `qa/` or `handoff/`. See [the deployment guide](docs/DEPLOYMENT.md) for DigitalOcean, the scoped Nginx locations, atomic activation, cache policy and rollback.

The publication is live at <https://www.benamuwo.me/schrodingers_civ/>, served beside the existing Flask/Gunicorn blog on the same host. The blog owns the domain; this path is handled by a small isolated Flask blueprint that reads a static release directory and touches no database, model or migration. Both the apex and `www` hosts resolve to it. The deployment guide also documents a direct Nginx location as an alternative — install one owner for the path, not both.

## Source layout

| Path | Purpose |
| --- | --- |
| `src/content/` | PDF-derived reading Markdown, guided dossier HTML, complete story and chapter manifest |
| `src/assets/` | Selected public PDFs, immutable figure/CSV exports, compressed artwork |
| `src/originals/` | Supplied PDF bytes retained privately for provenance; excluded from deployment |
| `src/styles.css`, `src/app.js` | Shared design and small progressive enhancements |
| `scripts/build.mjs` | Deterministic static generation, publication ZIP and asset manifest |
| `scripts/serve.mjs` | Base-path-aware preview with redirects and genuine HTTP 404 |
| `scripts/check.mjs`, `scripts/browser-qa.mjs` | Static integrity and rendered browser checks |
| `qa/` | Verification reports, source-import manifest and screenshots |
| `docs/` | Deployment, source issues and complete visual inventory |
| `dist/` | Standalone public output |
| `release/` | Source and public deployment ZIPs |

## Editing

Change interface styles in `src/styles.css` and small interactions in `src/app.js`; shared page composition lives in `scripts/build.mjs`. Run build and the relevant checks afterward. The canonical base is deliberately fixed to `/schrodingers_civ/` with `www` in canonical URLs.

Change chapter focal points in `src/content/chapters.json` (`focal`, e.g. `65% 40%`). To replace an image, retain its public filename under `src/assets/art/`, update its dimensions and provenance in the chapter/source manifests, then build and inspect that chapter on mobile and desktop. Current source images are only 357–486 pixels wide. All 23 are integrated, but full-resolution masters would improve the large-screen experience. Do not upscale them and describe the result as recovered detail.

The complete narrative is in `src/content/tale-source.md`. Chapter boundaries are identified from the 23 original headings, not by alphabetic filename order. A chapter must never be shortened to fit its background. Alt+Left/Right navigates chapters; text selection and normal scrolling remain available. Viewer +/−, arrows and Home operate only when the viewer is focused. Touch pan/pinch is opt-in, so ordinary page scrolling remains available.

Publication readers are labelled derived editions. Their PDF and Markdown downloads include the two project URLs. The PDF bodies remain unchanged below the 35-point URL band. Audit source has 9 pages; Atlas has 6. See [source notes](docs/CONTENT-ISSUES.md) and [figure inventory](docs/FIGURE-INVENTORY.md). Do not replace these readers with the differently worded repository Markdown.

## Optional source-preparation tools

Regular builds never read Downloads or the research checkout. The one-time importer has the original paths recorded explicitly for provenance. To reproduce that preparation on the original workstation, install `requirements-preparation.txt` in an isolated Python environment and run:

```sh
python scripts/import-publications.py
python scripts/refine-readers.py
npm run build
python scripts/verify-publications.py
```

This importer reads the explicitly listed source publications, selected committed exports and `handoff/gallery/`. It must not be run as a routine interface build. It will regenerate derived reader source and PDF URL overlays; inspect differences before accepting them.

## Verification and limits

See [QA evidence](qa/QA.md) and machine reports in `qa/`. Presentation checks verify content integrity and interface behavior; they are not scholarly validation. Testing uses Chromium on macOS and emulated viewport/touch settings, not universal browser/device coverage. No independent fresh-context acceptance review has been claimed.

The landing hero uses the supplied Maitrism Seal SVG at `src/assets/identity/maitrism-03-seal-final.svg`. All 23 chapter images remain unchanged.

Optional requested Flask `url.py` and `views.py` integration: see [FLASK-WIRING.md](docs/FLASK-WIRING.md). Example files are included but have not been applied to WebDev. The supplied Maitrism Seal is also the favicon scoped to this publication; the main blog favicon is unchanged.

## License

Software (build scripts, stylesheet, client-side JavaScript) — MIT, see
[`LICENSE`](LICENSE). Publication content — CC BY 4.0, see
[`LICENSE-CONTENT.md`](LICENSE-CONTENT.md), which also names what is excluded:
the supplied chapter artwork, the identity mark, and the underlying research
package, none of which are relicensed here.
