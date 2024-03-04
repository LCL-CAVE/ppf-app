from engine.scenario_capacity.eng_read_scenario import serve_read_scenario
from utils.fig_multiple_line import serve_fig_multiple_line

initial_capacity = 30000
growth_rate = 0.7
scenario_start_date = "2024-06-01 00:00"
scenario_end_date = "2028-06-01 00:00"
generation_type = 'ror'

# scenarios = serve_read_scenario(initial_capacity,
#                                 growth_rate,
#                                 scenario_start_date,
#                                 scenario_end_date,
#                                 generation_type)
#
# serve_fig_multiple_line(scenarios, "M", generation_type.upper() + ' Generation Scenarios', 'MW')


serve_fig_multiple_line(serve_read_scenario(initial_capacity, growth_rate, scenario_start_date,
                                            scenario_end_date,
                                            "solar"),"D",
                                                       'Wind Generation Scenarios',
                                                       "MW")