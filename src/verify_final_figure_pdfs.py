from pathlib import Path
import subprocess
import json
from PIL import Image, ImageDraw

root=Path(__file__).resolve().parents[1]
poppler=Path('C:/Users/ALBERT/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin')
review=root/'outputs/final_visualizations/pdf_review'
review.mkdir(exist_ok=True)
pdfs=sorted((root/'figures/final').glob('figure*.pdf'))
assert len(pdfs)==10
results=[]
for pdf in pdfs:
    prefix=review/pdf.stem
    subprocess.run([str(poppler/'pdftoppm.exe'),'-singlefile','-scale-to','1600','-png',str(pdf),str(prefix)],check=True,capture_output=True)
    info=subprocess.run([str(poppler/'pdfinfo.exe'),str(pdf)],check=True,capture_output=True,text=True).stdout
    assert 'Pages:           1' in info
    with Image.open(prefix.with_suffix('.png')) as im:
        assert im.convert('RGBA').getchannel('A').getextrema()==(255,255)
        assert im.convert('RGB').getpixel((0,0))==(255,255,255)
    results.append({'pdf':pdf.name,'one_page':True,'rendered_successfully':True,'opaque_white_background':True})
sheet=Image.new('RGB',(1800,2800),'white')
for i,pdf in enumerate(pdfs):
    with Image.open((review/pdf.stem).with_suffix('.png')) as im:
        im.thumbnail((885,530)); x=(i%2)*900; y=(i//2)*560
        sheet.paste(im,(x,y+20)); ImageDraw.Draw(sheet).text((x+10,y+3),pdf.stem,fill='black')
sheet.save(review/'contact_sheet.jpg')
(review/'validation.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print('Ten one-page PDFs rendered and verified; contact sheet saved.')
