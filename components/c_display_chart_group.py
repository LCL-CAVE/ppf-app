import dash_mantine_components as dmc
from dash import html
from utils.fig_demand_curve import serve_fig_demand_curve
from utils.fig_price_curve import serve_fig_price_curve
from utils.fig_thermal_coal import serve_fig_thermal_coal
from utils.fig_nat_gas import serve_fig_natural_gas
from utils.fig_hist_temp import serve_fig_hist_temp
from controls.cl_json_parser import parse_json
from components.c_button_time_group import create_btn_time_group
from dash import html, dcc
import os


# category_list : .json
def create_display_chart_group():
    kpi_item_list = parse_json(
        os.path.join(
            os.path.dirname('./params/'),
            'kpi.json')
    )
    return [
        html.Tr(
            html.Td(
                children=[
                    html.Div(
                        create_btn_time_group("market"),
                        className="div-btn-time-grouper"),
                    dcc.Graph(
                        figure=serve_fig_demand_curve("D"),
                        config={'displayModeBar': False},
                        id="graph_input_demand_curve",
                    ),
                ],
                className="td-col-chart",
                colSpan=len(kpi_item_list),
            ),
        ),
        html.Tr(
            html.Td(
                children=[
                    dcc.Graph(
                        figure=serve_fig_price_curve("D"),
                        config={'displayModeBar': False},
                        id="graph_input_price_curve",
                    ),

                ],
                className="td-col-chart",
                colSpan=len(kpi_item_list),
            ),
        ),
        html.Tr(
            html.Td(
                children=[
                    dcc.Graph(
                        figure=serve_fig_thermal_coal("D"),
                        config={'displayModeBar': False},
                        id="graph_input_thermal_coal",
                    ),

                ],
                className="td-col-chart",
                colSpan=len(kpi_item_list),
            ),
        ),
        html.Tr(
            html.Td(
                children=[
                    dcc.Graph(
                        figure=serve_fig_natural_gas("D"),
                        config={'displayModeBar': False},
                        id="graph_input_natural_gas",
                    ),

                ],
                className="td-col-chart",
                colSpan=len(kpi_item_list),
            ),
        ),
        html.Tr(
            html.Td(
                children=[
                    dcc.Graph(
                        figure=serve_fig_hist_temp("D"),
                        config={'displayModeBar': False},
                        id="graph_input_hist_temp",
                    ),

                ],
                className="td-col-chart",
                colSpan=len(kpi_item_list),
            ),
        ),
    ]
