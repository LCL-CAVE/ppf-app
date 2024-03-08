from app import app
from dash import Input, Output, callback_context, no_update, ctx
from components.c_display_chart_group_b import create_display_chart_group_b
from engine.scenario_capacity.eng_read_scenario import serve_read_scenario
from dash.exceptions import PreventUpdate


# def serve_clb_update_layout_b(app, cache, background_callback_manager):
def serve_clb_update_layout_b(app):
    @app.callback(
        Output("data_layout_b_row_a", "data"),
        Output("data_layout_b_row_b", "data"),
        Output("data_layout_b_row_c", "data"),
        Output("output-layout", "children", allow_duplicate=True),
        Input("btn_output_selector_price_source", "n_clicks"),
        Input("date_picker_time_horizon_forecasting", "value"),
        Input("num_input_capacity_solar_total", "value"),
        Input("num_input_capacity_wind_total", "value"),
        Input("num_input_capacity_hydro_total", "value"),
        Input("num_input_capacity_solar_change", "value"),
        Input("num_input_capacity_wind_change", "value"),
        Input("num_input_capacity_hydro_change", "value"),
        # background=True,
        # manager=background_callback_manager,
        prevent_initial_call=True,
    )
    # @cache.memoize()
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
        if callback_context.triggered_id == "btn_output_selector_price_source":
            df_layout_b_row_a = serve_read_scenario(initial_capacity_solar,
                                                    growth_rate_solar,
                                                    scenario_start_date,
                                                    scenario_end_date,
                                                    "solar"),
            df_layout_b_row_b = serve_read_scenario(initial_capacity_wind,
                                                    growth_rate_wind,
                                                    scenario_start_date,
                                                    scenario_end_date,
                                                    "wind"),
            df_layout_b_row_c = serve_read_scenario(initial_capacity_hydro,
                                                    growth_rate_hydro,
                                                    scenario_start_date,
                                                    scenario_end_date,
                                                    "ror"),
            return {"data-frame": df_layout_b_row_a[0].to_dict("records")}, \
                {"data-frame": df_layout_b_row_b[0].to_dict("records")}, \
                {"data-frame": df_layout_b_row_c[0].to_dict("records")}, \
                create_display_chart_group_b("D",
                                             df_layout_b_row_a,
                                             df_layout_b_row_b,
                                             df_layout_b_row_c)
        else:
            raise PreventUpdate

