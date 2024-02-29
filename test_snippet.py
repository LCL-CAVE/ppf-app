import plotly.express as px
import pandas as pd
from controls.cl_fig_update_layout import create_update_layout_fig
import os
import numpy as np
#
# from power_api.api_callback import serve_api_callback
# import json
#
# # HTTP Basic Authentication Credentials
# with open(os.path.join(
#             os.getcwd(),
#             'power_api/credential.json'), 'r') as file:
#     credential = json.load(file)
#
# username = credential[0]['username']
# password = credential[0]['password']
# url = 'http://127.0.0.1:5000/v1/table'
#
# # Request parameters
# payload = {
#     'table': 'day_ahead_price',
#     'bidding_zone': 'DE_LU',  # Provide the desired bidding zone
#     'date_from': '2020-02-01 00:00:00',  # Provide start date
#     'date_to': '2021-02-01 23:59:59'  # Provide end date
# }
#
# df = serve_api_callback(url, username, password, payload)
#
#
# # start_date_train = "2018-01-01"
# # finish_date_train = "2019-01-01"
#
# df = df.loc[(df['timestamp'] > payload['date_from']) & (df['timestamp'] <= payload['date_to'])]
#
# # df = df.groupby(pd.Grouper(key="timestamp", freq="D")).mean()
# #
# # df = df.reset_index()
#
# fig = px.area(df, x='timestamp', y="price", )
#
# create_update_layout_fig(fig, "Day ahead electricity price")
# fig.update_traces(fillcolor="rgba(204,204,255,.15)")
#
# fig.update_yaxes(
#     range=[min(df["price"]) - 5, max(df["price"]) + 2],
# )
#
# fig.show()

print(50/100)
# # print(df.shape[0])
#
# df1 = df[['date', 'solar']]
# df2 = df[['date', 'wind']]
# df3 = df[['date', 'hydro']]
# df1 = df1.rename(columns={'solar': 'value'})
# df2 = df2.rename(columns={'wind': 'value'})
# df3 = df3.rename(columns={'hydro': 'value'})
# print(df1)
# print(df1)
# df1['type'] = "solar"
# df2['type'] = "wind"
# # df3['type'] = "hydro"
# df_new = pd.concat([df1, df2], ignore_index=True)
# df_new.to_csv("capture_prices.csv",index=False)
# print(df_new)

# df = pd.read_csv(
#     os.path.join(os.path.dirname('./data/'), 'tech_stack.csv'),
#     delimiter=';',
# )
# # df = px.data.medals_long()
# #
# # print(df)
# df['date'] = pd.to_datetime(df['date'])
# #
# df = df.groupby([pd.Grouper(key="date", freq="W"), pd.Grouper('tech')]).mean()
# df = df.reset_index()
# fig = px.area(df, x="date", y="value")
# fig.show()
#
# df['date'] = pd.to_datetime(df['date'])
# df = df.sort_values(by='date')
# df = df.set_index('date').resample('H').interpolate()
#
# print(df)
#
# df.to_csv("./data/other_prices2.csv")
# from controls.cl_json_parser import parse_json
#
# item_list = parse_json(
#     os.path.join(
#         os.path.dirname('./params/'),
#         'kpi.json')
# )
#
# print(item_list[0])

# print(np.round(7400+100*np.random.rand(),2))
#
# fig = px.area(df, x='date', y="value", )
# create_update_layout_fig(fig, "Solar Capture Price")
#
# fig.update_yaxes(
#     range=[min(df["value"]) - 2, max(df["value"]) + 2],
# )
# fig.show()

# start_date_train = "2024-01-01"
# finish_date_train = "2025-01-01"
#
# df = df.loc[(df['date'] > start_date_train) & (df['date'] <= finish_date_train)]
#
# if freq == "M":
#     df = df.groupby(pd.Grouper(key="date", freq="M")).mean()
# elif freq == "D":
#     df = df.groupby(pd.Grouper(key="date", freq="D")).mean()
# elif freq == "W":
#     df = df.groupby(pd.Grouper(key="date", freq="W")).mean()
# else:
#     df = df.groupby(pd.Grouper(key="date", freq="H")).mean()
# df = df.reset_index()
#
