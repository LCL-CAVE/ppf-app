from app import app
from dash import Input, Output, callback_context, no_update
from components.c_display_chart_group_b import create_display_chart_group_b
from dash.exceptions import PreventUpdate


def serve_clb_update_layout_b(app, cache, background_callback_manager):
    @app.callback(
        Output("output-layout", "children", allow_duplicate=True),
        Input("btn_output_selector_price_source", "n_clicks"),
        Input("date_picker_time_horizon_forecasting", "value"),
        Input("num_input_capacity_solar_total", "value"),
        Input("num_input_capacity_wind_total", "value"),
        Input("num_input_capacity_hydro_total", "value"),
        Input("num_input_capacity_solar_change", "value"),
        Input("num_input_capacity_wind_change", "value"),
        Input("num_input_capacity_hydro_change", "value"),
        background=True,
        manager=background_callback_manager,
        prevent_initial_call=True,
    )
    @cache.memoize()
    def update_layout_b(n_clicks,
                        dates,
                        initial_capacity_solar,
                        initial_capacity_wind,
                        initial_capacity_hydro,
                        growth_rate_solar,
                        growth_rate_wind,
                        growth_rate_hydro):
        scenario_start_date = dates[0]
        scenario_end_date = dates[1]
        # if n_clicks is None:
        return create_display_chart_group_b("D",
                                            initial_capacity_solar,
                                            initial_capacity_wind,
                                            initial_capacity_hydro,
                                            growth_rate_solar,
                                            growth_rate_wind,
                                            growth_rate_hydro,
                                            scenario_start_date,
                                            scenario_end_date)
