import dash_mantine_components as dmc
from dash import html
from utils.fig_out_wind_production import serve_fig_out_wind_production
from utils.fig_out_solar_production import serve_fig_out_solar_production
from utils.fig_out_hydro_production import serve_fig_out_hydro_production
from utils.fig_out_tech_stack import serve_fig_out_tech_stack
from utils.fig_installed_capacity import serve_fig_installed_capacity
from controls.cl_json_parser import parse_json
from components.c_button_time_group import create_btn_time_group
from dash import html, dcc
import os


# category_list : .json
def create_display_chart_group_out1(start_date_train_initial, finish_date_train_initial):
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
                        create_btn_time_group("produce"),
                        className="div-btn-time-grouper"),
                    dcc.Graph(
                        figure=serve_fig_installed_capacity("D", start_date_train_initial, finish_date_train_initial),
                        config={'displayModeBar': False},
                        id="graph_out_installed_capacity",
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
                        figure=serve_fig_out_tech_stack("D"),
                        config={'displayModeBar': False},
                        id="graph_out_tech_stack",
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
