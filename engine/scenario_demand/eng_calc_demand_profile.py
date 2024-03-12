import pandas as pd
import numpy as np
from math import ceil


def serve_eng_calc_demand_profile(data, config):
    # Filter the data for the specified year
    df_year = data[data.index.year == config["demand_base_year"]]
    average_demand_per_hour = df_year.groupby(df_year.index.hour)['Actual Load'].mean().tolist()

    # Manipulate demand to match user input "demand_level"
    average_demand = sum(average_demand_per_hour) / len(average_demand_per_hour)
    factor = config['demand_level'] / average_demand
    demand_base_new = [demand * factor for demand in average_demand_per_hour]

    # Project demand to a future value wrt the growth rates
    demand_final_year = []
    for hour, demand in enumerate(demand_base_new):
        if hour < 4:
            growth_rate = config["growth_rate_0_4"]
        elif hour < 8:
            growth_rate = config["growth_rate_4_8"]
        elif hour < 12:
            growth_rate = config["growth_rate_8_12"]
        elif hour < 16:
            growth_rate = config["growth_rate_12_16"]
        elif hour < 20:
            growth_rate = config["growth_rate_16_20"]
        else:
            growth_rate = config["growth_rate_20_0"]
        demand_final_year.append(demand * (1 + growth_rate))

    # Linearly connect the initial values to final values wrt the number of years
    start_date = pd.to_datetime(config["scenario_start_date"])
    end_date = pd.to_datetime(config["scenario_end_date"])
    # years_difference = (end_date - start_date).days // 365.25
    # steps = int(years_difference) - 1
    if end_date.month < start_date.month or (end_date.month == start_date.month and end_date.day < start_date.day):
        number_of_years = end_date.year - start_date.year - 1
    else:
        number_of_years = end_date.year - start_date.year
    steps = number_of_years
    interpolated_lists = []
    if steps > 0:
        for step in range(1, steps + 1):
            fraction = step / (steps + 1)
            interpolated_list = demand_base_new + (np.array(demand_final_year) - np.array(demand_base_new)) * fraction
            interpolated_lists.append(interpolated_list.tolist())

    # Make the demand profile
    demand_base_new_arr = np.array(demand_base_new)
    interpolated_arrs = [np.array(lst) for lst in interpolated_lists]
    demand_final_year_arr = np.array(demand_final_year)
    demand_profile = np.vstack([demand_base_new_arr] + interpolated_arrs + [demand_final_year_arr])

    return demand_profile
