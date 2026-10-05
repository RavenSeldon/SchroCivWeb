#!/usr/bin/env python3
"""Apply the "Schrödinger's Cat's Tail" alternate-title changes to transmission_live.

Writes nothing unless both files have the exact SHA-256 they were prepared against
and every replacement matches exactly once. Never runs git.
Usage:  python3 apply_tale_alias_to_repo.py ~/Root/transmission_live
"""
import hashlib, pathlib, sys
ROOT = pathlib.Path(sys.argv[1]).expanduser()
EXPECT = {
  "scripts/build.mjs":   "1558763002a24eb7219abfe08aa1e436a05bf336ecefd9a7098f421e2494db9b",
  "docs/FINDABILITY.md": "0c486879bb7087a8818b29dc443c363466a178fde87244e1f05374ab0e37a3a9",
}
RESULT = {
  "scripts/build.mjs":   "90428376299b0943bc0c0c7b94529a41e2685bf9d3994d5025840aed1b90807b",
  "docs/FINDABILITY.md": "1c4aff093e0746ba39c80990f6361a34328b644ab9138b216dbf396ed3113371",
}

EDITS = {'scripts/build.mjs': [("const LICENSE='https://creativecommons.org/licenses/by/4.0/';", "const LICENSE='https://creativecommons.org/licenses/by/4.0/';\n// The Tale's alternate title. It appears as visible text on the Tale index and the\n// home card, so the matching Book.alternateName describes content readers can see.\nconst TALE_ALIAS='Schrödinger’s Cat’s Tail';"), ('<p class="eyebrow">The Translator’s Tale · 23 chapters</p>', '<p class="eyebrow">The Translator’s Tale; or, ${TALE_ALIAS} · 23 chapters</p>'), ("page('tale/',{title:'The Translator’s Tale',description:'With Effort, to the Stars. A history of the Claim Transmission Atlas in 23 illustrated chapters.',", "page('tale/',{title:'The Translator’s Tale; or, '+TALE_ALIAS,description:TALE_ALIAS+': With Effort, to the Stars. A history of the Claim Transmission Atlas in 23 illustrated chapters.',"), ("alternateName:'The Translator’s Tale'", "alternateName:['The Translator’s Tale',TALE_ALIAS]"), ('<p class="eyebrow">The Translator’s Tale</p>', '<p class="eyebrow">The Translator’s Tale; or, ${TALE_ALIAS}</p>'), ('description:`Chapter ${c.stem} of The Translator’s Tale: With Effort, to the Stars.`', 'description:`Chapter ${c.stem} of The Translator’s Tale (${TALE_ALIAS}): With Effort, to the Stars.`')], 'docs/FINDABILITY.md': [('  Whether these surface the Tale depends on indexing, which this runbook cannot guarantee.\n', '  Whether these surface the Tale depends on indexing, which this runbook cannot guarantee.\n- **"Schrödinger\'s Cat\'s Tail" is a crowded query.** On 2026-09-17, in the same search service, it returned Springer\'s *Tails of Schrödinger\'s Cat*, a ResearchGate paper subtitled *Twisting the Tail of Schrödinger\'s Cat*, and Wikipedia\'s *Schrödinger\'s cat*. The Tale\'s own text never mentions Schrödinger, a cat, a tail or a box, so the alternate title (§6) is the page\'s only connection to that query. Established reference pages are likely to outrank it for the unquoted phrase.\n'), ('## 6. Observed at Preparation, Not Changed\n', '## 6. The Tale\'s Alternate Title\n\nThe Tale carries the alternate title **Schrödinger\'s Cat\'s Tail**, set once as `TALE_ALIAS` in `scripts/build.mjs`. It is there so the Tale can match searches that combine or blur "Schrödinger\'s cat", "Schrödinger\'s Civilization", "tale" and "tail".\n\n**Where it appears:**\n\n| Page | Place | Visible to readers? |\n| --- | --- | --- |\n| `/tale/` | `<title>`, `og:title`, `twitter:title`: *The Translator\'s Tale; or, Schrödinger\'s Cat\'s Tail* | Browser tab and share cards |\n| `/tale/` | Hero eyebrow above the heading | Yes |\n| `/tale/` | Meta, `og:` and `twitter:` descriptions | Snippets and share cards |\n| `/tale/` | JSON-LD `Book.alternateName` | No; mirrors the visible eyebrow |\n| `/` | Tale card eyebrow | Yes |\n| 23 chapters | Meta, `og:` and `twitter:` descriptions | Snippets and share cards |\n\nEach page shows the phrase to readers at most once.\n\n**Guardrails.** Keep future edits inside these limits:\n\n- **No hidden or repeated text.** Google\'s spam policies define keyword stuffing as "filling a web page with keywords or numbers in an attempt to manipulate rankings," and name hidden text, such as a font size or opacity of 0, as a violation. Sites that violate them "may rank lower in results or not appear in results at all." ([Spam policies](https://developers.google.com/search/docs/essentials/spam-policies))\n- **Structured data must describe visible content.** Google\'s structured-data policies say: "Don\'t mark up content that is not visible to readers of the page." ([General structured data guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)) If the eyebrow text is removed, remove the alias from `alternateName` too.\n- **No keywords meta tag.** Google "doesn\'t use the keywords meta tag." ([SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide))\n- **Descriptions are for snippets.** Google says snippets are "primarily created from the page content itself," with the meta description used when it describes the page better. It does not describe descriptions as a ranking factor. ([Snippets](https://developers.google.com/search/docs/appearance/snippet))\n\n**Verified when introduced:**\n\n- **Chapters:** only the three description fields changed, and `<body>` is byte-identical.\n- **Home:** only the Tale card eyebrow changed.\n- **Tale index:** only its title, description, `alternateName` and hero eyebrow changed.\n- **Rendering:** the phrase was visible at the same size and colour as the surrounding eyebrow text at 375 px and 1280 px wide, with no horizontal scrolling. On mobile both eyebrows wrap to two lines.\n- **Build:** build and check pass.\n\n**Not established:** that any search engine ranks the Tale for these searches. Before the change, the words "cat" and "tail" did not appear on `/tale/` at all; now they do. That makes a match possible; it does not guarantee one.\n\n## 7. Observed at Preparation, Not Changed\n')]}

new = {}
for rel, want in EXPECT.items():
    p = ROOT / rel
    got = hashlib.sha256(p.read_bytes()).hexdigest()
    if got == RESULT[rel]:
        sys.exit(f"Nothing to do: {rel} already has these changes. Nothing written.")
    if got != want:
        sys.exit(f"ABORT: {rel} differs from the version these edits were prepared against ({got[:12]} != {want[:12]}). Nothing written.")
    s = p.read_bytes().decode("utf-8")
    for old, rep in EDITS[rel]:
        n = s.count(old)
        if n != 1:
            sys.exit(f"ABORT: expected one match in {rel}, found {n}: {old[:60]!r}. Nothing written.")
        s = s.replace(old, rep)
    if hashlib.sha256(s.encode()).hexdigest() != RESULT[rel]:
        sys.exit(f"ABORT: result for {rel} is not the verified version. Nothing written.")
    new[rel] = s
for rel, s in new.items():
    (ROOT / rel).write_text(s, encoding="utf-8")
    print(f"updated {rel}  sha256 {RESULT[rel][:16]}")
print("Done. Nothing committed. Next: node scripts/build.mjs && npm run check && git diff")
