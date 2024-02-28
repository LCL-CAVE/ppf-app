import pandas as pd
from math import ceil
import numpy as np
import pickle
import os
from engine.scenario.eng_scenario_generate import serve_eng_generate_scenarios
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import PolynomialFeatures


class SolarRegression(LassoCV):
    poly = PolynomialFeatures(degree=2, interaction_only=False, include_bias=False)

    def getX(self, datetime):
        X = pd.DataFrame({
            'sy1': np.sin(2 * np.pi * datetime.dayofyear / 365.25),
            'cy1': np.cos(2 * np.pi * datetime.dayofyear / 365.25),
        })

        # Generate hour dummies without converting to strings
        hour_dummies = pd.get_dummies(datetime.hour, prefix='hour')

        # Join the initial features with hour dummies
        X = pd.concat([X, hour_dummies], axis=1)

        # No need to convert column names to strings here
        return self.poly.fit_transform(X)

    def fit(self, datetime, y):
        super().fit(self.getX(datetime), y)

    def score(self, datetime, y):
        return super().score(self.getX(datetime), y)

    def predict(self, datetime):
        return super().predict(self.getX(datetime))


class WindRegression(SolarRegression):

    def getX(self, datetime):
        X = (pd.DataFrame(index=datetime)
             .assign(sy1=lambda x: np.sin(2 * np.pi * datetime.dayofyear / 365.25))
             .assign(cy1=lambda x: np.cos(2 * np.pi * datetime.dayofyear / 365.25))
             )
        return self.poly.fit_transform(X)


class RorRegression(SolarRegression):

    def getX(self, datetime):
        X = (pd.DataFrame(index=datetime)
             .assign(sy1=lambda x: np.sin(2 * np.pi * datetime.dayofyear / 365.25))
             .assign(cy1=lambda x: np.cos(2 * np.pi * datetime.dayofyear / 365.25))
             )
        return self.poly.fit_transform(X)


def serve_read_scenario(initial_capacity,
                        growth_rate,
                        scenario_start_date,
                        scenario_end_date,
                        generation_type):
    # inputs from user
    # initial_capacity = 30000
    # growth_rate = 0.7
    # scenario_start_date = "2024-06-01 00:00"
    # scenario_end_date = "2028-06-01 00:00"

    config = {
        "num_scenarios": 10,  # Number of solar generation scenarios to generate
        "scenario_start_date": scenario_start_date,  # The start date for creating scenarios
        "scenario_end_date": scenario_end_date,  # User-defined end date for scenarios
        "initial_capacity": initial_capacity,
        "growth_rate": growth_rate,
        "cluster_count": 4,  # Number of clusters for the errors and creating a transition matrix
        "transition_frequency": "2W",  # Frequency of transition (e.g., every 2 weeks)
    }
    config["final_capacity"] = config["initial_capacity"] * (1 + config["growth_rate"])

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

    # Cache loading goes here
    pickle_file = "ES_" + generation_type.upper() + ".pickle"

    file_path = os.path.join(os.getcwd(), "engine/scenario/" + pickle_file)

    # file_path = os.path.join(os.getcwd(), pickle_file)

    with open(file_path, "rb") as f:
        prediction_errors_shape = pickle.load(f)
        kmeans_model = pickle.load(f)
        transition_matrix = pickle.load(f)
        errors = pickle.load(f)
        prediction_errors = pickle.load(f)
        obj_reg = pickle.load(f)
        quantile_transform = pickle.load(f)
        generation_type = pickle.load(f)

    # Scenario Generation
    scenarios = serve_eng_generate_scenarios(config,
                                             prediction_errors_shape,
                                             kmeans_model,
                                             transition_matrix,
                                             errors,
                                             prediction_errors,
                                             obj_reg,
                                             quantile_transform,
                                             config["initial_capacity"],
                                             config["final_capacity"],
                                             generation_type)
    return scenarios
