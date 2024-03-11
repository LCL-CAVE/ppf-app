import pandas as pd
import plotly.express as px
import holidays
from sklearn.preprocessing import PolynomialFeatures, QuantileTransformer
from engine.scenario_demand.eng_generate_scenario_demand import serve_eng_generate_scenario_demand
from math import ceil
import numpy as np
from sklearn.linear_model import LassoCV
from engine.scenario_demand.eng_calc_demand_profile import serve_eng_calc_demand_profile
from power_api.api_callback import serve_api_callback
from power_api.api_login import serve_api_login
import pandas as pd
import os
import pickle


# function starts here

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
        "demand_level": demand_level,
        "growth_rate_0_4": growth_rate_0_4,
        "growth_rate_4_8": growth_rate_4_8,
        "growth_rate_8_12": growth_rate_8_12,
        "growth_rate_12_16": growth_rate_12_16,
        "growth_rate_16_20": growth_rate_16_20,
        "growth_rate_20_0": growth_rate_20_0,
        "cluster_count": 4,  # Number of clusters for the errors and creating a transition matrix
        "transition_frequency": "2W",  # Frequency of transition (e.g., every 2 weeks)
        "train_data": "ES_param_demand.csv",  # Name of the Excel file for historical data
        "country": country,
        "demand_base_year": 2022
    }

    # Read and preprocess data
    # data = pd.read_csv(config["train_data"], sep='\t', index_col=0)
    df = df.drop(columns=["id", "bidding_zone_id"])
    df.index = df["timestamp"]
    df = df.drop(columns=["timestamp"])
    df = df.rename(columns={'load': 'Actual Load'})
    df.index = pd.to_datetime(df.index, utc=True)
    demand_profile = serve_eng_calc_demand_profile(df, config)

    # Convert the start and end dates to pandas datetime objects
    start_date = pd.to_datetime(config["scenario_start_date"])
    end_date = pd.to_datetime(config["scenario_end_date"])

    # Calculate the total duration between the start and end dates
    total_duration = end_date - start_date

    # Convert the transition_frequency to a pandas Timedelta and get the total days for one period
    period_duration_days = pd.Timedelta(config["transition_frequency"]).days

    # Calculate the number of periods and round up
    config["periods"] = ceil(total_duration.days / period_duration_days)

    # Calculate number of periods based on transition frequency
    config["number_of_periods"] = 24 * pd.Timedelta(config["transition_frequency"]).days

    country_holidays = holidays.CountryHoliday(config["country"])

    class SolarRegression(LassoCV):
        poly = PolynomialFeatures(degree=2, interaction_only=False, include_bias=False)

        def getX(self, datetime):
            X = (pd.DataFrame()
                 .assign(sy1=lambda x: np.sin(2 * np.pi * datetime.dayofyear / 365.25))
                 .assign(cy1=lambda x: np.cos(2 * np.pi * datetime.dayofyear / 365.25))
                 .join(pd.get_dummies(datetime.hour))
                 )
            return self.poly.fit_transform(X)

        def fit(self, datetime, y):
            super().fit(self.getX(datetime), y)

        def score(self, datetime, y):
            return super().score(self.getX(datetime), y)

        def predict(self, datetime):
            return super().predict(self.getX(datetime))

    class DemandRegression(SolarRegression):
        holidays = country_holidays

        def getX(self, datetime):
            X = pd.DataFrame()
            X = X.assign(holiday=pd.Series(datetime).apply(lambda x: 1 if x in self.holidays else 0))
            X = X.assign(sy1=lambda x: np.sin(2 * np.pi * datetime.dayofyear / 365.25))
            X = X.assign(cy1=lambda x: np.cos(2 * np.pi * datetime.dayofyear / 365.25))
            X = X.join(pd.get_dummies(datetime.hour, prefix='hour'))  # Prefix added for clarity
            X = X.join(pd.get_dummies(datetime.day_name(), prefix='day'))

            # Ensure all column names are strings to avoid the TypeError
            X.columns = X.columns.astype(str)

            return self.poly.fit_transform(X)

    # cache loading goes here

    pickle_file = bidding_zone + "_DEMAND.pickle"

    file_path = os.path.join(os.getcwd(), "engine/scenario_demand/" + pickle_file)

    with open(file_path, "rb") as f:
        prediction_errors_shape = pickle.load(f)
        kmeans_model = pickle.load(f)
        transition_matrix = pickle.load(f)
        errors = pickle.load(f)
        prediction_errors = pickle.load(f)
        demand_reg = pickle.load(f)
        quantile_transform = pickle.load(f)

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

    return scenarios
