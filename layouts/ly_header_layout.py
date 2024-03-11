import dash_mantine_components as dmc
from dash import html
import os


def create_header_layout():
    return dmc.Header(
        height=60,
        children=
        [
            dmc.Grid(
                children=
                [
                    dmc.Col(
                        dmc.Text(
                            "LCL-Cave Power Price Forecasting",
                            color="blue",
                            mt=15,
                            ml=20,
                            className="header-text-col",
                        ),
                        span=6,
                    ),
                    dmc.Col(
                        html.Img(
                            src=os.path.join(
                                os.path.dirname('./assets/'),
                                'cave-lux-logo.png'),
                            className="logo-col",
                        ),
                        span=6,
                    ),
                ],

            ),
        ],
        className="layout-header"
    )
