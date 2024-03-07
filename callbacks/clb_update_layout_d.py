from app import app
from dash import Input, Output
from components.c_display_chart_group_d import create_display_chart_group_d


# def serve_clb_update_layout_d(app, cache, background_callback_manager):
def serve_clb_update_layout_d(app):
    @app.callback(
        Output("output-layout", "children", ),
        Input("btn_output_selector_produce_source", "n_clicks"),
        # background=True,
        # manager=background_callback_manager,
        prevent_initial_call=True,
    )
    # @cache.memoize()
    def update_display_graphs3(n_clicks):
        return create_display_chart_group_d("D")
