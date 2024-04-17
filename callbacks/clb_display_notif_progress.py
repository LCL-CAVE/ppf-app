import time
from dash import Input, Output
import dash_mantine_components as dmc


def serve_clb_display_notif_stage_a(app):
    @app.callback(
        Output("notifications-container", "children", allow_duplicate=True),
        Input("btn_run", "n_clicks"),
        prevent_initial_call=True,
    )
    def display_notification1(n_clicks):
        time.sleep(2)
        return dmc.Notification(
            title="First pass!",
            id="simple-notify2",
            action="show",
            message="Engine passed the inverse-model cache successfully!",
        )


def serve_clb_display_notif_stage_b(app):
    @app.callback(
        Output("notifications-container", "children", ),
        Input("btn_run", "n_clicks"),
        prevent_initial_call=True,
    )
    def display_notification2(n_clicks):
        time.sleep(5)
        return dmc.Notification(
            title="Second pass!",
            id="simple-notify4",
            action="show",
            message="Engine fetched the final cache solution successfully!",
        )
