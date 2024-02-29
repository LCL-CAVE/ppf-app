from app import app
from dash import Input, Output
from components.c_display_chart_group_b import create_display_chart_group_b


def serve_clb_update_layout_b(app):
    @app.callback(
        Output("output-layout", "children", allow_duplicate=True),
        Input("btn_output_selector_price_source", "n_clicks"),
        Input("date_picker_time_horizon_forecasting", "value"),
        Input("num_input_capacity_solar_total", "value"),
        Input("num_input_capacity_solar_change", "value"),
        Input("num_input_capacity_wind_total", "value"),
        Input("num_input_capacity_wind_change", "value"),
        Input("num_input_capacity_hydro_total", "value"),
        Input("num_input_capacity_hydro_change", "value"),
        # Input("dropdown_country", "value"),
        prevent_initial_call=True,
    )
    def update_display_graphs2(n_clicks,
                               dates,
                               initial_capacity_solar,
                               initial_capacity_wind,
                               initial_capacity_hydro,
                               growth_rate_solar,
                               growth_rate_wind,
                               growth_rate_hydro):
        scenario_start_date = dates[0]
        scenario_end_date = dates[1]
        return create_display_chart_group_b(initial_capacity_solar,
                                            initial_capacity_wind,
                                            initial_capacity_hydro,
                                            growth_rate_solar,
                                            growth_rate_wind,
                                            growth_rate_hydro,
                                            scenario_start_date,
                                            scenario_end_date)
