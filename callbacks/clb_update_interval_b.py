from app import app
from dash import Input, Output
from utils.fig_multiple_line import serve_fig_multiple_line
from engine.scenario_capacity.eng_read_scenario import serve_read_scenario
from components.c_display_chart_group_b import create_display_chart_group_b


def serve_clb_update_interval_b(app, cache, background_callback_manager):
    @app.callback(
        Output("graph_group_b_row_a", "figure"),
        Output("graph_group_b_row_b", "figure"),
        Output("graph_group_b_row_c", "figure"),
        Input("date_picker_time_horizon_forecasting", "value"),
        Input("btn_time_group_display_layout_b", "value"),
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
        return serve_fig_multiple_line(serve_read_scenario(initial_capacity_solar,
                                                           growth_rate_solar,
                                                           scenario_start_date,
                                                           scenario_end_date,
                                                           "solar"),
                                       freq,
                                       'Solar Generation Scenarios (MW)',
                                       "MW"), \
            serve_fig_multiple_line(serve_read_scenario(initial_capacity_wind,
                                                        growth_rate_wind,
                                                        scenario_start_date,
                                                        scenario_end_date,
                                                        "wind"),
                                    freq,
                                    'Wind Generation Scenarios (MW)',
                                    "MW"), \
            serve_fig_multiple_line(serve_read_scenario(initial_capacity_hydro,
                                                        growth_rate_hydro,
                                                        scenario_start_date,
                                                        scenario_end_date,
                                                        "ror"),
                                    freq,
                                    'Hydro ROR Generation Scenarios (MW)',
                                    "MW")
