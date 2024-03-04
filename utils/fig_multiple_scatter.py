import plotly.express as px
import pandas as pd


def serve_fig_multiple_scatter(df, freq, title):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.groupby([pd.Grouper(key='timestamp', freq=freq), pd.Grouper('variable')]).mean()
    df = df.reset_index()

    fig = px.scatter(df, x="timestamp", y="value")

    fig.update_traces(marker_color='rgb(102, 178, 255,0.05)', marker_size=3)

    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=16),
            automargin=True,
            yref='container',
            x=0.05,
            y=0.95,
        ),
        margin=dict(
            l=40,
            r=40,
            b=40,
            t=40
        ),
        yaxis={
            'title': None,
            'linecolor': "#D3D3D3",
            # 'ticklabelposition': 'inside',
            'showgrid': False
        },
        xaxis={
            'title': None,
            'linecolor': "#D3D3D3",
            # 'ticklabelposition': 'inside',
            'showgrid': False
        },
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
        hoverlabel=dict(
            bgcolor='rgba(0,0,0,.9)',
            font_size=16,
            font_family="Rockwell"
        ),
    )
    return fig
