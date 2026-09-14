"""One-time, read-only source import. Run with the pinned preparation environment.
Normal website builds need only Node and the versioned src/ directory.
"""
from pathlib import Path
import csv, hashlib, io, json, re, shutil, unicodedata
import pdfplumber
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
RESEARCH=Path('/Users/theda/Root/transmission')
BASE='https://www.benamuwo.me/schrodingers_civ/'
GITHUB='https://github.com/RavenSeldon/shrodingers_civ.git'
HEADER=f'[Project website]({BASE}) · [Research repository]({GITHUB})\n\n'
records=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def record(p,dest,role):records.append(dict(source=str(p),destination=str(dest.relative_to(ROOT)),sha256=sha(p),role=role))
def copy(p,dest,role):
 dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest);record(p,dest,role)
for p in (RESEARCH/'submission/tables').glob('*.csv'):copy(p,ROOT/'src/assets/tables'/p.name,'Frozen source table; no recalculation')
copy(RESEARCH/'submission/assets/claim_transmission_atlas.svg',ROOT/'src/assets/figures/atlas.svg','87-tree expanded legibility vector, disclosure chronology corrected; unmodified')
raw=Path('/Users/theda/Downloads/Apart Research Sprint/Minded_Language_Audit_Dossier.html').read_text()
svgs=re.findall(r'<svg\b.*?</svg>',raw,re.S)
for i,s in enumerate(svgs):
 (ROOT/f'src/assets/figures/audit-{i+1}.svg').write_text(s)
# Preserve the complete guided narrative; replace its stale download section only.
body=raw[raw.index('<header>'):raw.index('<!-- =============================== DOWNLOAD -->')]
for i,s in enumerate(svgs):body=body.replace(s,f'<img src="@@BASE@@assets/figures/audit-{i+1}.svg" alt="Audit figure {i+1}; description and interpretation in the adjacent caption" loading="lazy">')
body=re.sub(r'<!--.*?-->','',body,flags=re.S)
(ROOT/'src/content/dossier.html').write_text(body)
record(Path('/Users/theda/Downloads/Apart Research Sprint/Minded_Language_Audit_Dossier.html'),ROOT/'src/content/dossier.html','Guided dossier; SVGs externalized; stale PDF script and download notes omitted')
copy(ROOT/'handoff/TRANSLATOR_STORY.md',ROOT/'src/content/tale-source.md','Original narrative with chat citation markers already removed')
rows=list(csv.DictReader(open(ROOT/'handoff/STORY_IMAGE_MANIFEST.csv')))
expected={r['image_stem'] for r in rows}; files=list((ROOT/'handoff/gallery').glob('*'))
valid=[p for p in files if p.suffix.lower() in {'.png','.jpg','.jpeg','.webp'} and p.stem in expected]
assert {p.stem for p in valid}==expected and len(valid)==23,'Missing or duplicate chapter art'
art=[]
for row in rows:
 p=next(p for p in valid if p.stem==row['image_stem']);im=Image.open(p).convert('RGB');dest=ROOT/'src/assets/art'/f'{p.stem.lower()}.webp';im.save(dest,'WEBP',quality=88,method=6)
 slug='prologue' if p.stem=='PROLOGUE' else 'epilogue' if p.stem=='EPILOGUE' else row['section_title'].lower().replace(',','').replace("'",'')
 slug=re.sub('[^a-z0-9]+','-',slug).strip('-')
 art.append(dict(order=int(row['order']),stem=p.stem,title=row['section_title'],slug=slug,width=im.width,height=im.height,focal='50% 50%',file=dest.name,sourceSha256=sha(p)))
 record(p,dest,'Chapter artwork; WebP at original dimensions, no upscaling')
