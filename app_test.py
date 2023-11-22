import dash_mantine_components as dmc
import dash
from dash import Dash, Output, callback, Input, State
from layouts.ly_body_layout import create_body_layout
from layouts.ly_header_layout import create_header_layout
from controls.cl_json_parser import parse_json
import time

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

app.title = "ppa"
server = app.server
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True
app.config.suppress_callback_exceptions = True

app.layout = dmc.MantineProvider(
    id="theme-app",
    children=[
        dmc.Paper(
            [
                create_header_layout(),
                create_body_layout(),
                dmc.Text(id="xyz"),
                dmc.Text(id="zyx"),
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

from components.c_display_chart_group import create_display_chart_group
from components.c_display_chart_group2 import create_display_chart_group2
from components.c_display_chart_group_out1 import create_display_chart_group_out1


@app.callback(
    # Output("zyx", "children"),
    Output("output-layout", "children", allow_duplicate=True),
    Input("btn_output_selector_demand_load", "n_clicks"),
    prevent_initial_call=True,
)
def update_input_graphs1(n_clicks):
    # time.sleep(1)
    return create_display_chart_group()
    # return " ", create_display_chart_group()


@app.callback(
    # Output("zyx", "children"),
    Output("output-layout", "children", allow_duplicate=True),
    Input("btn_output_selector_price_dynamics", "n_clicks"),
    prevent_initial_call=True,
)
def update_input_graphs2(n_clicks):
    # time.sleep(1)
    return create_display_chart_group2()


@app.callback(
    # Output("zyx", "children"),
    Output("output-layout", "children"),
    Input("btn_output_selector_produce_source", "n_clicks"),
    prevent_initial_call=True,
)
def update_out_graphs1(n_clicks):
    # time.sleep(1)
    return create_display_chart_group_out1()


from utils.fig_demand_curve import serve_fig_demand_curve
from utils.fig_price_curve import serve_fig_price_curve

@app.callback(
    Output("xyz", "children"),
    Output("graph_input_demand_curve", "figure"),
    Output("graph_input_price_curve", "figure"),
    Input("btn_time_group_display_market", "value"),
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


from utils.fig_out_solar_production import serve_fig_out_solar_production
from utils.fig_out_wind_production import serve_fig_out_wind_production

@app.callback(
    Output("zyx", "children"),
    Output("graph_out_solar_production", "figure"),
    Output("graph_out_wind_production", "figure"),
    Input("btn_time_group_display_produce", "value"),
    prevent_initial_call=True,
)
def update_output_graphs(value):
    if value == "monthly":
        return " ", serve_fig_out_solar_production("M"), serve_fig_out_wind_production("M")
    elif value == "weekly":
        return " ", serve_fig_out_solar_production("W"), serve_fig_out_wind_production("W")
    elif value == "daily":
        return " ", serve_fig_out_solar_production("D"), serve_fig_out_wind_production("D")
    else:
        return " ", serve_fig_out_solar_production("H"), serve_fig_out_wind_production("H")


# Running the server
if __name__ == "__main__":
    # from callbacks.clb_update_input_graph import serve_clb_update_input_graphs
    #
    # serve_clb_update_input_graphs(app)
    app.run_server(debug=True)
