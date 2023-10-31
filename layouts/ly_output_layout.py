from dash import html
import dash_mantine_components as dmc
from dash_iconify import DashIconify as dicon
from components.c_kpi_group import create_kpi_group


def create_output_layout():
    return html.Table(
        [
            html.Tbody(
                [
                    html.Tr(
                        create_kpi_group()
                        +
                        [
                            html.Th(
                                dmc.Container(
                                    [
                                        dmc.Badge("Select Outputs", variant="outline", size="lg", color='gray',
                                                  fullWidth=True),
                                        dmc.Button(
                                            "Demand load",
                                            mt=20,
                                            id="load-button1",
                                            variant="filled",
                                            fullWidth=True,
                                            style={
                                                'box-shadow': 'rgba(9, 30, 66, 0.25) 0px 4px 8px -2px, rgba(9, 30, 66, 0.08) 0px 0px 0px 1px'}
                                        ),
                                        dmc.Button(
                                            "Production",
                                            mt=10,
                                            id="load-button2",
                                            variant="outline",
                                            fullWidth=True,
                                            style={
                                                'box-shadow': 'rgba(9, 30, 66, 0.25) 0px 4px 8px -2px, rgba(9, 30, 66, 0.08) 0px 0px 0px 1px'}
                                        ),
                                        dmc.Button(
                                            "Price dynamics",
                                            mt=10,
                                            id="load-button3",
                                            variant="outline",
                                            fullWidth=True,
                                            style={
                                                'box-shadow': 'rgba(9, 30, 66, 0.25) 0px 4px 8px -2px, rgba(9, 30, 66, 0.08) 0px 0px 0px 1px'}
                                        ),
                                    ],
                                    style={

                                        'position': 'sticky',
                                        'top': "2rem",
                                    },
                                ),
                                rowSpan=4,
                                style={'vertical-align': 'top',
                                       'padding-top': 20,
                                       'padding-left': 20,
                                       'padding-right': 20,
                                       'border-left': "1px solid #F5F5F5",
                                       },
                            ),
                        ],
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
