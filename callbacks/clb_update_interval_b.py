from app import app
from dash import Input, Output, State, callback_context, no_update, ctx
from utils.fig_multiple_line import serve_fig_multiple_line
import pandas as pd
from engine.scenario_capacity.eng_read_scenario import serve_read_scenario
from components.c_display_chart_group_b import create_display_chart_group_b
from dash.exceptions import PreventUpdate


# def serve_clb_update_interval_b(app, cache, background_callback_manager):
def serve_clb_update_interval_b(app):
    @app.callback(
        Output("graph_group_b_row_a", "figure"),
        Output("graph_group_b_row_b", "figure"),
        Output("graph_group_b_row_c", "figure"),
        Input("btn_time_group_display_layout_b", "value"),
        Input("data_layout_b_row_a", "data"),
        Input("data_layout_b_row_b", "data"),
        Input("data_layout_b_row_c", "data"),
        # background=True,
        # manager=background_callback_manager,
        prevent_initial_call=True,
    )
    # @cache.memoize()
    def update_interval_b(freq,
                          data_layout_b_row_a,
                          data_layout_b_row_b,
                          data_layout_b_row_c):
        return serve_fig_multiple_line(pd.DataFrame(data_layout_b_row_a["data-frame"]),
                                       freq,
                                       'Solar Generation Scenarios (MW)',
                                       "MW"), \
            serve_fig_multiple_line(pd.DataFrame(data_layout_b_row_b["data-frame"]),
                                    freq,
                                    'Wind Generation Scenarios (MW)',
                                    "MW"), \
            serve_fig_multiple_line(pd.DataFrame(data_layout_b_row_c["data-frame"]),
                                    freq,
                                    'Hydro ROR Generation Scenarios (MW)',
                                    "MW")
