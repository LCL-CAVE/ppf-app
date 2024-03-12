import pandas as pd
import plotly.express as px
import holidays
from sklearn.preprocessing import PolynomialFeatures, QuantileTransformer
from engine.scenario_demand.eng_generate_matrix_transition import perform_clustering_and_create_transition_matrix
from math import ceil
import numpy as np
from sklearn.linear_model import LassoCV, LinearRegression
from engine.scenario_demand.eng_calc_demand_profile import serve_eng_calc_demand_profile
import requests
import pandas as pd
from datetime import datetime
from io import StringIO

scenario_start_date = "2025-04-07 00:00"
scenario_end_date = "2026-10-07 00:00"
demand_level = 24000
growth_rate_0_4 = 0.03
growth_rate_4_8 = 0.03
growth_rate_8_12 = 0.03
growth_rate_12_16 = 0.03
growth_rate_16_20 = 0.03
growth_rate_20_0 = 0.03
country = "Netherlands"
bidding_zone = "NL"
import os
import json
import sys


def serve_api_login():
    with open(os.path.join(
            sys.path[1],
            'power_api/credential.json'), 'r') as file:
        credential = json.load(file)

    username = credential[0]['username']
    password = credential[0]['password']
    url = 'http://127.0.0.1:5000/v1/table'

    return url, username, password


def serve_api_callback(url, username, password, payload):
    # Send authenticated request to the API
    response = requests.post(url, auth=(username, password), data=payload)

    # Check if request was successful
    if response.status_code == 200:
        # Convert JSON response to Pandas DataFrame
        df = pd.read_json(StringIO(response.text))

        # Convert 'timestamp' column to Pandas datetime format
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Display the DataFrame
        return df

    else:
        print(f"Error: {response.status_code} - {response.text}")


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
    "country": country,
    "demand_base_year": 2022
}
# config["final_capacity"] = config["initial_capacity"] * (1 + config["growth_rate"])

# Read and preprocess data
# data = pd.read_csv(config["train_data"], sep='\t', index_col=0)
# print(data)
df = df.drop(columns=["id", "bidding_zone_id"])
df.index = df["timestamp"]
df = df.drop(columns=["timestamp"])
df = df.rename(columns={'load': 'Actual Load'})
print(df)
data = df
data.index = pd.to_datetime(data.index, utc=True)
demand_profile = serve_eng_calc_demand_profile(data, config)

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

# ===============================================================================================================
# remove hourly demand profile
X = pd.get_dummies(data.index.hour)
y = data['Actual Load']
reg = LinearRegression(fit_intercept=False)
reg.fit(X, y)
# demand_profile = reg.coef_
df = data.copy()
df['Actual Load'] = y / reg.predict(X)
ax = pd.DataFrame(reg.coef_, columns=["demand_cap"]).plot(title="Demand Profile")

# Spanish Holidays
country_holidays = holidays.CountryHoliday(config["country"])

# Quantile Transformation
quantile_transform = QuantileTransformer(n_quantiles=100, output_distribution="normal")
Y = pd.DataFrame(quantile_transform.fit_transform(df), index=df.index, columns=df.columns)


##############################################################################################
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


##############################################################################################
# Error Calculation and Solar Regression
prediction_errors = Y.copy()
datetime = Y.index
y = Y['Actual Load']
demand_reg = DemandRegression()
# demand_reg.holidays = country_holidays
demand_reg.fit(datetime, y)
pred = demand_reg.predict(datetime)
prediction_errors["Actual Load"] = y - pred

n, prediction_errors_shape = prediction_errors.shape
clipsize = (n // config["number_of_periods"]) * config["number_of_periods"]
errors = prediction_errors.values[:clipsize].reshape(
    (n // config["number_of_periods"], prediction_errors_shape * config["number_of_periods"]))

# Performs KMeans clustering on the provided error data and creates a transition matrix.
kmeans_model, transition_matrix = perform_clustering_and_create_transition_matrix(errors, config["cluster_count"])
# ===============================================================================================================

import cloudpickle

with open(bidding_zone + "_DEMAND.pickle", "wb") as f:
    cloudpickle.dump(prediction_errors_shape, f)
    cloudpickle.dump(kmeans_model, f)
    cloudpickle.dump(transition_matrix, f)
    cloudpickle.dump(errors, f)
    cloudpickle.dump(prediction_errors, f)
    cloudpickle.dump(demand_reg, f)
    cloudpickle.dump(quantile_transform, f)

print("###############")
print("PICKLE is cached")
print("###############")
