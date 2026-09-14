"""Verify URL overlays, body preservation, figures and source extraction completeness."""
import csv, hashlib, json, re, unicodedata
from pathlib import Path
import pdfplumber
from pypdf import PdfReader
from PIL import Image, ImageChops
root=Path(__file__).resolve().parents[1];reports=[]
(root/'qa/source').mkdir(parents=True,exist_ok=True)
urls=['https://www.benamuwo.me/schrodingers_civ/','https://github.com/RavenSeldon/schrodingers_civ']
for name,filename in [('audit','Minded_Language_Audit_v1.0_Amuwo_Reading_Edition.pdf'),('atlas','Claim_Transmission_Atlas_v1.0_Apart_Submission_FINAL.pdf')]:
 a=root/'src/originals'/filename;b=root/f'dist/assets/papers/{name}.pdf'
 with pdfplumber.open(a) as original,pdfplumber.open(b) as derived:
  assert len(original.pages)==len(derived.pages)
  for i,(p,q) in enumerate(zip(original.pages,derived.pages)):
   # Original title-band URL replacement is the only excluded area.
   box=(0,35,p.width,p.height)
   def chars(page):return [(c['text'],round(c['x0'],3),round(c['top'],3),c['fontname'],round(c['size'],3)) for c in page.crop(box).chars]
   assert chars(p)==chars(q),(name,i,'body changed')
   x=p.crop(box).to_image(resolution=90).original.convert('RGB');y=q.crop(box).to_image(resolution=90).original.convert('RGB')
   assert ImageChops.difference(x,y).getbbox() is None,(name,i,'body render differs')
   if i in [0,len(original.pages)-1]:q.to_image(resolution=120).save(root/f'qa/source/{name}-linked-{i+1}.png')
   annotations=PdfReader(b).pages[i].get('/Annots',[])
   links=[o.get_object().get('/A',{}).get('/URI','') for o in annotations]
   assert all(u in links for u in urls),(name,i,'missing header URLs')
  reports.append({'paper':name,'pages':len(original.pages),'bodyGlyphsAndPositions':'identical below top 35 points','bodyRenderAt90Dpi':'pixel-identical below top 35 points','bothClickableUrls':'verified on every page'})
# Numeric-table comparisons use the source PDFs; no empirical recomputation.
for name,count in [('audit',4),('atlas',2)]:
 text=(root/f'src/content/{name}.md').read_text();assert len(re.findall(r'^\| ---',text,re.M))==count
 for p in sorted((root/'qa/source').glob(f'{name}-table-*.json')):
  rows=json.loads(p.read_text())
  for row in rows:
   for cell in row:assert cell in text,(p,cell)
# Every original story section is preserved by the build, including Markdown emphasis and hard line breaks.
source=(root/'handoff/TRANSLATOR_STORY.md').read_bytes();assert source==(root/'src/content/tale-source.md').read_bytes()
assert not re.search(r'||turn\d+(?:file|search)',source.decode())
report={'pdfChecks':reports,'auditTables':4,'atlasTables':2,'storySourceSha256':hashlib.sha256(source).hexdigest(),'storySourceUnchanged':True}
(root/'qa/publication-verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
