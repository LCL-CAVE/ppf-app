from app import app
from dash import Input, Output, callback_context, no_update
from components.c_display_chart_group_c import create_display_chart_group_c
from engine.scenario_fuel.eng_read_scenario_fuel import serve_read_scenario_fuel
from dash.exceptions import PreventUpdate


# def serve_clb_update_layout_c(app, cache, background_callback_manager):
def serve_clb_update_layout_c(app):
    @app.callback(
        Output("data_layout_c_row_a", "data"),
        Output("data_layout_c_row_b", "data"),
        Output("data_layout_c_row_c", "data"),
        Output("output-layout", "children", allow_duplicate=True),
        Input("btn_output_selector_fuel_scenario", "n_clicks"),
        Input("date_picker_time_horizon_forecasting", "value"),
        Input("num_input_price_gas_total", "value"),
        Input("num_input_price_coal_total", "value"),
        Input("num_input_price_carbon_total", "value"),
        Input("num_input_price_gas_change", "value"),
        Input("num_input_price_coal_change", "value"),
        Input("num_input_price_carbon_change", "value"),
        # background=True,
        # manager=background_callback_manager,
        prevent_initial_call=True,
    )
    # @cache.memoize()
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
        df_layout_c_row_a = serve_read_scenario_fuel("gas",
                                                     initial_price_gas,
                                                     growth_rate_gas,
                                                     scenario_start_date,
                                                     scenario_end_date,
                                                     ),
        df_layout_c_row_b = serve_read_scenario_fuel("coal",
                                                     initial_price_coal,
                                                     growth_rate_coal,
                                                     scenario_start_date,
                                                     scenario_end_date),
        df_layout_c_row_c = serve_read_scenario_fuel("carbon",
                                                     initial_price_carbon,
                                                     growth_rate_carbon,
                                                     scenario_start_date,
                                                     scenario_end_date),
        if n_clicks is None:
            raise PreventUpdate
        else:
            return {"data-frame": df_layout_c_row_a[0].to_dict("records")}, \
                {"data-frame": df_layout_c_row_b[0].to_dict("records")}, \
                {"data-frame": df_layout_c_row_c[0].to_dict("records")}, \
                create_display_chart_group_c("D",
                                             df_layout_c_row_c,
                                             df_layout_c_row_b,
                                             df_layout_c_row_c)
