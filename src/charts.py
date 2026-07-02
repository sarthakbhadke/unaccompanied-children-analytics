import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

COLORS = {
    'hhs_blue'     : '#1f77b4',
    'cbp_orange'   : '#ff7f0e',
    'stress_red'   : '#d62728',
    'relief_green' : '#2ca02c',
    'neutral_gray' : '#7f7f7f',
    'backlog_purple': '#9467bd'
}

LAYOUT_DEFAULTS = dict(
    font       = dict(family='Arial, sans-serif', size=13),
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor  = 'rgba(0,0,0,0)',
    margin     = dict(l=40, r=40, t=60, b=40),
    hoverlabel = dict(bgcolor='white', font_size=13)
)

def chart_hhs_care_timeline(df, show_rolling=True):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['date'], y=df['hhs_in_care'],
        mode='lines', name='Daily HHS Care Load',
        line=dict(color=COLORS['hhs_blue'], width=1, dash='dot'),
        opacity=0.4
    ))
    if show_rolling:
        fig.add_trace(go.Scatter(
            x=df['date'], y=df['hhs_care_7day_avg'],
            mode='lines', name='7-Day Average',
            line=dict(color=COLORS['hhs_blue'], width=2.5)
        ))
    peak_date = df.loc[df['hhs_in_care'].idxmax(), 'date']
    peak_val  = df['hhs_in_care'].max()
    fig.add_annotation(
        x=peak_date, y=peak_val,
        text=f"Peak: {peak_val:,}",
        showarrow=True, arrowhead=2,
        arrowcolor=COLORS['stress_red'],
        font=dict(color=COLORS['stress_red'], size=12),
        yshift=10
    )
    fig.update_layout(
        **LAYOUT_DEFAULTS,
        title='HHS Care Load Over Time',
        xaxis_title='Date',
        yaxis_title='Children in HHS Care',
        hovermode='x unified',
        legend=dict(orientation='h', y=1.1),
        xaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0')
    )
    return fig

def chart_cbp_vs_hhs(df):
    fig = make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Scatter(
        x=df['date'], y=df['cbp_in_custody'],
        name='CBP Custody',
        line=dict(color=COLORS['cbp_orange'], width=2)
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=df['date'], y=df['hhs_in_care'],
        name='HHS Care',
        line=dict(color=COLORS['hhs_blue'], width=2)
    ), secondary_y=True)
    fig.update_layout(
        **LAYOUT_DEFAULTS,
        title='CBP Custody vs HHS Care Load',
        hovermode='x unified',
        legend=dict(orientation='h', y=1.1)
    )
    fig.update_yaxes(title_text='Children in CBP Custody', secondary_y=False)
    fig.update_yaxes(title_text='Children in HHS Care',    secondary_y=True)
    return fig

def chart_net_intake_monthly(monthly):
    colors = [
        COLORS['stress_red'] if val > 0 else COLORS['relief_green']
        for val in monthly['net_intake_total']
    ]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=monthly['month_label'],
        y=monthly['net_intake_total'],
        marker_color=colors,
        name='Net Intake'
    ))
    fig.add_hline(
        y=0, line_dash='dash',
        line_color=COLORS['neutral_gray'],
        annotation_text='Balance point'
    )
    fig.update_layout(
        **LAYOUT_DEFAULTS,
        title='Monthly Net Intake (Transfers − Discharges)',
        xaxis_title='Month',
        yaxis_title='Net Children',
        xaxis=dict(tickangle=-45)
    )
    return fig

def chart_system_load_area(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['date'], y=df['hhs_in_care'],
        name='HHS Care', fill='tozeroy', mode='lines',
        line=dict(color=COLORS['hhs_blue'], width=1),
        fillcolor='rgba(31, 119, 180, 0.3)'
    ))
    fig.add_trace(go.Scatter(
        x=df['date'], y=df['cbp_in_custody'],
        name='CBP Custody', fill='tozeroy', mode='lines',
        line=dict(color=COLORS['cbp_orange'], width=1),
        fillcolor='rgba(255, 127, 14, 0.3)'
    ))
    fig.update_layout(
        **LAYOUT_DEFAULTS,
        title='Total System Load — CBP + HHS',
        xaxis_title='Date',
        yaxis_title='Children',
        hovermode='x unified',
        legend=dict(orientation='h', y=1.1)
    )
    return fig

def chart_monthly_avg_bar(monthly):
    fig = px.bar(
        monthly, x='avg_hhs_care', y='month_label',
        orientation='h',
        color='avg_hhs_care',
        color_continuous_scale='RdYlGn_r',
        labels={
            'avg_hhs_care': 'Avg Children in HHS Care',
            'month_label' : 'Month'
        },
        title='Average Monthly HHS Care Load'
    )
    fig.update_layout(
        **LAYOUT_DEFAULTS,
        yaxis=dict(autorange='reversed'),
        coloraxis_showscale=False
    )
    return fig

def chart_cumulative_backlog(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['date'], y=df['cumulative_backlog'],
        mode='lines', name='Cumulative Backlog',
        line=dict(color=COLORS['backlog_purple'], width=2),
        fill='tozeroy',
        fillcolor='rgba(148, 103, 189, 0.2)'
    ))
    fig.add_hline(y=0, line_dash='dash', line_color=COLORS['neutral_gray'])
    fig.update_layout(
        **LAYOUT_DEFAULTS,
        title='Cumulative Net Intake Over Time',
        xaxis_title='Date',
        yaxis_title='Cumulative Net Children',
        hovermode='x unified'
    )
    return fig