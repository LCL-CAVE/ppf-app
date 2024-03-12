from utils.fig_out_tech_stack import serve_fig_out_tech_stack
from utils.fig_out_capture_price import serve_fig_out_capture_price
from utils.fig_out_elec_price_forecast import serve_fig_out_elec_price_forecast
from controls.cl_json_parser import parse_json
from components.c_button_time_group import create_btn_time_group
from dash import html, dcc
import os


# category_list : .json
def create_display_chart_group_e(freq):
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
                        create_btn_time_group("layout_e"),
                        className="div-btn-time-grouper"),
                    dcc.Graph(
                        figure=serve_fig_out_elec_price_forecast(freq),
                        config={'displayModeBar': False},
                        id="graph_group_e_row_a",
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
                        figure=serve_fig_out_capture_price(freq),
                        config={'displayModeBar': False},
                        id="graph_group_e_row_b",
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
                        figure=serve_fig_out_tech_stack(freq),
                        config={'displayModeBar': False},
                        id="graph_group_e_row_c",
                    ),
                ],
                className="td-col-chart",
                colSpan=len(kpi_item_list),
            ),
        ),
        # html.Tr(
        #     html.Td(
        #         children=[
        #             dcc.Graph(
        #                 figure=serve_fig_out_solar_production("D"),
        #                 config={'displayModeBar': False},
        #                 id="graph_out_solar_production",
        #             ),
        #         ],
        #         className="td-col-chart",
        #         colSpan=len(kpi_item_list),
        #     ),
        # ),
        # html.Tr(
        #     html.Td(
        #         children=[
        #             dcc.Graph(
        #                 figure=serve_fig_out_wind_production("D"),
        #                 config={'displayModeBar': False},
        #                 id="graph_out_wind_production",
        #             ),
        #
        #         ],
        #         className="td-col-chart",
        #         colSpan=len(kpi_item_list),
        #     ),
        # ),
        # html.Tr(
        #     html.Td(
        #         children=[
        #             dcc.Graph(
        #                 figure=serve_fig_out_hydro_production("D"),
        #                 config={'displayModeBar': False},
        #                 id="graph_out_hydro_production",
        #             ),
        #
        #         ],
        #         className="td-col-chart",
        #         colSpan=len(kpi_item_list),
        #     ),
        # ),
    ]
