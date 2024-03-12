from app import app
from dash import Input, Output, callback_context, no_update, ctx
from components.c_display_chart_group_d import create_display_chart_group_d
from engine.scenario_demand.eng_read_scenario_demand import serve_read_scenario_demand
from dash.exceptions import PreventUpdate


# def serve_clb_update_layout_b(app, cache, background_callback_manager):
def serve_clb_update_layout_d(app):
    @app.callback(
        Output("data_layout_d_row_a", "data"),
        Output("output-layout", "children", allow_duplicate=True),
        Input("btn_output_selector_layout_d", "n_clicks"),
        Input("date_picker_time_horizon_forecasting", "value"),
        Input("dropdown_country", "value"),
        Input("slider_demand_demand_level", "value"),
        Input("slider_demand_0_4_rate", "value"),
        Input("slider_demand_4_8_rate", "value"),
        Input("slider_demand_8_12_rate", "value"),
        Input("slider_demand_12_16_rate", "value"),
        Input("slider_demand_16_20_rate", "value"),
        Input("slider_demand_20_0_rate", "value"),

        # background=True,
        # manager=background_callback_manager,
        prevent_initial_call=True,
    )
    # @cache.memoize()
    def update_layout_d(n_clicks,
                        dates,
                        bidding_zone,
                        demand_level,
                        growth_rate_0_4,
                        growth_rate_4_8,
                        growth_rate_8_12,
                        growth_rate_12_16,
                        growth_rate_16_20,
                        growth_rate_20_0):
        scenario_start_date = dates[0]
        scenario_end_date = dates[1]
        if callback_context.triggered_id == "btn_output_selector_layout_d":
            df_layout_d_row_a = serve_read_scenario_demand(demand_level,
                                                           bidding_zone,
                                                           growth_rate_0_4,
                                                           growth_rate_4_8,
                                                           growth_rate_8_12,
                                                           growth_rate_12_16,
                                                           growth_rate_16_20,
                                                           growth_rate_20_0,
                                                           scenario_start_date,
                                                           scenario_end_date)
            return {"data-frame": df_layout_d_row_a.to_dict("records")}, \
                create_display_chart_group_d("D",
                                             df_layout_d_row_a)
        else:
            raise PreventUpdate
