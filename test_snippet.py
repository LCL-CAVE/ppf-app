import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import dash_mantine_components as dmc
from controls.cl_json_parser import parse_json
import os
#
# df = pd.read_csv("./data/es_demand_price.csv", delimiter=';')
#
# df['DayAheadPrices_ES'] = df['DayAheadPrices_ES'].str.replace(',', '.').astype(float)
#
# df['date'] = pd.to_datetime(df['date'])
#
# start_date_train = "2018-01-01"
# finish_date_train = "2019-01-01"
#
# df = df.loc[(df['date'] > start_date_train) & (df['date'] <= finish_date_train)]
#
# # df["ActualTotalLoad_ES"] = pd.to_numeric(df["ActualTotalLoad_ES"], downcast="float")
# # df["DayAheadPrices_ES"] = pd.to_numeric(df["DayAheadPrices_ES"], downcast="float")
# print(df)
#
# # df = df.reset_index(drop=True).set_index(['date'])
#
# # df = df.set_index(['date'])
#
# # df = df.resample('M').mean()
# df = df.groupby(pd.Grouper(key="date", freq="W")).mean()
#
# df = df.reset_index()
# # df['date'] = pd.to_datetime(df['date'])
# print(df)
# # df = df.groupby(pd.Grouper(key="datetime", freq="D"))
# # print(df)
# #
# # df = df.reset_index()
# # # print(df.head())
# #
# # # df = px.data.stocks()  # iris is a pandas DataFrame
# fig = px.line(df, x='date', y="ActualTotalLoad_ES")
# # fig.update_layout(
# #     margin=dict(l=0, r=0, b=0, t=0),
# #     yaxis={'ticklabelposition': 'inside', 'showgrid': False},
# #     xaxis={'ticklabelposition': 'inside', 'showgrid': False},
# #     plot_bgcolor='rgba(0,0,0,0)',
# #     paper_bgcolor='rgba(0,0,0,0)',
# #     autosize=True,
# #     legend={'visible': False})
# fig.show()
#
#
# # df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/volcano.csv")
# #
# # print(df.head())

import dash_mantine_components as dmc
from dash import Dash, Output, Input, html, callback

app = Dash()

app.layout = dmc.MantineProvider(
    id="theme-app",
    children=[
        html.Div(
            [
                dmc.SegmentedControl(
                    id="segmented",
                    value="ng",
                    data=[
                        {"value": "react", "label": "React"},
                        {"value": "ng", "label": "Angular"},
                        {"value": "svelte", "label": "Svelte"},
                        {"value": "vue", "label": "Vue"},
                    ],
                    mt=10,
                ),
                dmc.Text(id="segmented-value"),
            ]
        )
    ],
)


@callback(Output("segmented-value", "children"), Input("segmented", "value"))
def select_value(value):
    return value

# Running the server
if __name__ == "__main__":
    app.run_server(debug=True)