from app import app
from dash import Input, Output
from utils.fig_multiple_line import serve_fig_multiple_line
from utils.fig_multiple_scatter import serve_fig_multiple_scatter
from engine.scenario_fuel.eng_read_scenario_fuel import serve_read_scenario_fuel


def serve_clb_update_interval_c(app, cache, background_callback_manager):
    @app.callback(
        Output("graph_group_c_row_a", "figure"),
        Output("graph_group_c_row_b", "figure"),
        Output("graph_group_c_row_c", "figure"),
        Input("date_picker_time_horizon_forecasting", "value"),
        Input("btn_time_group_display_layout_c", "value"),
        Input("num_input_price_gas_total", "value"),
        Input("num_input_price_coal_total", "value"),
        Input("num_input_price_carbon_total", "value"),
        Input("num_input_price_gas_change", "value"),
        Input("num_input_price_coal_change", "value"),
        Input("num_input_price_carbon_change", "value"),
        background=True,
        manager=background_callback_manager,
        prevent_initial_call=True,
    )
    @cache.memoize()
    def update_interval_b(dates,
                          freq,
                          initial_price_gas,
                          initial_price_coal,
                          initial_price_carbon,
                          growth_rate_gas,
                          growth_rate_coal,
                          growth_rate_carbon):
        scenario_start_date = dates[0]
        scenario_end_date = dates[1]
        return serve_fig_multiple_scatter(serve_read_scenario_fuel("gas",
                                                                   initial_price_gas,
                                                                   growth_rate_gas,
                                                                   scenario_start_date,
                                                                   scenario_end_date),
                                          freq,
                                          'Gas Price', ), \
            serve_fig_multiple_scatter(serve_read_scenario_fuel("coal",
                                                                initial_price_coal,
                                                                growth_rate_coal,
                                                                scenario_start_date,
                                                                scenario_end_date),
                                       freq,
                                       'Coal Price'), \
            serve_fig_multiple_scatter(serve_read_scenario_fuel("carbon",
                                                                initial_price_carbon,
                                                                growth_rate_carbon,
                                                                scenario_start_date,
                                                                scenario_end_date),
                                       freq,
                                       'Carbon Price', )
