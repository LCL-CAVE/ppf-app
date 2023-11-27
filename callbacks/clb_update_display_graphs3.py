from app_test import app
from dash import Input, Output
from components.c_display_chart_group_out1 import create_display_chart_group_out1


def serve_clb_update_display_graphs3(app):
    @app.callback(
        Output("output-layout", "children", ),
        Input("btn_output_selector_produce_source", "n_clicks"),
        prevent_initial_call=True,
    )
    def update_display_graphs3(n_clicks):
        return create_display_chart_group_out1()
