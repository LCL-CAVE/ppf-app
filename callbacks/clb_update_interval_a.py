from app import app
from dash import Input, Output
from utils.fig_demand_curve import serve_fig_demand_curve
from utils.fig_hist_temp import serve_fig_hist_temp
from utils.fig_fuel_price import serve_fig_fuel_price


def serve_clb_update_interval_a(app):
    @app.callback(
        Output("graph_input_demand_curve", "figure"),
        Output("graph_input_fuel_price", "figure"),
        Output("graph_input_hist_temp", "figure"),
        Input("btn_time_group_display_market", "value"),
        Input("date_picker_time_horizon_training", "value"),
        prevent_initial_call=True,
    )
    def update_time_interval_graphs1(value, dates):
        start_date_train = dates[0]
        finish_date_train = dates[1]
        if value == "monthly":
            return serve_fig_demand_curve("M", start_date_train, finish_date_train), \
                serve_fig_fuel_price("M", start_date_train, finish_date_train), \
                serve_fig_hist_temp("M", start_date_train, finish_date_train)
        elif value == "weekly":
            return serve_fig_demand_curve("W", start_date_train, finish_date_train), \
                serve_fig_fuel_price("W", start_date_train, finish_date_train), \
                serve_fig_hist_temp("W", start_date_train, finish_date_train)
        elif value == "daily":
            return serve_fig_demand_curve("D", start_date_train, finish_date_train), \
                serve_fig_fuel_price("D", start_date_train, finish_date_train), \
                serve_fig_hist_temp("D", start_date_train, finish_date_train)
        else:
            return serve_fig_demand_curve("H", start_date_train, finish_date_train), \
                serve_fig_fuel_price("H", start_date_train, finish_date_train), \
                serve_fig_hist_temp("H", start_date_train, finish_date_train)
