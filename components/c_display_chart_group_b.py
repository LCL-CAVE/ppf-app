from utils.fig_multiple_line import serve_fig_multiple_line
from engine.scenario.eng_read_scenario import serve_read_scenario
from controls.cl_json_parser import parse_json
from components.c_button_time_group import create_btn_time_group
from dash import html, dcc
import os


def create_display_chart_group_b(freq,
                                 initial_capacity_solar,
                                 initial_capacity_wind,
                                 initial_capacity_hydro,
                                 growth_rate_solar,
                                 growth_rate_wind,
                                 growth_rate_hydro,
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
                        create_btn_time_group("layout_b"),
                        className="div-btn-time-grouper"),
                    dcc.Graph(
                        figure=serve_fig_multiple_line(serve_read_scenario(initial_capacity_solar,
                                                                           growth_rate_solar,
                                                                           scenario_start_date,
                                                                           scenario_end_date,
                                                                           "solar"),
                                                       freq,
                                                       'Solar Generation Scenarios',
                                                       "MW"),
                        config={'displayModeBar': False},
                        id="graph_group_b_row_a",
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
                        figure=serve_fig_multiple_line(serve_read_scenario(initial_capacity_wind,
                                                                           growth_rate_wind,
                                                                           scenario_start_date,
                                                                           scenario_end_date,
                                                                           "wind"),
                                                       freq,
                                                       'Wind Generation Scenarios',
                                                       "MW"),
                        config={'displayModeBar': False},
                        id="graph_group_b_row_b",
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
                        figure=serve_fig_multiple_line(serve_read_scenario(initial_capacity_hydro,
                                                                           growth_rate_hydro,
                                                                           scenario_start_date,
                                                                           scenario_end_date,
                                                                           "ror"),
                                                       freq,
                                                       'Hydro ROR Generation Scenarios',
                                                       "MW"),
                        config={'displayModeBar': False},
                        id="graph_group_b_row_c",
                    ),
                ],
                className="td-col-chart",
                colSpan=len(kpi_item_list),
            ),
        ),
    ]
