import plotly.express as px
import pandas as pd
from controls.cl_fig_update_layout import create_update_layout_fig


def serve_fig_natural_gas(freq):
    df = pd.read_csv("./data/other_prices.csv", delimiter=';')
    df['NatGas'] = df['NatGas'].str.replace(',', '.').astype(float)
    df['ThermalCoal'] = df['ThermalCoal'].str.replace(',', '.').astype(float)
    df['Carbon'] = df['Carbon'].str.replace(',', '.').astype(float)

    df['date'] = pd.to_datetime(df['date'])

    start_date_train = "2018-01-01"
    finish_date_train = "2019-01-01"

    df = df.loc[(df['date'] > start_date_train) & (df['date'] <= finish_date_train)]

    fig = px.area(df, x='date', y="NatGas",)

    create_update_layout_fig(fig, "Natural gas price")

    fig.update_yaxes(
        range=[min(df["NatGas"])-2, max(df["NatGas"])+2],
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
