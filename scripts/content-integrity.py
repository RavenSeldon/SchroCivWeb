"""Character-multiset audit to catch omitted PDF prose or numerical table cells.
Figure interiors, running footers and edition metadata are deliberately excluded.
Meaning and reading order are separately inspected in the source/rendered editions.
"""
from pathlib import Path
import collections, re, unicodedata, json
import pdfplumber
root=Path(__file__).resolve().parents[1]
figures={'audit':{3:[(48,250),(357,620)],4:[(310,567)]},'atlas':{0:[(340,423)],2:[(44,410)]}}
def norm(s):return collections.Counter(re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKC',s).lower()))
report=[]
for name,file in [('audit','Minded_Language_Audit_v1.0_Amuwo_Reading_Edition.pdf'),('atlas','Claim_Transmission_Atlas_v1.0_Apart_Submission_FINAL.pdf')]:
 with pdfplumber.open(root/'src/originals'/file) as d:
  texts=[]
  for pi,p in enumerate(d.pages):
   chars=[c['text'] for c in p.chars if c['top']>35 and c['top']<(800 if name=='audit' else 768 if pi==0 else 755) and not any(a<=c['top']<b for a,b in figures[name].get(pi,[]))]
   texts.append(''.join(chars))
  source=''.join(texts)
 text=(root/f'src/content/{name}.md').read_text()
 text=re.sub(r'^\[Project website\].*\n','',text)
 text=re.sub(r'^> Derived reading edition.*\n','',text,flags=re.M)
 text=re.sub(r'<!--.*?-->','',text,flags=re.S)
 text=re.sub(r'!\[[^\]]*\]\([^)]*\)','',text)
 text=text.replace('## Title footnote','')
 a=norm(source);b=norm(text)
 # Source title superscript 1 is represented once at the footnote in Markdown.
 a['1']-=1
 missing=a-b;extra=b-a
 assert not missing and not extra,(name,missing,extra)
 report.append(dict(paper=name,missing=dict(missing),extra=dict(extra),sourceCharacters=sum(a.values()),readerCharacters=sum(b.values())))
(root/'qa/prose-character-audit.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
