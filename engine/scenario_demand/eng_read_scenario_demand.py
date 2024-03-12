import pandas as pd
from engine.scenario_demand.eng_generate_scenario_demand import serve_eng_generate_scenario_demand
from math import ceil
from engine.scenario_demand.eng_calc_demand_profile import serve_eng_calc_demand_profile
from power_api.api_callback import serve_api_callback
from power_api.api_login import serve_api_login
import os
import cloudpickle


def serve_read_scenario_demand(demand_level,
                               bidding_zone,
                               growth_rate_0_4,
                               growth_rate_4_8,
                               growth_rate_8_12,
                               growth_rate_12_16,
                               growth_rate_16_20,
                               growth_rate_20_0,
                               scenario_start_date,
                               scenario_end_date):
    # scenario_start_date = "2025-04-07 00:00"
    # scenario_end_date = "2026-10-07 00:00"
    # demand_level = 24000
    # growth_rate_0_4 = 0.03
    # growth_rate_4_8 = 0.03
    # growth_rate_8_12 = 0.03
    # growth_rate_12_16 = 0.03
    # growth_rate_16_20 = 0.03
    # growth_rate_20_0 = 0.03
    # country = "Hungary"
    # bidding_zone = "HU"

    if bidding_zone == "ES":
        country = "Spain"
    elif bidding_zone == "FR":
        country = "France"
    elif bidding_zone == "HU":
        country = "Hungary"
    elif bidding_zone == "DE_LU":
        country = "Germany"
    elif bidding_zone == "NL":
        country = "Netherlands"
    elif bidding_zone == "BE":
        country = "Belgium"

    url, username, password = serve_api_login()

    # Request parameters
    payload = {
        'table': 'load_forecast',
        'bidding_zone': bidding_zone,
        'date_from': "2015-01-01 00:00:00",
        'date_to': "2023-05-31 23:45:00"
    }

    df = serve_api_callback(url, username, password, payload)

    config = {
        "num_scenarios": 10,  # Number of solar generation scenarios to generate
        "scenario_start_date": scenario_start_date,  # The start date for creating scenarios
        "scenario_end_date": scenario_end_date,  # User-defined end date for scenarios
        "demand_level": demand_level * 1000,
        "growth_rate_0_4": growth_rate_0_4 / 100,
        "growth_rate_4_8": growth_rate_4_8 / 100,
        "growth_rate_8_12": growth_rate_8_12 / 100,
        "growth_rate_12_16": growth_rate_12_16 / 100,
        "growth_rate_16_20": growth_rate_16_20 / 100,
        "growth_rate_20_0": growth_rate_20_0 / 100,
        "cluster_count": 4,  # Number of clusters for the errors and creating a transition matrix
        "transition_frequency": "2W",  # Frequency of transition (e.g., every 2 weeks)
        "country": country,
        "demand_base_year": 2022
    }

    # Convert the start and end dates to pandas datetime objects
    start_date = pd.to_datetime(config["scenario_start_date"])
    end_date = pd.to_datetime(config["scenario_end_date"])
    # Read and preprocess data
    # data = pd.read_csv(config["train_data"], sep='\t', index_col=0)
    df = df.drop(columns=["id", "bidding_zone_id"])
    df.index = df["timestamp"]
    df = df.drop(columns=["timestamp"])
    df = df.rename(columns={'load': 'Actual Load'})
    df.index = pd.to_datetime(df.index, utc=True)
    demand_profile = serve_eng_calc_demand_profile(df, config)



    # Calculate the total duration between the start and end dates
    total_duration = end_date - start_date

    # Convert the transition_frequency to a pandas Timedelta and get the total days for one period
    period_duration_days = pd.Timedelta(config["transition_frequency"]).days

    # Calculate the number of periods and round up
    config["periods"] = ceil(total_duration.days / period_duration_days)

    # Calculate number of periods based on transition frequency
    config["number_of_periods"] = 24 * pd.Timedelta(config["transition_frequency"]).days

    # cache loading goes here

    pickle_file = bidding_zone + "_DEMAND.pickle"

    file_path = os.path.join(os.getcwd(), "engine/scenario_demand/" + pickle_file)

    with open(file_path, "rb") as f:
        prediction_errors_shape = cloudpickle.load(f)
        kmeans_model = cloudpickle.load(f)
        transition_matrix = cloudpickle.load(f)
        errors = cloudpickle.load(f)
        prediction_errors = cloudpickle.load(f)
        demand_reg = cloudpickle.load(f)
        quantile_transform = cloudpickle.load(f)

    # Scenario Generation
    scenarios = serve_eng_generate_scenario_demand(config,
                                                   prediction_errors_shape,
                                                   kmeans_model,
                                                   transition_matrix,
                                                   errors,
                                                   prediction_errors,
                                                   demand_reg,
                                                   quantile_transform,
                                                   demand_profile)
    scenarios["timestamp"] = scenarios.index
    return scenarios