(ROOT/'src/content/chapters.json').write_text(json.dumps(art,indent=2))
(ROOT/'qa/gallery-inventory.json').write_text(json.dumps(dict(chapters=art,excluded=[p.name for p in files if p not in valid],limitation='Supplied chapter images are 357–486 px wide. Full-resolution masters were not supplied. No synthetic upscaling performed.'),indent=2))
# Table boundaries are manually verified against the rendered final PDFs.
TABLES={
 'audit':{2:[(200,302,[55,121,161,193,226,258,541],[203,222,235,248,261,274,287,301]),(362,518,[55,85,185,285,541],[365,385,420,455,490,518])],8:[(109,226,[55,350,382,409,438,466,500,541],[110,129,142,155,168,181,194,207,225]),(263,413,[55,222,285,541],[265,283,295,309,333,346,357,372,385,398,413])]},
 'atlas':{1:[(409,492,[54,145,210,290,349,430,504,558],[410,423,437,450,464,477,492])],5:[(93,219,[54,218,349,468,558],[94,107,121,135,149,163,177,191,205,219])]}}
FIGS={'audit':{3:[(48,250,'audit-1.svg'),(357,620,'audit-2.svg')],4:[(310,567,'audit-3.svg')]},'atlas':{0:[(340,423,'atlas-emblem.png')],2:[(44,410,'atlas-paper-figure.png')]}}
# Page-level references retain all figures even when one is also available as an interactive vector.
for name,filename in [('audit','Minded_Language_Audit_v1.0_Amuwo_Reading_Edition.pdf'),('atlas','Claim_Transmission_Atlas_v1.0_Apart_Submission_FINAL.pdf')]:
 source=ROOT/'handoff'/filename
 copy(source,ROOT/'src/originals'/filename,'Immutable supplied PDF, excluded from public output')
 reader=PdfReader(source);writer=PdfWriter();writer.clone_document_from_reader(reader)
 for i,page in enumerate(writer.pages):
  w=float(page.mediabox.width);h=float(page.mediabox.height)
  packet=io.BytesIO();c=canvas.Canvas(packet,pagesize=(w,h),invariant=1)
  # Atlas p1 already carries an obsolete URL header: replace only its empty top band.
  c.setFillColorRGB(*( (0,0,0) if name=='audit' else (1,1,1)));c.rect(0,h-35,w,35,fill=1,stroke=0)
  c.setFillColorRGB(*( (.8,.84,.88) if name=='audit' else (.12,.16,.2)));c.setFont('Helvetica',6)
  for y,url in [(h-14,BASE),(h-24,GITHUB)]:
   c.drawString(40,y,url);c.linkURL(url,(40,y-1,40+c.stringWidth(url,'Helvetica',6),y+7),relative=0)
  c.save();page.merge_page(PdfReader(packet).pages[0])
 writer.add_metadata({'/Title': 'Who is speaking when a Worker speaks?' if name=='audit' else 'How Faithfully Did the Press Transmit the Record?', '/Subject':'Website reading edition: project and research repository links added; publication body unchanged'})
 with open(ROOT/f'src/assets/papers/{name}.pdf','wb') as f:writer.write(f)
 page_blocks=[]
 with pdfplumber.open(source) as doc:
  for pi,page in enumerate(doc.pages):
   events=[];exclusions=[]
   for top,bottom,xs,ys in TABLES[name].get(pi,[]):
    exclusions.append((top,bottom));out=[]
    for ya,yb in zip(ys,ys[1:]):
     cells=[]
     for xa,xb in zip(xs,xs[1:]):
      cell=page.filter(lambda o: o.get('object_type')=='char' and xa <= (o['x0']+o['x1'])/2 < xb and ya <= (o['top']+o['bottom'])/2 < yb).extract_text(x_tolerance=1) or ''
      cells.append(unicodedata.normalize('NFKC',cell).replace('\n',' ').replace('|','\\|'))
     out.append(cells)
    md='| '+' | '.join(out[0])+' |\n| '+' | '.join(['---']*len(out[0]))+' |\n'+'\n'.join('| '+' | '.join(r)+' |' for r in out[1:])
    events.append((top,'table',md));(ROOT/f'qa/source/{name}-table-{pi}-{int(top)}.json').write_text(json.dumps(out,indent=2))
   for top,bottom,file in FIGS[name].get(pi,[]):
    exclusions.append((top,bottom));events.append((top,'figure',f'![{"Publication emblem" if "emblem" in file else "Publication figure; full caption follows"}](../figures/{file})'))
    if file.endswith('.png'):
     bbox=next(im for im in page.images if im['top']>=top and im['bottom']<=bottom)
     page.crop((bbox['x0'],bbox['top'],bbox['x1'],bbox['bottom'])).to_image(resolution=180).save(ROOT/f'src/assets/figures/{file}')
   lines=page.extract_text_lines(x_tolerance=1)
   for line in lines:
    top=line['top'];bottom=line['bottom'];t=unicodedata.normalize('NFKC',line['text'])
    if (name=='audit' and top>800) or (name=='atlas' and ((top>755 and not (pi==0 and top<768)) or (pi==0 and top<35))) or any(a<=top<b for a,b in exclusions):continue
    if name=='atlas' and pi==0 and t=='1':continue
    # Detect source headings from typeface and size, without interpreting prose.
    cs=[ch for ch in line['chars'] if ch['text'].strip()];font=cs[0]['fontname'] if cs else '';size=max((ch['size'] for ch in cs),default=0)
    heading=(name=='audit' and all('Heros-Bold' in c['fontname'] for c in cs) and size>=9.9) or (name=='atlas' and all('Bold' in c['fontname'] for c in cs) and size>=10)
    if pi==0 and top<190:heading=False
    events.append((top,'heading' if heading else 'text',t,bottom))
   events.sort();blocks=[];buf='';lastbottom=None
   for e in events:
    top,kind,t=e[:3]
    if kind!='text':
     if buf:blocks.append(buf);buf=''
     blocks.append(('## ' if kind=='heading' else '')+t);lastbottom=None;continue
    if buf and (lastbottom is None or top-lastbottom>(3 if name=='atlas' else 4.5) or re.match(r'^(?:[•]|\d+\. )',t)):
     blocks.append(buf);buf=''
    if buf.endswith('-') and t and t[0].islower():
     compound = re.search(r'(four|agent|subject|highest|author|minded)-$',buf)
     buf=(buf if compound else buf[:-1])+t
    else:buf+=(' ' if buf else '')+t
    lastbottom=e[3]
   if buf:blocks.append(buf)
   page_blocks.append(blocks)
  # Pull title matter and footnote out into explicit source structure.
  title='Who is speaking when a Worker speaks?' if name=='audit' else 'How Faithfully Did the Press Transmit the Record?'
  page_blocks[0][0]=re.sub(r'^WHO IS SPEAKING WHEN A WORKER SPEAKS\?1\s*','',page_blocks[0][0]) if name=='audit' else re.sub(r'^HOW FAITHFULLY DID THE PRESS TRANSMIT THE RECORD\?\s*','',page_blocks[0][0])
  md=HEADER+f'# {title}\n\n> Derived reading edition of the supplied {len(doc.pages)}-page PDF. Paragraphs are reflowed; figures and tables are retained. The supplied PDF remains the authority. Project links have been added to this edition.\n\n'
  for pi,blocks in enumerate(page_blocks):md+=f'<!-- source-page: {pi+1} -->\n\n'+'\n\n'.join(blocks)+'\n\n'
  (ROOT/f'src/content/{name}.md').write_text(md)
# Standalone story download keeps every source line, with links added above it.
(ROOT/'src/assets/papers/tale.md').write_text(HEADER+(ROOT/'src/content/tale-source.md').read_text())
(ROOT/'qa/import-manifest.json').write_text(json.dumps(dict(researchHead='2e978808cc7f007a7dd07bf14d91249469ebe9c4',sources=records),indent=2))
print('Imported publications, figures, seven frozen tables and 23 chapter artworks.')
