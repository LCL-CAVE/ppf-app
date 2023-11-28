import plotly.express as px
import pandas as pd
from controls.cl_fig_update_layout import create_update_layout_fig
import os
import numpy as np

df = pd.read_csv(
    os.path.join(os.path.dirname('./data/'), 'es_demand_price.csv'),
    delimiter=';',
    decimal=","
)
print(df.shape[0])
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
