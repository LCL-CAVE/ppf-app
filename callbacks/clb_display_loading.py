import time
from dash import Input, Output, no_update


def serve_clb_display_loading(app):
    @app.callback(
        Output("loading-layout", "children"),
        Input("btn_run", "n_clicks"),
        prevent_initial_call=True,
    )
    def show5(n_clicks):
        time.sleep(5)
        return no_update