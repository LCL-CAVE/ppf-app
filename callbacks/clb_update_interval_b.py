from app import app
from dash import Input, Output
from components.c_display_chart_group_b import create_display_chart_group_b


def serve_clb_update_interval_b(app):
    @app.callback(
        Output("output-layout", "children", allow_duplicate=True),
        Input("date_picker_time_horizon_forecasting", "value"),
        Input("btn_time_group_display_layout_b", "value"),
        Input("num_input_capacity_solar_total", "value"),
        Input("num_input_capacity_wind_total", "value"),
        Input("num_input_capacity_hydro_total", "value"),
        Input("num_input_capacity_solar_change", "value"),
        Input("num_input_capacity_wind_change", "value"),
        Input("num_input_capacity_hydro_change", "value"),
        prevent_initial_call=True,
    )
    def update_interval_b(dates,
                          freq,
                          initial_capacity_solar,
                          initial_capacity_wind,
                          initial_capacity_hydro,
                          growth_rate_solar,
                          growth_rate_wind,
                          growth_rate_hydro):
        scenario_start_date = dates[0]
        scenario_end_date = dates[1]
        return create_display_chart_group_b(freq,
                                            initial_capacity_solar,
                                            initial_capacity_wind,
                                            initial_capacity_hydro,
                                            growth_rate_solar,
                                            growth_rate_wind,
                                            growth_rate_hydro,
                                            scenario_start_date,
                                            scenario_end_date)
