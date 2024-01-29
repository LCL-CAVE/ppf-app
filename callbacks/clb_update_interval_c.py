from app import app
from dash import Input, Output
from utils.fig_out_tech_stack import serve_fig_out_tech_stack
from utils.fig_installed_capacity import serve_fig_installed_capacity


def serve_clb_update_interval_c(app):
    @app.callback(
        # Output("zyx", "children"),
        Output("graph_out_tech_stack", "figure"),
        Output("graph_out_installed_capacity", "figure"),
        Input("btn_time_group_display_produce", "value"),
        Input("date_picker_time_horizon_training", "value"),
        prevent_initial_call=True,
    )
    def update_time_interval_graphs3(value, dates):
        start_date_train = dates[0]
        finish_date_train = dates[1]
        if value == "monthly":
            return serve_fig_out_tech_stack("M"), serve_fig_installed_capacity("M", start_date_train, finish_date_train)
        elif value == "weekly":
            return serve_fig_out_tech_stack("W"), serve_fig_installed_capacity("W", start_date_train, finish_date_train)
        elif value == "daily":
            return serve_fig_out_tech_stack("D"), serve_fig_installed_capacity("D", start_date_train, finish_date_train)
        else:
            return serve_fig_out_tech_stack("H"), serve_fig_installed_capacity("H", start_date_train, finish_date_train)