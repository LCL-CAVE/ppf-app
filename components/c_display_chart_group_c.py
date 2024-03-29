from utils.fig_multiple_scatter import serve_fig_multiple_scatter
from engine.scenario_fuel.eng_read_scenario_fuel import serve_read_scenario_fuel
from controls.cl_json_parser import parse_json
from components.c_button_time_group import create_btn_time_group
from dash import html, dcc
import os


def create_display_chart_group_c(freq,
                                 df_layout_c_row_a,
                                 df_layout_c_row_b,
                                 df_layout_c_row_c):
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
                        figure=serve_fig_multiple_scatter(df_layout_c_row_a[0],
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
                        figure=serve_fig_multiple_scatter(df_layout_c_row_b[0],
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
                        figure=serve_fig_multiple_scatter(df_layout_c_row_c[0],
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
