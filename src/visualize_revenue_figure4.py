"""Figure 4: retain the project's revenue and coverage chart."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from visualization_theme import (BUSINESS_COLORS, PRODUCT_COLORS, COMPANY_COLORS,
    PERIOD_COLORS, TEXT, MUTED, POSITIVE, NEGATIVE, NEUTRAL, CAPACITY,
    apply_theme, finalize_figure)
apply_theme()
from matplotlib.ticker import StrMethodFormatter
from matplotlib.patches import Patch
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / 'figures/final'
OUT = ROOT / 'outputs/final_visualizations'
FIG.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

def save(fig, number, slug, title, subtitle, note, maximum_year):
    fig.text(.065,.972,f'FIGURE {number}  |  {title}',ha='left',va='top',fontsize=14,fontweight='bold',color=TEXT)
    fig.text(.065,.927,subtitle,ha='left',va='top',fontsize=11.5,color=MUTED)
    fig.subplots_adjust(left=.12,right=.96,bottom=.10,top=.83,hspace=.12)
    for ext in ('png','pdf'):
        finalize_figure(fig)
        fig.savefig(FIG/f'figure4_{slug}.{ext}',dpi=300,facecolor='white',transparent=False)
    plt.close(fig)

financials = pd.read_csv(ROOT/'data/processed/financials_features.csv')
assert not financials.duplicated(['company_name','year']).any()
trend = financials.loc[financials.year.between(2010,2025)].groupby('year',as_index=False).agg(revenue_usd_bn=('revenue_usd_bn','sum'),entities=('company_name','nunique'))
trend['yoy_pct'] = trend.revenue_usd_bn.pct_change(fill_method=None)*100
trend.to_csv(OUT/'figure_04_inputs.csv',index=False)

fig,(top,bottom)=plt.subplots(2,1,figsize=(14,8.4),sharex=True,gridspec_kw={'height_ratios':[5.3,0.85],'hspace':0.12})
periods=[(2009.7,2021.5,'#E8F0FA','Smart Automobile Expansion (2010-2021)'),(2021.5,2022.5,'#FBEBDD','Transition Year (2022)'),(2022.5,2025.3,'#DDF3EF','AI Expansion (2023-2025)')]
for ax in (top,bottom):
    for lo,hi,color,_ in periods: ax.axvspan(lo,hi,color=color,zorder=0)
    ax.set_axisbelow(True)
    ax.grid(axis='y',color='#DDE6EB',linewidth=.65)
    ax.spines[['top','right']].set_visible(False)
    ax.spines[['left','bottom']].set_color('#B9C5CD')
    ax.tick_params(colors='#344655',labelsize=9.5)
era_colors = ['#3974b9' if year <= 2021 else '#c36b30' if year == 2022 else '#168c86' for year in trend.year]
for i in range(1,len(trend)):
    top.plot(trend.year.iloc[i-1:i+1],trend.revenue_usd_bn.iloc[i-1:i+1],color=era_colors[i],lw=3,zorder=3)
top.fill_between(trend.year,trend.revenue_usd_bn,color='#3974b9',alpha=.08,zorder=1)
top.scatter(trend.year,trend.revenue_usd_bn,s=36,color=era_colors,edgecolor='white',linewidth=.6,zorder=4)
key_years={2010,2022,2025}
for row in trend.itertuples():
    key=row.year in key_years
    label=f'${row.revenue_usd_bn:,.2f}B' if key else f'${row.revenue_usd_bn:,.1f}B'
    top.annotate(label,(row.year,row.revenue_usd_bn),xytext=(10 if row.year in (2023,2024) else 0,-12 if row.year in (2023,2024) else (11 if key else 8)),textcoords='offset points',ha='center',va='top' if row.year in (2023,2024) else 'bottom',fontsize=10.1 if key else 8.1,fontweight='bold' if key else 'normal',color='#173F5D' if key else '#526B7C',bbox={'boxstyle':'square,pad=.35','facecolor':'white','edgecolor':'#D62828','linewidth':1.7} if row.year == 2023 else None,zorder=6)
    if key: top.scatter([row.year],[row.revenue_usd_bn],s=68,color=era_colors[row.Index],edgecolor='white',linewidth=1.2,zorder=5)
auto_peak=trend.loc[trend.year.between(2011,2021)].nlargest(1,'yoy_pct').iloc[0]
ai_peak=trend.loc[trend.year.between(2023,2025)].nlargest(1,'yoy_pct').iloc[0]
peak_text=(f'Peak annual revenue growth (YoY)\n'
           f'Automobile era: {auto_peak.yoy_pct:.2f}% ({int(auto_peak.year)-1}-{int(auto_peak.year)})   |   AI era: {ai_peak.yoy_pct:.2f}% ({int(ai_peak.year)-1}-{int(ai_peak.year)})')
top.text(.53,.97,peak_text,transform=top.transAxes,ha='left',va='top',fontsize=9.3,color='#294B62',linespacing=1.5,bbox={'facecolor':'white','edgecolor':'#DCE5E9','boxstyle':'round,pad=.6','alpha':.92})
top.set_ylim(0,1180)
top.set_xlabel('Year'); top.xaxis.label.set_visible(False)
top.set_ylabel('Total Revenue of Represented Companies (USD billions)',fontsize=10.7,color='#263C4D',labelpad=10)
top.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
top.legend(handles=[Patch(facecolor=color,edgecolor='#DFE5E9',label=label) for _,_,color,label in periods],loc='upper left',frameon=False,fontsize=8.6)
bottom.step(trend.year,trend.entities,where='post',color='#865bb1',linewidth=2.2,zorder=3)
bottom.scatter(trend.year,trend.entities,s=16,color='#865bb1',zorder=4)
for row in trend.itertuples():
    if row.year==2010 or row.year==2025 or (row.year>2010 and row.entities!=int(trend.loc[trend.year.eq(row.year-1),'entities'].iloc[0])):
        bottom.annotate(str(row.entities),(row.year,row.entities),xytext=(0,6),textcoords='offset points',ha='center',va='bottom',fontsize=8.4,color='#355268')
bottom.set_ylim(29,44); bottom.set_yticks([30,35,40]); bottom.set_xticks(trend.year); bottom.set_xlim(2009.6,2025.5)
bottom.set_ylabel('Companies',fontsize=9.5,color='#263C4D',labelpad=10); bottom.set_xlabel('Year',fontsize=9.5,color='#263C4D')
bottom.text(2020.1,31.0,'40 companies from 2020 through 2025',fontsize=8.6,color='#355268')
save(fig,4,'financial_revenue_coverage','Represented Company Revenue Reached $1.01 Trillion in 2025','Annual revenue and represented company coverage, 2010-2025','The totals represent the companies included in the dataset and do not represent total global semiconductor industry revenue. Period labels show time intervals, not causes.',2025)
