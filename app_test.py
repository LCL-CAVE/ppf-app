import dash_mantine_components as dmc
import dash
from dash import Dash, Output, callback, Input, State
from layouts.ly_body_layout import create_body_layout
from layouts.ly_header_layout import create_header_layout
from controls.cl_json_parser import parse_json
from utils.fig_demand_curve import serve_fig_demand_curve
from utils.fig_price_curve import serve_fig_price_curve

app = Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,"
        "400;1,500;1,700;1,900&display=swap",
    ]
)
app.title = "ppa"
server = app.server
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

app.layout = dmc.MantineProvider(
    id="theme-app",
    children=[
        dmc.Paper(
            [
                create_header_layout(),
                create_body_layout(),
            ],
        )
    ],
    withGlobalStyles=True,
    inherit=True,
    withNormalizeCSS=True,
    theme={
        "colorScheme": "light",
    },

)


@app.callback(
    Output("xyz", "children"),
    Output("graph_input_demand_curve", "figure"),
    Output("graph_input_price_curve", "figure"),
    Input("btn_time_group_display", "value")
)
def select_value(value):
    if value == "monthly":
        return " ", serve_fig_demand_curve("M"), serve_fig_price_curve("M")
    elif value == "weekly":
        return " ", serve_fig_demand_curve("W"), serve_fig_price_curve("W")
    elif value == "daily":
        return " ", serve_fig_demand_curve("D"), serve_fig_price_curve("D")
    else:
        return " ", serve_fig_demand_curve("H"), serve_fig_price_curve("H")


# Running the server
if __name__ == "__main__":
    app.run_server(debug=True)
