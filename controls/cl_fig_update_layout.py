from plotly.validators.layout import activeshape


def create_update_layout_fig(fig, title):
    fig.update_traces(fillcolor="rgba(0,0,255,.1)")
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
            font_size=16,
            font_family="Rockwell"
        ),
    )
