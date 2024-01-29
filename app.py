import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate
from dash import Dash, Output, callback, Input, State, html, no_update, dcc
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



from components.c_display_chart_group import create_display_chart_group
from components.c_display_chart_group_out1 import create_display_chart_group_out1
from components.c_display_chart_group_out2 import create_display_chart_group_out2
from utils.fig_demand_curve import serve_fig_demand_curve
from utils.fig_price_curve import serve_fig_price_curve
from utils.fig_hist_temp import serve_fig_hist_temp
from utils.fig_fuel_price import serve_fig_fuel_price
from utils.fig_out_elec_price_forecast import serve_fig_out_elec_price_forecast
from utils.fig_out_capture_price import serve_fig_out_capture_price
from utils.fig_out_tech_stack import serve_fig_out_tech_stack
from utils.fig_installed_capacity import serve_fig_installed_capacity


@app.callback(
    Output("output-layout", "children", allow_duplicate=True),
    Input("btn_output_selector_market_dynamics", "n_clicks"),
    Input("date_picker_time_horizon_training", "value"),
    prevent_initial_call=True,
)
def update_display_graphs1(n_clicks, dates):
    start_date_train = dates[0]
    finish_date_train = dates[1]
    return create_display_chart_group(start_date_train, finish_date_train)


@app.callback(
    Output("output-layout", "children", allow_duplicate=True),
    Input("btn_output_selector_price_source", "n_clicks"),
    Input("date_picker_time_horizon_training", "value"),
    prevent_initial_call=True,
)
def update_display_graphs2(n_clicks, dates):
    start_date_train = dates[0]
    finish_date_train = dates[1]
    return create_display_chart_group_out2(start_date_train, finish_date_train)


# @app.callback(
#     Output("output-layout", "children", ),
#     Input("btn_output_selector_produce_source", "n_clicks"),
#     Input("date_picker_time_horizon_training", "value"),
#     prevent_initial_call=True,
# )
# def update_display_graphs3(n_clicks, dates):
#     start_date_train = dates[0]
#     finish_date_train = dates[1]
#     return create_display_chart_group_out1(start_date_train, finish_date_train)


@app.callback(
    Output("graph_input_demand_curve", "figure"),
    # Output("graph_input_price_curve", "figure"),
    Output("graph_input_fuel_price", "figure"),
    Output("graph_input_hist_temp", "figure"),
    Input("btn_time_group_display_market", "value"),
    Input("date_picker_time_horizon_training", "value"),
    prevent_initial_call=True,
)
def update_time_interval_graphs1(value, dates):
    start_date_train = dates[0]
    finish_date_train = dates[1]
    if value == "monthly":
        return serve_fig_demand_curve("M", start_date_train, finish_date_train), \
            serve_fig_fuel_price("M", start_date_train, finish_date_train), \
            serve_fig_hist_temp("M", start_date_train, finish_date_train)
    elif value == "weekly":
        return serve_fig_demand_curve("W", start_date_train, finish_date_train), \
            serve_fig_fuel_price("W", start_date_train, finish_date_train), \
            serve_fig_hist_temp("W", start_date_train, finish_date_train)
    elif value == "daily":
        return serve_fig_demand_curve("D", start_date_train, finish_date_train), \
            serve_fig_fuel_price("D", start_date_train, finish_date_train), \
            serve_fig_hist_temp("D", start_date_train, finish_date_train)
    else:
        return serve_fig_demand_curve("H", start_date_train, finish_date_train), \
            serve_fig_fuel_price("H", start_date_train, finish_date_train), \
            serve_fig_hist_temp("H", start_date_train, finish_date_train)


@app.callback(
    # Output("zxc", "children"),
    Output("graph_input_price_curve", "figure"),
    Output("graph_out_elec_price_forecast", "figure"),
    Output("graph_out_capture_price", "figure"),
    Input("btn_time_group_display_price", "value"),
    Input("date_picker_time_horizon_training", "value"),
    prevent_initial_call=True,
)
def update_time_interval_graphs2(value, dates):
    start_date_train = dates[0]
    finish_date_train = dates[1]
    if value == "monthly":
        return serve_fig_price_curve("M", start_date_train, finish_date_train), \
            serve_fig_out_elec_price_forecast("M"), \
            serve_fig_out_capture_price("M")
    elif value == "weekly":
        return serve_fig_price_curve("M", start_date_train, finish_date_train), \
            serve_fig_out_elec_price_forecast("W"), \
            serve_fig_out_capture_price("W")
    elif value == "daily":
        return serve_fig_price_curve("D", start_date_train, finish_date_train), \
            serve_fig_out_elec_price_forecast("D"), \
            serve_fig_out_capture_price("D")
    else:
        return serve_fig_price_curve("H", start_date_train, finish_date_train), \
            serve_fig_out_elec_price_forecast("H"), \
            serve_fig_out_capture_price("H")


@app.callback(
    # Output("zyx", "children"),
    Output("graph_out_tech_stack", "figure"),
    Output("graph_out_installed_capacity", "figure"),
    # Output("graph_out_solar_production", "figure"),
    # Output("graph_out_wind_production", "figure"),
    # Output("graph_out_hydro_production", "figure"),
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
        message="Engine passed the first step (inverse-model) successfully!",
    )


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
        message="Engine fetched the final solution successfully!",
    )


import numpy as np


# @app.callback(Output('text_kpi_avg_capture_price', 'children'),
#               Output('text_kpi_avg_production', 'children'),
#               Output('text_kpi_avg_price', 'children'),
#               Input('interval-component', 'n_intervals'))
# def update_kpi(n):
#     return str(np.round(50 + 10 * np.random.rand(), 2)) + " euro", str(
#         np.round(7400 + 300 * np.random.rand(), 2)) + " GW/h", str(np.round(50 + 10 * np.random.rand(), 2)) + " euro"


@app.callback(
    Output("loading-layout", "children"),
    Input("btn_run", "n_clicks"),
    prevent_initial_call=True,
)
def show5(n_clicks):
    time.sleep(5)
    return no_update


# @app.callback(
#     Output("selected-date-date-range-picker", "children"),
#     Input("date_picker_time_horizon_training", "value"),
# )
# def update_output(dates):
#     prefix = "You have selected: "
#     return dates[0]


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
            dmc.NotificationsProvider(
                [
                    html.Div(
                        id="notifications-container"
                    ),
                ],
                position='top-right',
            )
        ],
        withGlobalStyles=True,
        inherit=True,
        withNormalizeCSS=True,
        theme={
            "colorScheme": "light",
        },

    )
    from callbacks.clb_update_display_graphs3 import serve_clb_update_display_graphs3
    serve_clb_update_display_graphs3(app)
    app.run_server(debug=True)
