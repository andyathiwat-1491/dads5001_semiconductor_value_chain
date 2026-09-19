"""Period medians calculated directly from valid company-year observations."""
from pathlib import Path
import hashlib
import json
import subprocess
import textwrap
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from visualization_theme import (BUSINESS_COLORS, PRODUCT_COLORS, COMPANY_COLORS,
    PERIOD_COLORS, TEXT, MUTED, POSITIVE, NEGATIVE, NEUTRAL, CAPACITY,
    apply_theme, finalize_figure)
apply_theme()

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'data/processed/financials_features.csv'
OUT = ROOT/'outputs/final_visualizations'
FIG = ROOT/'figures/final/figure3_profitability_bar_chart'
PERIODS = [('2015-2021',2015,2021,'Smart automobile expansion',PERIOD_COLORS["pre_ai"]),
           ('2022',2022,2022,'Transition Year',PERIOD_COLORS["transition"]),
           ('2023-2025',2023,2025,'AI Expansion period',PERIOD_COLORS["ai"])]


def main():
    digest=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    data=pd.read_csv(SOURCE)
    assert {'company_name','year','value_chain_group','revenue_usd_bn','operating_income_usd_bn'}.issubset(data)
    numeric=['year','revenue_usd_bn','operating_income_usd_bn']
    existing='operating_margin_pct' in data
    if existing: numeric.append('operating_margin_pct')
    invalid={}
    for col in numeric:
        converted=pd.to_numeric(data[col],errors='coerce')
        invalid[col]=int((data[col].notna() & converted.isna()).sum())
        data[col]=converted.replace([np.inf,-np.inf],np.nan)
    rows=data.loc[data.year.between(2015,2025)].copy()
    assert not rows.duplicated(['company_name','year']).any()
    assert rows[['company_name','value_chain_group']].notna().all().all()
    if not existing:
        rows['operating_margin_pct']=rows.operating_income_usd_bn.div(rows.revenue_usd_bn.where(rows.revenue_usd_bn.gt(0)))*100
    valid=rows[['revenue_usd_bn','operating_income_usd_bn','operating_margin_pct']].notna().all(axis=1) & rows.revenue_usd_bn.gt(0)
    clean=rows.loc[valid].copy()
    clean['extreme_flag']=False
    for group,g in clean.groupby('value_chain_group'):
        q1,q3=g.operating_margin_pct.quantile([.25,.75])
        clean.loc[g.index,'extreme_flag']=(g.operating_margin_pct.lt(q1-1.5*(q3-q1)) | g.operating_margin_pct.gt(q3+1.5*(q3-q1)))
    overall=clean.groupby('value_chain_group').operating_margin_pct.median().sort_values(ascending=False)
    assert set(overall.index)=={'Foundry','Fabless','IDM','Equipment','EDA Software'}
    records=[]
    for group in overall.index:
        for period,start,end,_,_ in PERIODS:
            represented=rows.loc[rows.value_chain_group.eq(group) & rows.year.between(start,end)]
            g=clean.loc[clean.value_chain_group.eq(group) & clean.year.between(start,end)]
            records.append({'group':group,'period':period,'companies':represented.company_name.nunique(),
                            'valid_companies':g.company_name.nunique(),'valid_observations':len(g),
                            'median_operating_margin':g.operating_margin_pct.median(),
                            'weighted_operating_margin':g.operating_income_usd_bn.sum()/g.revenue_usd_bn.sum()*100,
                            'company_year_iqr':g.operating_margin_pct.quantile(.75)-g.operating_margin_pct.quantile(.25)})
    table=pd.DataFrame(records)
    med=table.pivot(index='group',columns='period',values='median_operating_margin').reindex(overall.index)
    change=med['2023-2025']-med['2022']
    largest=change.abs().idxmax()
    leader=overall.index[0]
    stability=med.max(axis=1)-med.min(axis=1)
    stable=stability.idxmin()
    validation={'source_unchanged':True,'source_sha256':digest,'duplicate_company_years':0,
                'margin_field':'operating_margin_pct','existing_margin_used':existing,
                'invalid_numeric_conversions_full_file':invalid,
                'missing_values_in_window':rows[['revenue_usd_bn','operating_income_usd_bn','operating_margin_pct']].isna().sum().to_dict(),
                'nonpositive_revenue_flagged':int(rows.revenue_usd_bn.le(0).sum()),
                'excluded_observations':int((~valid).sum()),'valid_observations':len(clean),
                'negative_margins_retained':int(clean.operating_margin_pct.lt(0).sum()),
                'extreme_observations_flagged_and_retained':int(clean.extreme_flag.sum()),
                'extreme_rule':'Pooled within-group 1.5-IQR fences',
                'weighted_formula':'sum(operating_income_usd_bn) / sum(revenue_usd_bn) * 100',
                'change_comparison':'2023-2025 period median minus 2022 period median, percentage points'}
    cols=['group','period','companies','valid_observations','median_operating_margin']
    print('PERIOD VALIDATION\n'+table[cols].round(3).to_string(index=False))
    print('\nREVENUE-WEIGHTED ROBUSTNESS\n'+table[['group','period','weighted_operating_margin']].round(3).to_string(index=False))
    print('\nLIMITATIONS\n'+json.dumps(validation,indent=2))
    print('EDA coverage is two companies. Eight zero-revenue rows are excluded; extremes are retained. Periods have unequal lengths and changing company coverage.')
    OUT.mkdir(parents=True,exist_ok=True)
    table.to_csv(OUT/'figure_03_bar_period_validation.csv',index=False)
    table[['group','period','weighted_operating_margin']].to_csv(OUT/'figure_03_bar_weighted_margins.csv',index=False)
    rows.loc[~valid].to_csv(OUT/'figure_03_bar_excluded_observations.csv',index=False)
    clean.loc[clean.extreme_flag].to_csv(OUT/'figure_03_bar_extreme_observations.csv',index=False)
    navy,grey=TEXT,MUTED
    fig=plt.figure(figsize=(18,10),facecolor='white')
    fig.text(.06,.957,'FIGURE 3 | Profitability Varied Across Semiconductor Business Models, 2015-2025',fontsize=21,weight='bold',color=navy,va='top')
    fig.text(.06,.906,'Median company operating margin across three industry periods',fontsize=14,color=grey)
    takeaway=(f'{leader} had the highest eleven-year median ({overall.loc[leader]:.1f}%); {largest} changed most in 2023-2025 '
              f'({change.loc[largest]:+.2f} percentage points versus 2022).')
    fig.text(.06,.86,takeaway,fontsize=12.5,weight='bold',color=PERIOD_COLORS["ai"])
    ax=fig.add_axes([.08,.31,.87,.45])
    x=np.arange(len(overall));width=.235
    for i,(period,_,_,description,color) in enumerate(PERIODS):
        values=med[period]
        bars=ax.bar(x+(i-1)*width,values,width=width,color=color,label=f'{period} ({description})',zorder=3)
        for rect,value in zip(bars,values):
            ax.annotate(f'{value:.1f}%',(rect.get_x()+rect.get_width()/2,value),xytext=(0,7 if value>=0 else -7),
                        textcoords='offset points',ha='center',va='bottom' if value>=0 else 'top',fontsize=11.5,weight='bold',color=navy)
    ax.axhline(0,color='#7D909B',lw=1)
    ax.set_ylim(min(0,med.min().min())-1,max(0,med.max().max())+7)
    ax.set_xticks(x,overall.index,fontsize=13)
    ax.tick_params(axis='x',length=0,pad=12)
    ax.set_ylabel('Median operating margin (%)',color=navy,labelpad=12)
    ax.grid(axis='y',color='#E3E7EB',lw=.7);ax.set_axisbelow(True)
    ax.spines[['left','bottom']].set_color('#BAC2C9')
    ax.tick_params(colors=grey)
    ax.legend(loc='lower left',bbox_to_anchor=(-.01,1.055),ncol=3,frameon=False,fontsize=10.5,handlelength=1.4,columnspacing=2)
    for i,group in enumerate(overall.index):
        cells=table.loc[table.group.eq(group)]
        label=' | '.join(f'{r.companies}/{r.valid_observations}' for r in cells.itertuples())
        ax.text(i,-.12,label,transform=ax.get_xaxis_transform(),ha='center',va='top',fontsize=10,color=grey)
    fig.text(.08,.215,'Coverage: represented companies / valid company-year observations, in period order: 2015-2021 | 2022 | 2023-2025.',fontsize=10,color=grey)
    note='Note: Bars show the median operating margin across valid company-year observations within each period. Operating margin is operating income divided by revenue. Results describe represented companies only and may be influenced by company composition, product mix, accounting practices, and limited coverage in smaller groups.'
    fig.text(.06,.158,textwrap.fill(note,160),fontsize=10.5,color=grey,va='top',linespacing=1.5)
    finalize_figure(fig)
    fig.canvas.draw()
    for t in fig.texts:
        b=t.get_window_extent(fig.canvas.get_renderer())
        assert b.x0>=0 and b.x1<=fig.bbox.width and b.y0>=0 and b.y1<=fig.bbox.height,t.get_text()
    for ext in ('png','pdf'):
        temporary=FIG.with_name(FIG.name+'_temp').with_suffix('.'+ext)
        finalize_figure(fig)
        fig.savefig(temporary,dpi=300,facecolor='white')
        temporary.replace(FIG.with_suffix('.'+ext))
    plt.close(fig)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==digest
    (OUT/'figure_03_bar_validation.json').write_text(json.dumps(validation,indent=2),encoding='utf-8')
    weighted=table.pivot(index='group',columns='period',values='weighted_operating_margin')
    report=['# Figure 3: profitability across three periods','',takeaway,'',
            'Operating margin measures the proportion of revenue remaining after operating expenses, before interest and taxes. Higher margin indicates greater operating profitability per revenue dollar, not necessarily the largest absolute operating profit.',
            'Existing operating_margin_pct is used for company medians. revenue_usd_bn and operating_income_usd_bn are used for validity checks and revenue weighting. Supplied margins are retained rather than reconstructed from rounded dollar amounts. Each bar is the direct median of all valid company-year observations in the period, not an average of annual medians.',
            f'{leader} leads the overall pooled eleven-year median. {stable} has the smallest range across the three period medians ({stability.loc[stable]:.2f} percentage points). This is stability of period medians, not proof of company-level or annual stability.',
            f'The largest absolute change is {largest}: {change.loc[largest]:+.2f} percentage points from 2022 to 2023-2025. These pooled-period comparisons do not isolate the 2023 downturn from the 2024-2025 recovery.',
            'Weighted margin leaders by period: '+ '; '.join(f'{period}: {weighted[period].idxmax()} ({weighted[period].max():.2f}%)' for period, *_ in PERIODS)+'. Weighting favors larger firms and can change rankings.',
            f'The dataset has no missing revenue or operating-income values in this window and no duplicate company-years. Eight zero-revenue rows are flagged and excluded. There are no negative margins among valid observations. {int(clean.extreme_flag.sum())} within-group IQR extremes are flagged and retained.',
            'EDA Software has only two companies in each period. Group composition and observation counts differ across periods. Company-year pooling gives more weight to companies with more observed years. Period medians are descriptive, not global industry estimates or evidence that business models caused the differences.',
            '', '## Validation table','',table[cols].round(3).to_markdown(index=False),
            '', '## Weighted robustness table','',table[['group','period','weighted_operating_margin']].round(3).to_markdown(index=False),
            '', '## Dispersion and coverage','',table.round(3).to_markdown(index=False)]
    (OUT/'figure_03_bar_findings.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
    poppler=Path('C:/Users/ALBERT/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe')
    subprocess.run([str(poppler),'-singlefile','-scale-to','2000','-png',str(FIG.with_suffix('.pdf')),str(OUT/'pdf_review/figure3_profitability_bar_chart')],check=True)
    print(takeaway)
    print(f'Most stable period medians: {stable}, range {stability.loc[stable]:.2f} pp')


if __name__=='__main__':
    main()
