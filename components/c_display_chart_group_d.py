from utils.fig_multiple_line import serve_fig_multiple_line
from engine.scenario_capacity.eng_read_scenario import serve_read_scenario
from controls.cl_json_parser import parse_json
from components.c_button_time_group import create_btn_time_group
from dash import html, dcc
import os


def create_display_chart_group_d(freq,
                                 df_layout_d_row_a):
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
                        create_btn_time_group("layout_d"),
                        className="div-btn-time-grouper"),
                    dcc.Graph(
                        figure=serve_fig_multiple_line(df_layout_d_row_a,
                                                       freq,
                                                       'Demand Scenario(MW)',
                                                       "MW"),
                        config={'displayModeBar': False},
                        id="graph_group_d_row_a",
                    ),
                ],
                className="td-col-chart",
                colSpan=len(kpi_item_list),
            ),
        )
    ]
