import plotly.express as px
import pandas as pd


def serve_fig_demand_curve(freq):
    df = pd.read_csv("./data/es_demand_price.csv", delimiter=';')
    df['DayAheadPrices_ES'] = df['DayAheadPrices_ES'].str.replace(',', '.').astype(float)

    df['date'] = pd.to_datetime(df['date'])

    start_date_train = "2018-01-01"
    finish_date_train = "2019-01-01"

    # df = df[::30]

    df = df.loc[(df['date'] > start_date_train) & (df['date'] <= finish_date_train)]

    if freq == "M":
        df = df.groupby(pd.Grouper(key="date", freq="M")).mean()
    elif freq == "D":
        df = df.groupby(pd.Grouper(key="date", freq="D")).mean()
    elif freq == "W":
        df = df.groupby(pd.Grouper(key="date", freq="W")).mean()
    else:
        df = df.groupby(pd.Grouper(key="date", freq="H")).mean()
    # df = df.groupby(pd.Grouper(key="date", freq="H")).mean()
    df = df.reset_index()


    fig = px.line(df, x='date', y="ActualTotalLoad_ES", render_mode='svg')
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
            l=40,
            r=40,
            b=40,
            t=0
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
        # autosize=True,
        legend={
            'visible': False
        },
        hoverlabel=dict(
            bgcolor='rgba(0,0,0,.9)',
            font_size=15,
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

    return fig
