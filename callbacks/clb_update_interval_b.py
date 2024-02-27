from app import app
from dash import Input, Output
from utils.fig_price_curve import serve_fig_price_curve
from utils.fig_out_elec_price_forecast import serve_fig_out_elec_price_forecast
from utils.fig_out_capture_price import serve_fig_out_capture_price


def serve_clb_update_interval_b(app):
    @app.callback(
        # Output("zxc", "children"),
        Output("graph_out_elec_price_forecast", "figure"),
        Output("graph_out_capture_price", "figure"),
        Input("btn_time_group_display_price", "value"),
        Input("date_picker_time_horizon_training", "value"),
        Input("dropdown_country", "value"),
        prevent_initial_call=True,
    )
    def update_time_interval_graphs2(value, dates, country):
        start_date_train = dates[0]
        finish_date_train = dates[1]
        if value == "monthly":
            return serve_fig_out_elec_price_forecast("M"), \
                serve_fig_out_capture_price("M")
        elif value == "weekly":
            return serve_fig_out_elec_price_forecast("W"), \
                serve_fig_out_capture_price("W")
        elif value == "daily":
            return serve_fig_out_elec_price_forecast("D"), \
                serve_fig_out_capture_price("D")
        else:
            return serve_fig_out_elec_price_forecast("H"), \
                serve_fig_out_capture_price("H")