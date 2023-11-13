import plotly.express as px
import pandas as pd

df = pd.read_csv("./data/other_prices.csv", delimiter=';')
df['NatGas'] = df['NatGas'].str.replace(',', '.').astype(float)
df['ThermalCoal'] = df['ThermalCoal'].str.replace(',', '.').astype(float)
df['Carbon'] = df['Carbon'].str.replace(',', '.').astype(float)

df['date'] = pd.to_datetime(df['date'])

start_date_train = "2018-01-01"
finish_date_train = "2019-01-01"

# df = df[::30]

df = df.loc[(df['date'] > start_date_train) & (df['date'] <= finish_date_train)]

df = df.groupby(pd.Grouper(key="date", freq="D")).mean()
# df = df.groupby(pd.Grouper(key="date", freq="H")).mean()
df = df.reset_index()

fig = px.line(df, x='date', y="Carbon", render_mode='svg')
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

fig.show()
