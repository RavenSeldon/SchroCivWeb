[Project website](https://www.benamuwo.me/schrodingers_civ/) · [Research repository](https://github.com/RavenSeldon/schrodingers_civ.git)

# Publication visual inventory

Every source figure is preserved. CSVs and printed tables are reproduced without recomputing results. SHA-256 values are in `qa/import-manifest.json` (source inputs) and `dist/assets/source-manifest.json` (public bytes).

| Source | Visual | Public destination | Treatment |
| --- | --- | --- | --- |
| Audit PDF p4, Figure 1; dossier Figure 1 | Severity profile, panels A and B | `assets/figures/audit-1.svg`; dossier and full reader | Original dossier vector externalized; full printed PDF remains available |
| Audit PDF p4, Figure 2; dossier Figure 2 | Filtration gradient | `assets/figures/audit-2.svg`; dossier and full reader | Original dossier vector; caption and qualification retained |
| Audit PDF p5, Figure 3; dossier Figure 3 | Per-archive S4 density | `assets/figures/audit-3.svg`; dossier and full reader | Original dossier vector; no cross-model inference claim retained |
| Audit PDF p3, Table 1 | Corpus inventory and gate performance | Audit full-reader HTML and MD | Semantic HTML/Markdown table, six body rows |
| Audit PDF p3, Table 2 | Severity ladder and provenance | Audit full-reader HTML and MD | Four complete tier rows |
| Audit PDF p9, Table 3 | Adjudicated density by tier | Audit full-reader HTML and MD | Seven rows including subject-corrected OpenAI |
| Audit PDF p9, Table 4 | Confidence register | Audit full-reader HTML and MD | Nine rows, full uncertainty labels and basis |
| Dossier ladder | Four coloured severity rungs | `/audit/#ladder` | Full source text and semantic colour distinctions |
| Dossier finding | Four-register S4 bars | `/audit/#finding` | Original denominators, values and relative widths |
| Dossier confidence register | Claim/state/basis table | `/audit/#confidence` | Complete source table inside horizontal scroll region |
| Atlas PDF p1 | Small publication emblem | `assets/figures/atlas-emblem.png`; full reader | Rendered from supplied embedded image at 180 dpi; not reused as website branding |
| Atlas PDF p2 | Claim-family result table | Atlas full reader and MD | All four families and total row |
| Atlas PDF p3, Figure 1 | Printed Claim Transmission Atlas | `assets/figures/atlas-paper-figure.png`; full reader | Exact printed visual rendered from the PDF at 180 dpi, original caption retained |
| Atlas PDF p6 | Human-model agreement table | Atlas full reader and MD | Eight rows; starred BORDERLINE qualification retained |
| Current committed submission SVG | Expanded legibility Atlas | `assets/figures/atlas.svg`; `/atlas/#atlas-view` | Original vector bytes, 87 trees; zoom, drag, keyboard controls and SVG download |
| Submission tables 01–07 | Corpus, family, mechanisms, sensitivity, surface/body, agreement, strata | `assets/tables/`; `/atlas/#source-tables` | Original CSV bytes plus accessible tables; seven exports |
| Gallery PROLOGUE, I–XXI, EPILOGUE | 23 chapter backgrounds | `assets/art/*.webp`; corresponding chapter | One mapped source image per chapter; original-size WebP conversion |

No further empirical graphs were generated. The Atlas emblem is a publication aid, not a new finding. The original PDF copies are in `src/originals/` and do not ship in `dist/`. All public PDF editions retain all their source graphics and tables; only top-margin link headers are added.

Landing-only update: the user-supplied `maitrism-03-seal-final.svg` is now the hero image beside the project title. It is served byte-for-byte from `assets/identity/`, uses contain sizing without recolouring, and does not replace the Prologue chapter artwork. The same source bytes are also the publication-scoped `assets/favicon.svg`; the main blog favicon is untouched. Its source hash is in the import manifest.
