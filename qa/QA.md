[Project website](https://www.benamuwo.me/schrodingers_civ/) · [Research repository](https://github.com/RavenSeldon/shrodingers_civ.git)

# Website verification record

**Later scoped update:** the landing hero and publication favicon now use the user-supplied Maitrism Seal. See `FOLLOWUP.md`, `landing-update.json` and `flask-wiring-check.json` for current checks and the optional, uninstalled Flask integration examples. The full-suite measurements below record the original implementation; their old byte counts and hashes are historical.

Local production-output verification completed 14 September 2026 UTC (13 September in Vancouver). This is implementation QA, not an independent fresh-context review or validation of research claims. Nothing was deployed.

## Environment and results

- macOS ARM64; Node 23.6.1; pinned Playwright 1.63.0; Chromium 153.0.8010.12; axe-core integration 4.10.2.
- Production output served at `http://127.0.0.1:4173/schrodingers_civ/`, with the exact requested subpath.
- **31 static routes**, including the custom 404 document; all directly navigated and reloaded. A nonexistent route separately returned actual HTTP 404. Missing trailing slash returned HTTP 308.
- **53 rendered layout checks:** all 31 routes at 360×800; representative home, dossier, explorer and poetry chapter at 844×390, 768×1024, 1024×768, 1440×1000 and 1920×1080; plus CSS 200% zoom and a 720×500 effective viewport. No horizontal page overflow or missing image in those checks. Horizontal table scrolling is intentional.
- **37 axe WCAG A/AA scans:** all 31 routes at 360×800 plus six representative desktop routes. Zero detected violations. This does not claim all WCAG success criteria or universal assistive-technology compatibility.
- Zero page-console exceptions and zero failed network requests in the full browser run.
- **1,857 local URL/fragment references** checked; **45 public asset hashes** checked both on disk and over HTTP. The final manifest itself lists public paths only. PDF, MD, CSV, SVG, WebP, PNG, JS, CSS and ZIP responses carry usable MIME types.
- Both linked PDF editions preserve page count (9 audit, 6 Atlas), all body glyphs/positions, and pixel-identical body rendering below the 35-point URL band at 90 dpi. Both clickable URLs exist on all 15 pages. Source files are untouched. The first/last linked pages were also rendered for visual inspection.
- The PDF-derived Markdown preserves four audit tables, two Atlas tables, all captions, references and retained appendices. A normalized alphanumeric character-multiset audit matches the source body exactly: **26,132 audit characters and 12,512 Atlas characters**, excluding plot interiors, repeated page furniture and added edition metadata. This is a completeness check, not a proof of semantic equivalence by itself; reading order, extracted tables and hyphenation were separately inspected.
- All **23 chapter prose blocks match the rendered HTML from their source Markdown**, including `<strong>`, `<em>`, paragraphs and hard line breaks. The supplied whole-story source SHA-256 remains `ffe7e60389e0b8ddf738146f929d85b8ff55ad4d016ce7023c9f2c5339d0ec46`.
- Artwork stems validated against the CSV, with no missing or duplicated chapter stems. The four extra reference sheets are explicitly excluded. No image is fabricated or mapped by lexicographic order.

## Interaction checks

- Drawer: close button, Escape, outside tap/click, navigation selection, explicit Tab/Shift+Tab focus loop and opener focus restoration all pass. Native modal background rejects programmatic focus. Closed dialog links do not participate in ordinary keyboard focus.
- Skip navigation works by Tab → Enter. Contextual links and the shared navigation remain ordinary URLs.
- Atlas: keyboard +/−, arrow panning, Home reset, button zoom, pointer dragging, pan-mode toggle and fit/reset pass. Emulated two-finger touch pinch enlarged the view to 205%; ordinary wheel scrolling still scrolls the page. Touch panning is opt-in and ordinary vertical scrolling is available when it is off.
- Actual PDF download yields `audit.pdf`; all asset downloads were fetched and their hashes matched.
- Tale: artwork modal and Escape restore focus; previous/next links, browser back/forward and Alt+Right navigation pass. No autoplay or scroll interception exists. Artwork and prose are separate elements.
- No-JavaScript audit, Atlas and prologue readers match the entire visible prose of their JavaScript versions.
- Reduced-motion media query is recognized and CSS disables transitions/animations.

## Visual inspection and contrast

Source PDF pages, all 23 supplied image mappings, all 23 mobile chapter screenshots, the landing page at desktop/phone, dossier at tablet and Atlas at desktop were inspected visually. Screenshots for the full viewport matrix are under `qa/screenshots/`.

The story text panel is 94% opaque over the artwork. Even assuming pure-white pixels behind it, calculated contrast is **13.91:1 for body prose** and **11.50:1 for italic emphasis**. Chapter-top links/progress also use dark backing. The original research figure palettes are preserved; website text uses its own restrained palette. Figure labels remain vector-sharp when opened or enlarged, though they are necessarily very small in a fit-to-screen overview.

## Performance measurements

The preview serves uncompressed files. One recorded local landing-page navigation reached DOMContentLoaded in **14.0 ms**, with a **6,940-byte HTML transfer**, **26,705-byte stylesheet transfer**, **5,979-byte script transfer** and **34,204-byte current artwork transfer**. These include per-response transfer overhead and describe localhost on this workstation, not public-network or mobile-device performance. Other publication imagery is lazy-loaded. The complete deployable output is about **3.90 MB**, including PDFs, vector figures, all artwork, source tables and the companion ZIP. There are no runtime third-party requests, remote fonts, analytics or service worker.

## Corrections made during QA

The original dossier table initially overflowed the phone layout; all source table variants are now wrapped in labelled horizontal scroll regions. The modal initially allowed a native Shift+Tab handoff outside its contents; an explicit focus loop was added. Test harness corrections normalized equivalent HTML entities, waited for the asynchronous dialog-close focus event, and compared complete no-JavaScript prose instead of an arbitrary character threshold. These harness corrections did not change the narrative.

## Limits and remaining inputs

- The provided chapter images are only 357–486 px wide. The illustrated experience is implemented, but full-resolution masters were not supplied and the backgrounds look soft on large screens. This is the remaining visual-quality input, not a missing chapter or a deployment dependency.
- Chromium emulation is not testing on physical phones, iOS Safari, Firefox, OS text scaling or a screen reader. Native browser-menu 200% zoom was not driven; CSS zoom and the halved effective viewport were tested and are identified as such. The CSS-zoom screenshot preserves the desktop media-query layout and is not evidence of native browser zoom behavior.
- The initial sandbox blocked the localhost listener and Chromium's macOS Mach-port startup. Approved local execution outside that sandbox enabled all reported browser checks. No sandbox failure is counted as a passing test.
- The existing `www.benamuwo.me` hosting configuration, TLS, Nginx integration and public-network performance were not inspected or tested. The supplied scoped configuration is an operator-reviewed deployment example. No DNS or server changes were made.
- Source-paper disagreements and retained draft-era text are listed in `docs/CONTENT-ISSUES.md`. The interface does not turn those into new research claims.

## Reproduction

```sh
npm ci
npm run build
npm run check
npm run preview
# In another terminal:
npx playwright install chromium
npm run test:browser
node scripts/final-checks.mjs
```

Optional PDF checks use the versions in `requirements-preparation.txt`:

```sh
python scripts/verify-publications.py
python scripts/content-integrity.py
```

Machine evidence: `static-check.json`, `browser-report.json`, `final-checks.json`, `publication-verification.json`, `prose-character-audit.json`, `gallery-inventory.json`, `import-manifest.json`, `reproducibility.json`. These checks are bounded to the delivered package.
