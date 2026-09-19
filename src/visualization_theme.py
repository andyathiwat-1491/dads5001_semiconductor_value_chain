"""Shared semantic colors and presentation styling for final Figures 2-13."""
import matplotlib as mpl
from matplotlib.text import Text

BUSINESS_COLORS = {
    "Foundry": "#168C86", "Fabless": "#3974B9", "IDM": "#C36B30",
    "Equipment": "#865BB1", "EDA Software": "#BD5084",
}
PRODUCT_COLORS = {"DRAM_DDR4_8Gb": "#204E70", "NAND_64Gb_MLC": "#C36B30", "HBM3_stack": "#168C86"}
COMPANY_COLORS = {
    "NVIDIA": "#3974B9", "Qualcomm": "#244B79", "TSMC": "#168C86",
    "Intel": "#87421D", "Samsung Memory": "#C36B30", "SK Hynix": "#A17A19",
    "Texas Instruments": "#765447", "Other": "#94A3B8",
}
PERIOD_COLORS = {"pre_ai": "#3974B9", "transition": "#C36B30", "ai": "#168C86"}
TEXT = "#1D3543"
MUTED = "#52636D"
GRID = "#E3E7EB"
BORDER = "#BAC2C9"
POSITIVE = "#168C86"
NEGATIVE = "#B3261E"
NEUTRAL = "#94A3B8"
CAPACITY = "#B9CFDF"
TITLE_SIZE = 16
PANEL_TITLE_SIZE = 12

def apply_theme():
    mpl.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 10,
        "text.color": TEXT, "axes.labelcolor": TEXT, "axes.titlecolor": TEXT,
        "axes.titlesize": PANEL_TITLE_SIZE, "axes.titleweight": "bold", "axes.titlelocation": "left", "axes.labelsize": 11,
        "xtick.labelsize": 10, "ytick.labelsize": 10,
        "xtick.color": MUTED, "ytick.color": MUTED,
        "axes.edgecolor": BORDER, "axes.linewidth": .8,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.axisbelow": True, "axes.grid": False,
        "grid.color": GRID, "grid.linewidth": .7, "grid.linestyle": "-",
        "legend.fontsize": 10, "legend.frameon": False,
        "figure.facecolor": "white", "axes.facecolor": "white",
        "savefig.facecolor": "white", "savefig.dpi": 300,
        "pdf.fonttype": 42, "svg.fonttype": "none",
        "lines.linewidth": 2.2,
        "axes.prop_cycle": mpl.cycler(color=list(BUSINESS_COLORS.values())),
    })

def finalize_figure(fig):
    """Apply a width-scaled type hierarchy before exporting; safe to call twice.

    Titles match Figure 5: 16 pt at 18 inches wide, scaled by canvas width.
    Panel headings use 12 pt at 18 inches wide; all headings are left aligned.
    Other sizes at 16 inches: labels 12, body 10, compact 8.
    Dense annotations keep the compact tier; twin-axis color cues are preserved.
    """
    if getattr(fig, "_shared_theme_applied", False):
        return
    scale = fig.get_figwidth() / 16
    title_scale = fig.get_figwidth() / 18
    for text in fig.findobj(Text):
        size = text.get_fontsize()
        text.set_fontfamily("DejaVu Sans")
        tier = 8 if size < 9 else 10 if size < 12 else 12 if size < 15 else 14
        text.set_fontsize(tier * scale)
        if text.get_fontweight() in ("heavy", "black"):
            text.set_fontweight("bold")
    for ax in fig.axes:
        for title in (ax.title, ax._left_title, ax._right_title):
            if title.get_text():
                title.set_fontsize((TITLE_SIZE if title.get_text().lower().startswith("figure") else PANEL_TITLE_SIZE) * title_scale)
                title.set_horizontalalignment("left")
                title.set_x((0.04 - ax.get_position().x0) / ax.get_position().width
                            if title.get_text().lower().startswith("figure") else 0)
                title.set_fontweight("bold")
                title.set_color(TEXT)
        for label in (ax.xaxis.label, ax.yaxis.label):
            label.set_fontsize(12 * scale)
        for tick in ax.get_xticklabels() + ax.get_yticklabels():
            tick.set_fontsize(10 * scale)
        for line in ax.get_xgridlines() + ax.get_ygridlines():
            line.set_color(GRID)
            line.set_linewidth(.7)
            line.set_linestyle("-")
            line.set_alpha(1)
        for spine in ax.spines.values():
            spine.set_color(BORDER)
            spine.set_linewidth(.8)
        legend = ax.get_legend()
        if legend:
            for text in legend.get_texts():
                text.set_fontsize(10 * scale)
            legend.get_frame().set_edgecolor(BORDER)
            legend.get_frame().set_facecolor("white")
    for text in fig.texts:
        value = text.get_text().strip()
        if (value.lower().startswith("figure") and len(value) > 12) or value == "Semiconductor Industry Landscape by Country/Region":
            text.set_fontsize(TITLE_SIZE * title_scale)
            text.set_x(0.04)
            text.set_horizontalalignment("left")
            text.set_fontweight("bold")
            text.set_color(TEXT)
    fig._shared_theme_applied = True
