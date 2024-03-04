from app import app
from dash import Input, Output, callback_context, no_update
from components.c_display_chart_group_c import create_display_chart_group_c
from dash.exceptions import PreventUpdate


def serve_clb_update_layout_c(app, cache, background_callback_manager):
    @app.callback(
        Output("output-layout", "children", allow_duplicate=True),
        Input("btn_output_selector_fuel_scenario", "n_clicks"),
        Input("date_picker_time_horizon_forecasting", "value"),
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
    def update_layout_c(n_clicks,
                        dates,
                        initial_price_gas,
                        initial_price_coal,
                        initial_price_carbon,
                        growth_rate_gas,
                        growth_rate_coal,
                        growth_rate_carbon):
        scenario_start_date = dates[0]
        scenario_end_date = dates[1]
        # if n_clicks is None:
        return create_display_chart_group_c("D",
                                            initial_price_gas,
                                            initial_price_coal,
                                            initial_price_carbon,
                                            growth_rate_gas,
                                            growth_rate_coal,
                                            growth_rate_carbon,
                                            scenario_start_date,
                                            scenario_end_date)
