import plotly.graph_objs as go
import pandas as pd


def serve_fig_multiple_line(df, freq, title, Y_Axis_Title):
    """
    Generates and displays a solar scenario plot.

    Parameters:
    df (pandas.DataFrame): The DataFrame containing the data to plot.
    graph_type (str): The type of graph to plot.
    light, medium, dark (str): Color specifications for the plot.
    title (str): The title of the plot.
    Y_Axis_Title (str): The title of the Y-axis.
    """

    # , 'rgb(102, 178, 255)''rgb(204, 229, 255)''rgb(53, 204, 255)'
    light, medium, dark = 'rgb(255, 200, 200)', 'rgb(255, 160, 160)', 'rgb(255, 50, 50)'

    # Validate inputs
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input 'df' must be a pandas DataFrame")

    df.index = df['timestamp']
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.index = pd.to_datetime(df['timestamp'])
    df = df.drop(columns=["timestamp"])

    # Calculate quantiles
    quantiles = [0.05, 0.25, 0.5, 0.75, 0.95]
    for q in quantiles:
        df[f'{q}'] = df.iloc[:, :].dropna().quantile(q=q, axis=1)

    df['timestamp'] = df.index

    df = df.groupby(pd.Grouper(key="timestamp", freq=freq)).mean()

    # Create figure
    fig = go.Figure()

    # Add traces
    trace_configs = [
        {'y': df['0.05'], 'fill': 'tonexty', 'name': 'Q 0.05'},
        {'y': df['0.25'], 'fill': 'tonexty', 'name': 'Q 0.25'},
        {'y': df['0.5'], 'fill': None, 'name': 'Q 0.5'},
        {'y': df['0.75'], 'fill': 'tonexty', 'name': 'Q 0.75'},
        {'y': df['0.95'], 'fill': 'tonexty', 'name': 'Q 0.95'}
    ]
    # for config in trace_configs:
    #     fig.add_trace(go.Scatter(
    #         x=df.index, y=config['y'], fill=config.get('fill'),
    #         line=dict(color=(medium if config.get('fill') else dark), width=0 if config.get('fill') else 1),
    #         mode='lines', name=config['name'], showlegend=False if config['name'] == 'Q 0.05' else True
    #     ))

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['0.5'],
            mode='lines',
            line=dict(color=dark),
            name='Q 50%'
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['0.05'],
            mode='lines',
            line=dict(color=light, width=0),
            name='Q 5%'
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['0.95'],
            mode='lines',
            fill='tonexty',
            line=dict(color=light, width=0),
            name='Q 95%'
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['0.25'],
            mode='lines',
            line=dict(color=medium, width=0),
            name='Q 25%'
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['0.75'],
            mode='lines',
            fill='tonexty',
            line=dict(color=medium, width=0),
            name='Q 75%'
        )
    )

    # Update layout
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=16),
            automargin=True,
            yref='container',
            x=0.05,
            y=0.95,
        ),
        margin=dict(
            l=40,
            r=40,
            b=40,
            t=40
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
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
        hoverlabel=dict(
            bgcolor='rgba(0,0,0,.9)',
            font_size=16,
            font_family="Rockwell"
        ),
    )

    # fig.show()
    return fig
