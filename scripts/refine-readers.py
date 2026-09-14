"""Deterministic, presentation-only corrections after PDF text extraction."""
from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
p=root/'src/content/audit.md';s=p.read_text()
# Rejoin sentences crossing pages and move the source footnote to the end.
foot=re.search(r'\n\n1Research conducted.*?\n\n',s,re.S)
if foot:
 note=foot.group().strip()[1:];s=s[:foot.start()]+s[foot.end():];s+='\n\n## Title footnote\n\n1. '+note+'\n'
s=re.sub(r'and\s*<!-- source-page: 2 -->\s*reports','and reports',s)
s=re.sub(r'anthropo-\s*<!-- source-page: 5 -->\s*morphising','anthropomorphising',s)
s=s.replace('## 3.','### 3.').replace('### 3. Methods','## 3. Methods').replace('## 4.1','### 4.1').replace('## 4.2','### 4.2').replace('## 4.3','### 4.3').replace('## 4.4','### 4.4')
# Restore figure accessibility; the original vectors retain every plot label.
s=s.replace('![Publication figure; full caption follows](../figures/audit-1.svg)','![Severity profile: absolute density and tier composition across six registers](../figures/audit-1.svg)').replace('![Publication figure; full caption follows](../figures/audit-2.svg)','![Filtration gradient across the internal, method, published and external registers](../figures/audit-2.svg)').replace('![Publication figure; full caption follows](../figures/audit-3.svg)','![Per-archive personhood and ritual density; model colours do not support cross-model inference](../figures/audit-3.svg)')
p.write_text(s)
p=root/'src/content/atlas.md';s=p.read_text().replace('\n\n• ','\n\n- ')
s=s.replace('* The 100% borderline',r'\* The 100% borderline')
s=s.replace('![Publication figure; full caption follows]','![Claim Transmission Atlas, as reproduced on page 3 of the supplied final PDF]')
p.write_text(s)
