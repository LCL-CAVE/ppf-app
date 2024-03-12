from app import app
from dash import Input, Output, State, callback_context, no_update, ctx
from utils.fig_multiple_line import serve_fig_multiple_line
import pandas as pd
from engine.scenario_demand.eng_read_scenario_demand import serve_read_scenario_demand
from components.c_display_chart_group_d import create_display_chart_group_d
from dash.exceptions import PreventUpdate


# def serve_clb_update_interval_b(app, cache, background_callback_manager):
def serve_clb_update_interval_d(app):
    @app.callback(
        Output("graph_group_d_row_a", "figure"),
        Input("btn_time_group_display_layout_d", "value"),
        Input("data_layout_d_row_a", "data"),
        # background=True,
        # manager=background_callback_manager,
        prevent_initial_call=True,
    )
    # @cache.memoize()
    def update_interval_d(freq,
                          data_layout_d_row_a):
        return serve_fig_multiple_line(pd.DataFrame(data_layout_d_row_a["data-frame"]),
                                       freq,
                                       'Demand Scenario (MW)',
                                       "MW")
