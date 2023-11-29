import plotly.express as px
import pandas as pd
import numpy as np
from controls.cl_fig_update_layout import create_update_layout_fig
import os

def serve_fig_thermal_coal(freq, start_date_train, finish_date_train):
    df = pd.read_csv(
        os.path.join(os.path.dirname('./data/'), 'other_prices2.csv'),
        delimiter=';',
    )

    df['date'] = pd.to_datetime(df['date'])

    # start_date_train = "2018-01-01"
    # finish_date_train = "2019-01-01"

    df = df.loc[(df['date'] > start_date_train) & (df['date'] <= finish_date_train)]

    if freq == "M":
        df = df.groupby(pd.Grouper(key="date", freq="M")).mean()
    elif freq == "D":
        df = df.groupby(pd.Grouper(key="date", freq="D")).mean()
    elif freq == "W":
        df = df.groupby(pd.Grouper(key="date", freq="W")).mean()
    else:
        df = df.groupby(pd.Grouper(key="date", freq="H")).mean()
    df = df.reset_index()

    fig = px.area(df, x='date', y="ThermalCoal",)
    # fig = px.area(df, x='date', y="ThermalCoal", pattern_shape_sequence=["x"])

    create_update_layout_fig(fig, "Thermal Coal Price")
    fig.update_traces(fillcolor="rgba(204,204,255,.15)")

    fig.update_yaxes(
        range=[min(df["ThermalCoal"]) - 2, max(df["ThermalCoal"]) + 2],
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
