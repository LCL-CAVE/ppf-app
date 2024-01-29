from app import app
from dash import Input, Output
from components.c_display_chart_group_out1 import create_display_chart_group_out1


def serve_clb_update_layout_c(app):
    @app.callback(
        Output("output-layout", "children", ),
        Input("btn_output_selector_produce_source", "n_clicks"),
        Input("date_picker_time_horizon_training", "value"),
        prevent_initial_call=True,
    )
    def update_display_graphs3(n_clicks, dates):
        start_date_train = dates[0]
        finish_date_train = dates[1]
        return create_display_chart_group_out1(start_date_train, finish_date_train)