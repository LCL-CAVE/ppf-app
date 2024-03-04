import plotly.express as px
import pandas as pd
import numpy as np
from controls.cl_fig_update_layout import create_update_layout_fig
import os


def serve_fig_out_tech_stack(freq):
    df = pd.read_csv(
        os.path.join(os.path.dirname('./data/'), 'tech_stack.csv'),
        delimiter=';',
    )

    df['date'] = pd.to_datetime(df['date'])

    if freq == "M":
        df = df.groupby([pd.Grouper(key="date", freq="M"), pd.Grouper('tech')]).mean()
    elif freq == "D":
        df = df.groupby([pd.Grouper(key="date", freq="D"), pd.Grouper('tech')]).mean()
    elif freq == "W":
        df = df.groupby([pd.Grouper(key="date", freq="W"), pd.Grouper('tech')]).mean()
    else:
        df = df.groupby([pd.Grouper(key="date", freq="H"), pd.Grouper('tech')]).mean()
    df = df.reset_index()

    fig = px.area(df, x="date", y="value", color="tech")

    create_update_layout_fig(fig, "Generation per Production Type (MW)")

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
        range=[min(df["value"]) + 100, max(df["value"]) + 2000],
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
