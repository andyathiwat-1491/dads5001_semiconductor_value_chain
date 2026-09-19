"""Build and execute the final presentation notebook in README figure order.

Run: python src/build_final_visualizations.py
Figure 1 is the supplied process illustration; Figures 2-13 are reproducible.
"""
from pathlib import Path
import csv
import json
import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
FIGURES = [
    (1, 'IC assembly process', None, 'IC_assembly_process'),
    (2, 'Country and business model', 'visualize_country_figure2.py', 'figure2_country_business_map'),
    (3, 'Profitability by business model', 'visualize_profitability_bar_figure3.py', 'figure3_profitability_bar_chart'),
    (4, 'Revenue and company coverage', 'visualize_revenue_figure4.py', 'figure4_financial_revenue_coverage'),
    (5, 'Memory price divergence', 'visualize_memory_prices_figure5.py', 'figure5_memory_price_divergence'),
    (6, 'Value-chain revenue decline', 'visualize_section2_figures.py', 'figure6_value_chain_revenue_decline'),
    (7, 'IDM segment revenue change', None, 'figure7_idm_segment_change'),
    (8, 'Export controls comparison', None, 'figure8_export_controls_test'),
    (9, 'DRAM capacity and price', None, 'figure9_dram_capacity_vs_price'),
    (10, 'Illustrative supply and demand mechanism', None, 'figure10_supply_demand_mechanism'),
    (11, 'Revenue share by value chain', 'visualize_value_chain_figure11.py', 'figure11_value_chain_revenue_share'),
    (12, 'Top three companies by revenue', 'visualize_top3_figures12_13.py', 'figure12_top3_revenue'),
    (13, 'Top three revenue spotlight on 2023', None, 'figure13_top3_revenue_2023'),
]


def write_manifest():
    out = ROOT / 'outputs/final_visualizations'
    out.mkdir(parents=True, exist_ok=True)
    records = []
    for number, title, script, stem in FIGURES:
        for extension in (('png',) if number == 1 else ('png', 'svg') if number in (2, 5) else ('png', 'pdf')):
            path = ROOT / 'figures/final' / f'{stem}.{extension}'
            assert path.is_file(), path
            records.append({'figure': number, 'title': title, 'format': extension, 'file': path.relative_to(ROOT).as_posix()})
    with (out / 'saved_outputs.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
    (out / 'validation.json').write_text(json.dumps({'figures': 13, 'png_files': 13, 'pdf_files': 10, 'svg_files': 2, 'notebook_executed': True}, indent=2), encoding='utf-8')
    report = '# Final presentation figures\n\nRebuild with `python src/build_final_visualizations.py`.\n\nFigure 1 is the supplied illustration. Figures 2–5 retain the current project analyses; Figures 6–10 use the imported Ozone script.\n\n'
    report += 'Figures 11-13 use the updated Best contribution.\n\n'
    report += '\n'.join(f'- Figure {number}: {title}' for number, title, _, _ in FIGURES)
    (out / 'RESULTS.md').write_text(report + '\n', encoding='utf-8')


def main():
    cells = [nbformat.v4.new_markdown_cell('# Final presentation: Figures 1-13\n\nMatches README.md. Figures 6-10 use the supplied Ozone plotting code; Figures 11-13 use the updated Best contribution. Figure 1 is an existing illustration.')]
    cells.append(nbformat.v4.new_code_cell("from pathlib import Path\nimport subprocess\nimport sys\nfrom IPython.display import Image, display\nROOT = Path.cwd() if (Path.cwd() / 'data/raw').is_dir() else Path.cwd().parent"))
    for number, title, script, stem in FIGURES:
        cells.append(nbformat.v4.new_markdown_cell(f'## Figure {number} - {title}'))
        code = ''
        if script:
            code = f"subprocess.run([sys.executable, str(ROOT / 'src' / {script!r})], cwd=ROOT, check=True)\n"
        code += f"display(Image(filename=str(ROOT / 'figures/final' / {stem + '.png'!r}), width=1000))"
        cells.append(nbformat.v4.new_code_cell(code))
    notebook = nbformat.v4.new_notebook(cells=cells, metadata={'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}})
    path = ROOT / 'notebooks/07_final_presentation_visualizations.ipynb'
    nbformat.write(notebook, path)
    NotebookClient(notebook, timeout=240, kernel_name='python3', resources={'metadata': {'path': str(ROOT)}}).execute()
    nbformat.write(notebook, path)
    write_manifest()
    print('Executed:', path)


if __name__ == '__main__':
    main()
