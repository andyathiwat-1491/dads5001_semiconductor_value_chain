# Final visualization theme

Figures 2-13 and notebook 07 use `src/visualization_theme.py`. Rebuild with `python src/build_final_visualizations.py` from the project directory. Figure 1 is a supplied raster illustration and retains its original artwork. Historical EDA notebooks and archived outputs are outside this final-presentation theme.

## Semantic colors

| Business model | Color |
|---|---|
| Foundry | Teal `#168C86` |
| Fabless | Blue `#3974B9` |
| IDM | Orange `#C36B30` |
| Equipment | Purple `#865BB1` |
| EDA Software | Rose `#BD5084` |

| Product | Color |
|---|---|
| DRAM DDR4 8Gb | Dark blue `#204E70` |
| NAND 64Gb MLC | Orange `#C36B30` |
| HBM3 | Teal `#168C86` |

Company colors are stable in Figures 12-13, using business-related hues: NVIDIA blue, TSMC teal, and separate brown/orange/ochre shades for Intel, Samsung Memory and SK Hynix. Company and business legends explicitly identify their different levels of detail.

Periods: pre-AI blue, transition orange, AI teal. Direction: negative red, positive teal. Policy exposure: targeted red, non-targeted slate. These are separate encodings and retain explicit labels/legends; Figure 3 colors encode periods, not businesses. Figure 5 bars encode products, with signed change labels. DRAM capacity uses pale blue bars and DRAM price a dark blue line. Figure 13 deliberately fades non-2023 bars to preserve the spotlight.

## Typography and surfaces

DejaVu Sans throughout. Main titles match Figure 5: 16 pt at an 18-inch canvas width, scaled proportionally with figure width so titles have the same apparent size when displayed at equal widths. Panel titles use the same scaling from 12 pt. All titles are left aligned. Main titles start at 4% of the figure width, independent of axis-label spacing. Other sizes scale with canvas width: at 16 inches, axis labels 12 pt, body/ticks/legends 10 pt, compact labels 8 pt. Dense map cards and stacked bars use compact labels. White backgrounds, navy text, muted secondary text, light gray gridlines and borders. PNG exports are 300 dpi (the detailed country map retains 220 dpi); PDF text is embedded and SVG text remains editable.

All data aggregation, values, time windows and chart-specific analytical emphasis are preserved. The shared finalization helper applies typography before each export. Extend the semantic palettes here rather than assigning new ad hoc colors in individual figures.
