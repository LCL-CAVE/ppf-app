from app import app
import pandas as pd
from dash import Input, Output
from utils.fig_multiple_line import serve_fig_multiple_line
from utils.fig_multiple_scatter import serve_fig_multiple_scatter
from engine.scenario_fuel.eng_read_scenario_fuel import serve_read_scenario_fuel

# def serve_clb_update_interval_c(app, cache, background_callback_manager):
def serve_clb_update_interval_c(app):
    @app.callback(
        Output("graph_group_c_row_a", "figure"),
        Output("graph_group_c_row_b", "figure"),
        Output("graph_group_c_row_c", "figure"),
        Input("btn_time_group_display_layout_c", "value"),
        Input("data_layout_c_row_a", "data"),
        Input("data_layout_c_row_b", "data"),
        Input("data_layout_c_row_c", "data"),
        # background=True,
        # manager=background_callback_manager,
        prevent_initial_call=True,
    )
    # @cache.memoize()
    def update_interval_b(freq,
                          data_layout_c_row_a,
                          data_layout_c_row_b,
                          data_layout_c_row_c):
        return serve_fig_multiple_scatter(pd.DataFrame(data_layout_c_row_a["data-frame"]),
                                          freq,
                                          'Gas Price', ), \
            serve_fig_multiple_scatter(pd.DataFrame(data_layout_c_row_b["data-frame"]),
                                       freq,
                                       'Coal Price'), \
            serve_fig_multiple_scatter(pd.DataFrame(data_layout_c_row_c["data-frame"]),
                                       freq,
                                       'Carbon Price', )
