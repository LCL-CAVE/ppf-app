from utils.fig_multiple_scatter import serve_fig_multiple_scatter
from engine.scenario_fuel.eng_read_scenario_fuel import serve_read_scenario_fuel
from controls.cl_json_parser import parse_json
from components.c_button_time_group import create_btn_time_group
from dash import html, dcc
import os


def create_display_chart_group_c(freq,
                                 initial_price_gas,
                                 initial_price_coal,
                                 initial_price_carbon,
                                 growth_rate_gas,
                                 growth_rate_coal,
                                 growth_rate_carbon,
                                 scenario_start_date,
                                 scenario_end_date):
    kpi_item_list = parse_json(
        os.path.join(
            os.path.dirname('./params/'),
            'kpi.json')
    )
    if freq is None:
        freq = "D"
    return [
        html.Tr(
            html.Td(
                children=[
                    html.Div(
                        create_btn_time_group("layout_c"),
                        className="div-btn-time-grouper"),
                    dcc.Graph(
                        figure=serve_fig_multiple_scatter(serve_read_scenario_fuel("gas",
                                                                                   initial_price_gas,
                                                                                   growth_rate_gas,
                                                                                   scenario_start_date,
                                                                                   scenario_end_date),
                                                          freq,
                                                          'Gas Price'),
                        config={'displayModeBar': False},
                        id="graph_group_c_row_a",
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
                        figure=serve_fig_multiple_scatter(serve_read_scenario_fuel("coal",
                                                                                   initial_price_coal,
                                                                                   growth_rate_coal,
                                                                                   scenario_start_date,
                                                                                   scenario_end_date),
                                                          freq,
                                                          'Coal Price', ),
                        config={'displayModeBar': False},
                        id="graph_group_c_row_b",
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
                        figure=serve_fig_multiple_scatter(serve_read_scenario_fuel("carbon",
                                                                                   initial_price_carbon,
                                                                                   growth_rate_carbon,
                                                                                   scenario_start_date,
                                                                                   scenario_end_date),
                                                          freq,
                                                          'Carbon Price', ),
                        config={'displayModeBar': False},
                        id="graph_group_c_row_c",
                    ),
                ],
                className="td-col-chart",
                colSpan=len(kpi_item_list),
            ),
        ),
    ]
