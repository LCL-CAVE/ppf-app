from dash import html
import dash_mantine_components as dmc
from dash_iconify import DashIconify as dicon
from components.c_kpi_group import create_kpi_group
from controls.cl_button_output_group import create_btn_output_group


def create_output_layout():
    return html.Table(
        [
            html.Tbody(
                [
                    html.Tr(
                        create_kpi_group()
                        +
                        create_btn_output_group(),
                        style={'height': 90}
                    ),
                    html.Tr(
                        html.Td(
                            dmc.Image(src="/assets/eecc.png",
                                      alt="Without placeholder"),
                            className="td-col-chart",
                            colSpan=3,
                            style={'border-top': "1px solid #F5F5F5"},
                        ),
                        style={'padding': 0, 'margin': 0},
                    ),
                    html.Tr(

                        html.Td(
                            dmc.Image(src="/assets/Peak-Demand-Graph.jpg",
                                      alt="Without placeholder"),
                            className="td-col-chart",
                            colSpan=3,
                            style={'border-top': "1px solid #F5F5F5"},
                        ),

                        style={'padding': 0, },
                    ),
                    html.Tr(

                        html.Td(
                            dmc.Image(src="/assets/Peak-Demand-Graph.jpg",
                                      alt="Without placeholder"),
                            className="td-col-chart",
                            colSpan=3,
                            style={'border-top': "1px solid #F5F5F5"},
                        ),

                        style={'padding': 0},
                    ),
                ],
                style={"padding": 0, 'margin': 0}
            )
        ],
        style={'cellspacing': 0, 'border-left': "1px solid #F5F5F5", 'border-collapse': 'collapse'}
    )
