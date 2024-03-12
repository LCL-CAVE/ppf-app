from app import app
from dash import Input, Output
from utils.fig_out_tech_stack import serve_fig_out_tech_stack
from utils.fig_out_capture_price import serve_fig_out_capture_price
from utils.fig_out_elec_price_forecast import serve_fig_out_elec_price_forecast

# def serve_clb_update_interval_d(app, cache, background_callback_manager):
def serve_clb_update_interval_e(app):
    @app.callback(
        Output("graph_group_e_row_a", "figure"),
        Output("graph_group_e_row_b", "figure"),
        Output("graph_group_e_row_c", "figure"),
        Input("btn_time_group_display_layout_e", "value"),
        # background=True,
        # manager=background_callback_manager,
        prevent_initial_call=True,
    )
    # @cache.memoize()
    def update_time_interval_e(freq):
        return serve_fig_out_elec_price_forecast(freq), serve_fig_out_capture_price(freq), serve_fig_out_tech_stack(freq)
