import plotly.express as px
import pandas as pd
from dash import html, dcc


def serve_fig_price_curve():
    df = pd.read_csv("./data/es_demand_price.csv", delimiter=';')

    df['date'] = pd.to_datetime(df['date'])

    start_date_train = "2018-01-01"
    finish_date_train = "2019-01-01"


    df = df.loc[(df['date'] > start_date_train) & (df['date'] <= finish_date_train)]

    fig = px.line(df, x='date', y="DayAheadPrices_ES")
    fig.update_layout(
        title=dict(
            text="Demand curve",
            font=dict(size=20),
            automargin=True,
            yref='container',
            x=0.5,
            y=0.95,
        ),
        margin=dict(
            l=20,
            r=20,
            b=20,
            t=0
        ),
        yaxis={
            # 'ticklabelposition': 'inside',
            'showgrid': False
        },
        xaxis={
            # 'ticklabelposition': 'inside',
            'showgrid': False
        },
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        # autosize=True,
        legend={
            'visible': False
        },
        hoverlabel=dict(
            bgcolor='rgba(0,0,0,.9)',
            # font_size=16,
            font_family="Roboto"
        ),
    )

    # fig.update_xaxes(
    #     rangeslider_visible=False,
    #     rangeselector=dict(
    #         buttons=list([
    #             dict(count=1, label="1m", step="day", stepmode="backward"),
    #             dict(count=6, label="6m", step="month", stepmode="backward"),
    #             dict(count=1, label="YTD", step="year", stepmode="todate"),
    #             dict(count=1, label="1y", step="year", stepmode="backward"),
    #             dict(step="all")
    #         ])
    #     )
    # )

    return dcc.Graph(
        figure=fig,
        config={'displayModeBar': False}
    )
