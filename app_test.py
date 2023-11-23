import dash_mantine_components as dmc
import dash
from dash import Dash, Output, callback, Input, State, html
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
        dmc.NotificationsProvider(
            [
                html.Div(
                    id="notifications-container"
                ),
            ],
            position='top-right',
        ),
        dmc.Paper(
            [
                create_header_layout(),
                create_body_layout(),
                dmc.Text(id="xyz"),
                dmc.Text(id="zyx"),
                dmc.Text(id="zxc"),
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
from components.c_display_chart_group_out2 import create_display_chart_group_out2


@app.callback(
    # Output("zyx", "children"),
    Output("output-layout", "children", allow_duplicate=True),
    Input("btn_output_selector_market_dynamics", "n_clicks"),
    prevent_initial_call=True,
)
def update_input_graphs1(n_clicks):
    # time.sleep(1)
    return create_display_chart_group()
    # return " ", create_display_chart_group()


@app.callback(
    # Output("zyx", "children"),
    Output("output-layout", "children", allow_duplicate=True),
    Input("btn_output_selector_price_source", "n_clicks"),
    prevent_initial_call=True,
)
def update_out_graphs2(n_clicks):
    # time.sleep(1)
    return create_display_chart_group_out2()


@app.callback(
    # Output("zyx", "children"),
    Output("output-layout", "children",),
    Input("btn_output_selector_produce_source", "n_clicks"),
    prevent_initial_call=True,
)
def update_out_graphs1(n_clicks):
    # time.sleep(1)
    return create_display_chart_group_out1()



from utils.fig_demand_curve import serve_fig_demand_curve
from utils.fig_price_curve import serve_fig_price_curve
from utils.fig_thermal_coal import serve_fig_thermal_coal
from utils.fig_nat_gas import serve_fig_natural_gas
from utils.fig_hist_temp import serve_fig_hist_temp


@app.callback(
    Output("xyz", "children"),
    Output("graph_input_demand_curve", "figure"),
    Output("graph_input_price_curve", "figure"),
    Output("graph_input_thermal_coal", "figure"),
    Output("graph_input_natural_gas", "figure"),
    Output("graph_input_hist_temp", "figure"),
    Input("btn_time_group_display_market", "value"),
    prevent_initial_call=True,
)
def update_input_graphs(value):
    if value == "monthly":
        return " ", serve_fig_demand_curve("M"), serve_fig_price_curve("M"), serve_fig_thermal_coal("M"), serve_fig_natural_gas("M"), serve_fig_hist_temp("M")
    elif value == "weekly":
        return " ", serve_fig_demand_curve("W"), serve_fig_price_curve("W"), serve_fig_thermal_coal("W"), serve_fig_natural_gas("W"), serve_fig_hist_temp("W")
    elif value == "daily":
        return " ", serve_fig_demand_curve("D"), serve_fig_price_curve("D"), serve_fig_thermal_coal("D"), serve_fig_natural_gas("D"), serve_fig_hist_temp("D")
    else:
        return " ", serve_fig_demand_curve("H"), serve_fig_price_curve("H"), serve_fig_thermal_coal("H"), serve_fig_natural_gas("H"), serve_fig_hist_temp("H")


from utils.fig_out_wind_capture_price import serve_fig_out_wind_capture_price
from utils.fig_out_elec_price_forecast import serve_fig_out_elec_price_forecast
from utils.fig_out_solar_capture_price import serve_fig_out_solar_capture_price


@app.callback(
    Output("zxc", "children"),
    Output("graph_out_elec_price_forecast", "figure"),
    Output("graph_out_solar_capture_price", "figure"),
    Output("graph_out_wind_capture_price", "figure"),
    Input("btn_time_group_display_price", "value"),
    prevent_initial_call=True,
)
def update_input_graphs(value):
    if value == "monthly":
        return " ", serve_fig_out_elec_price_forecast("M"), serve_fig_out_solar_capture_price("M"), serve_fig_out_wind_capture_price("M")
    elif value == "weekly":
        return " ", serve_fig_out_elec_price_forecast("W"), serve_fig_out_solar_capture_price("W"), serve_fig_out_wind_capture_price("W")
    elif value == "daily":
        return " ", serve_fig_out_elec_price_forecast("D"), serve_fig_out_solar_capture_price("D"), serve_fig_out_wind_capture_price("D")
    else:
        return " ", serve_fig_out_elec_price_forecast("H"), serve_fig_out_solar_capture_price("H"), serve_fig_out_wind_capture_price("H")

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



@app.callback(
    Output("notifications-container", "children", allow_duplicate=True),
    Input("btn_run", "n_clicks"),
    prevent_initial_call=True,
)
def show2(n_clicks):
    time.sleep(2)
    return dmc.Notification(
        title="First pass!",
        id="simple-notify2",
        action="show",
        message="Engine passed the first step (inverse-model) successfully!",
    )

@app.callback(
    Output("notifications-container", "children",),
    Input("btn_run", "n_clicks"),
    prevent_initial_call=True,
)
def show4(n_clicks):
    time.sleep(5)
    return dmc.Notification(
        title="Solution retrieved!",
        id="simple-notify4",
        action="show",
        message="Engine fetched the final solution successfully!",
    )


# @app.callback(
#     Output("notifications-container", "children",),
#     Input("btn_run", "n_clicks"),
#     prevent_initial_call=True,
# )
# def show4(n_clicks):
#     time.sleep(5)
#     return dmc.Notification(
#         title="Solution retrieved!",
#         id="simple-notify4",
#         action="show",
#         message="Engine fetched the final solution successfully!",
#     )



# Running the server
if __name__ == "__main__":
    # from callbacks.clb_update_input_graph import serve_clb_update_input_graphs
    #
    # serve_clb_update_input_graphs(app)
    app.run_server(debug=True)
