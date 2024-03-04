import plotly.express as px
import pandas as pd
from controls.cl_fig_update_layout import create_update_layout_fig
from power_api.api_callback import serve_api_callback
from power_api.api_login import serve_api_login


def serve_fig_price_curve(freq, country, start_date_train, finish_date_train):
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
        'table': 'day_ahead_price',
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

    fig = px.line(df, x='timestamp', y='price', )

    create_update_layout_fig(fig, "Day ahead electricity price")
    # fig.update_traces(fillcolor="rgba(204,204,255,.15)")

    fig.update_yaxes(
        range=[min(df['price']) - 5, max(df['price']) + 2],
    )

    return fig
