from pathlib import Path
import nbformat
from nbclient import NotebookClient
from PIL import Image, ImageOps, ImageDraw

root = Path(__file__).resolve().parents[1]
s = (root / 'src/supporting_data_analysis.py').read_text(encoding='utf-8')
s = s.replace('ROOT = Path(__file__).resolve().parents[1]', "ROOT = Path.cwd() if (Path.cwd() / 'data/raw').is_dir() else Path.cwd().parent")
anchors = [('ai = load(', 'AI-chip cleaning and EDA'), ('prices = load(', 'Monthly price cleaning and EDA'), ('fab = load(', 'Capacity cleaning and EDA'), ('events = load(', 'Policy-event cleaning and EDA'), ('financials = pd.read_csv(', 'Financial links and coverage'), ('plt.rcParams.update(', 'Visualization'), ('assert all(hashlib.sha256', 'Validation and results')]
bounds = [(0, 'Setup and audit')] + [(s.index(a),h) for a,h in anchors] + [(len(s),'')]
cells = [nbformat.v4.new_markdown_cell('# Supporting datasets: cleaning and EDA\n\nUses the three project periods. Numeric source values are preserved. See outputs/supporting_data_eda/RESULTS.md for interpretation limits.')]
for (start,heading),(end,_) in zip(bounds,bounds[1:]):
    cells += [nbformat.v4.new_markdown_cell('## '+heading),nbformat.v4.new_code_cell(s[start:end])]
cells.append(nbformat.v4.new_code_cell('from IPython.display import display, Image\nfor name in ["period_coverage", "ai_annual", "price_coverage", "review_flags"]:\n    print(name)\n    display(tables[name])\nfor path in chart_files:\n    display(Image(filename=str(path)))'))
nb = nbformat.v4.new_notebook(cells=cells)
path=root/'notebooks/06_supporting_data_eda.ipynb'
nbformat.write(nb,path)
NotebookClient(nb,timeout=180,kernel_name='python3',resources={'metadata':{'path':str(root)}}).execute()
nbformat.write(nb,path)
images=sorted((root/'outputs/supporting_data_eda/figures').glob('*.png'))
sheet=Image.new('RGB',(1600,2000),'white')
for i,p in enumerate(images):
    im=Image.open(p); im.thumbnail((780,475))
    x=(i%2)*800; y=(i//2)*500
    sheet.paste(im,(x,y+20))
    ImageDraw.Draw(sheet).text((x+10,y+3),p.stem,fill='black')
sheet.save(root/'outputs/supporting_data_eda/chart_review.jpg')
print('Notebook executed; chart review generated.')
