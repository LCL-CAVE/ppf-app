import dash_mantine_components as dmc
from dash import Dash
from layouts.ly_body_layout import create_body_layout
from layouts.ly_header_layout import create_header_layout
from components.c_display_notification_progress import create_notification_progress


app = Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,"
        "400;1,500;1,700;1,900&display=swap",
    ],
)

app.title = "PPF-app"
server = app.server
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True
app.config.suppress_callback_exceptions = True

# Running the server
if __name__ == "__main__":
    app.layout = dmc.MantineProvider(
        id="theme-app",
        children=[
            dmc.LoadingOverlay(
                dmc.Paper(
                    [
                        create_header_layout(),
                        create_body_layout(),

                    ],
                ),
                id="loading-layout"
            ),
            create_notification_progress(),
        ],
        withGlobalStyles=True,
        inherit=True,
        withNormalizeCSS=True,
        theme={
            "colorScheme": "light",
        },

    )
    from callbacks import clb_update_layout_a, clb_update_layout_b, clb_update_layout_c, clb_update_interval_a, \
        clb_update_interval_b, clb_update_interval_c, clb_display_notif_progress, clb_display_loading
    clb_update_layout_a.serve_clb_update_layout_a(app)
    clb_update_layout_b.serve_clb_update_layout_b(app)
    clb_update_layout_c.serve_clb_update_layout_c(app)
    clb_update_interval_a.serve_clb_update_interval_a(app)
    clb_update_interval_b.serve_clb_update_interval_b(app)
    clb_update_interval_c.serve_clb_update_interval_c(app)
    clb_display_notif_progress.serve_clb_display_notif_stage_a(app)
    clb_display_notif_progress.serve_clb_display_notif_stage_b(app)
    clb_display_loading.serve_clb_display_loading(app)
    app.run_server(debug=True)
