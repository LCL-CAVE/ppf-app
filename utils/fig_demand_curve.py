import plotly.express as px
import pandas as pd
from controls.cl_fig_update_layout import create_update_layout_fig
from power_api.api_callback import serve_api_callback
from power_api.api_login import serve_api_login


def serve_fig_demand_curve(freq, country, start_date_train, finish_date_train):
    # df = pd.read_csv(
    #     os.path.join(os.path.dirname('./data/'), 'es_demand_price.csv'),
    #     delimiter=';',
    #     decimal=","
    # )
    #
    # df['timestamp'] = pd.to_datetime(df['timestamp'])

    url, username, password = serve_api_login()

    # Request parameters
    payload = {
        'table': 'load_forecast',
        'bidding_zone': country,
        'date_from': start_date_train,
        'date_to': finish_date_train
    }

    df = serve_api_callback(url, username, password, payload)

    df = df.loc[(df['timestamp'] > start_date_train) & (df['timestamp'] <= finish_date_train)]

    if freq == "M":
        df = df.groupby(pd.Grouper(key='timestamp', freq="M")).mean()
    elif freq == "D":
        df = df.groupby(pd.Grouper(key='timestamp', freq="D")).mean()
    elif freq == "W":
        df = df.groupby(pd.Grouper(key='timestamp', freq="W")).mean()
    else:
        df = df.groupby(pd.Grouper(key='timestamp', freq="H")).mean()
    df = df.reset_index()

    fig = px.line(df, x='timestamp', y='load')

    create_update_layout_fig(fig, "Demand load curve")
    # fig.update_traces(fillcolor="rgba(204,204,255,.15)")

    fig.update_yaxes(
        range=[min(df['load']) - 500, max(df['load']) + 500],
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
