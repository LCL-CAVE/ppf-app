import plotly.express as px
import pandas as pd
import numpy as np
from controls.cl_fig_update_layout import create_update_layout_fig
import os


def serve_fig_out_capture_price(freq):
    df = pd.read_csv(
        os.path.join(os.path.dirname('./data/'), 'capture_prices.csv'),
        delimiter=';',
    )

    df['date'] = pd.to_datetime(df['date'])

    if freq == "M":
        df = df.groupby([pd.Grouper(key="date", freq="M"), pd.Grouper('type')]).mean()
    elif freq == "D":
        df = df.groupby([pd.Grouper(key="date", freq="D"), pd.Grouper('type')]).mean()
    elif freq == "W":
        df = df.groupby([pd.Grouper(key="date", freq="W"), pd.Grouper('type')]).mean()
    else:
        df = df.groupby([pd.Grouper(key="date", freq="H"), pd.Grouper('type')]).mean()
    df = df.reset_index()

    fig = px.line(df, x="date", y="value", color="type")

    create_update_layout_fig(fig, "Capture Prices by Type")

    # fig.update_traces(fill='tozeroy')
    fig.update_layout(
        legend={
            'visible': True
        },
    )

    fig.update_layout(
        legend_title=None,
        legend=dict(
            x=.95,
            y=.99,
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=15,
                color="black"
            ),
        )
    )

    fig.update_yaxes(
        range=[min(df["value"]) - 2, max(df["value"]) + 2],
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

    return fig
