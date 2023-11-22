from app_test import app
from dash import Dash, Output, callback, Input, State
from utils.fig_demand_curve import serve_fig_demand_curve
from utils.fig_price_curve import serve_fig_price_curve

def serve_clb_update_input_graphs(app):
    @app.callback(
        Output("xyz", "children"),
        Output("graph_input_demand_curve", "figure"),
        Output("graph_input_price_curve", "figure"),
        Input("btn_time_group_display", "value"),
        prevent_initial_call=True,
    )
    def update_input_graphs(value):
        if value == "monthly":
            return " ", serve_fig_demand_curve("M"), serve_fig_price_curve("M")
        elif value == "weekly":
            return " ", serve_fig_demand_curve("W"), serve_fig_price_curve("W")
        elif value == "daily":
            return " ", serve_fig_demand_curve("D"), serve_fig_price_curve("D")
        else:
            return " ", serve_fig_demand_curve("H"), serve_fig_price_curve("H")