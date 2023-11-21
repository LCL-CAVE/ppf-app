"""
This code implements a structural bottom-up model for competitive equilibria in the electricity market.
It forecasts future electricity prices based on market fundamentals using a combination of fundamental market modeling,
inverse optimization techniques, and machine learning. The model is calibrated with machine learning to align with real
market conditions and can handle noisy price data and operational complexities in the electricity sector.
The ultimate goal is to compute contract prices for Power Purchase Agreements (PPAs)
to assist large industrial consumers in meeting their sustainability targets.

--
Qorbanian, Roozbeh, Nils Löhndorf, and David Wozabal. "Valuation of Power Purchase Agreements for Corporate Renewable Energy Procurement."
"""

__author__ = "Roozbeh Qorbanian, Mohammad Namakshenas"
__copyright__ = "Copyright 2023, University of Luxembourg"

from dataReader import dataReader
from featureGenerator import featureExtractor, dateSlicer, featureExtractorFtuure
from simulator import markovChain
from inverseModel_CVXPY import inverseOptimizationSolver
from forwardModel_CVXPY import forwardOptimizationSolver
from postProcessor import plot_prices, plot_captured_prices, summary_table, plotScenarios
import time
import logging

# Create and configure logger
logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# User input this line
country = "ES"
country_full = "Spain"
start_date_train = "2018-01-01"
finish_date_train = "2019-01-01"
start_date_test = "2019-01-01"
finish_date_test = "2020-01-01"
start_date_future = "2024-01-01 00:00"
end_date_future = "2026-01-01 23:00"
num_scenarios = 3
param_lasso_1 = [7.35, 8.85, 13.10, 7.76, 6.68, 11.33]
param_lasso_2 = [7.97, 7.85, 10.72, 8.53, 11.03, 8.64]
Simulation = True
Validation = False


if __name__ == "__main__":

    # Read data
    logger.info("starting to read data")
    data = dataReader(country, country_full)
    logger.info("reading data is completed")

    # Simulation
    if Simulation:
        logger.info("starting to generate scenarios")
        data_scenarios = markovChain(data, num_clusters=4, start_date_future=start_date_future,
                                     end_date_future=end_date_future, num_scenarios=num_scenarios)
        logger.info("scenarios are generated")

    # Prepare features for the Inverse Model and Validation
    logger.info("starting to extract features")
    X_train = dateSlicer(data, country, start_date_train, finish_date_train)
    X_test = dateSlicer(data, country, start_date_test, finish_date_test)
    logger.info("features extracted")

    # Inverse model for Validation & Simulation
    start_time = time.perf_counter()
    logger.info("initializing the inverse model")
    dict_inverseModel = inverseOptimizationSolver(data, X_train, start_date_train, finish_date_train, param_lasso_1,
                                                  param_lasso_2)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    logger.info("the inverse model is solved in " + str(elapsed_time))

    # Forward model for Validation
    if Validation:
        dict_forwardModel = forwardOptimizationSolver(data, X_test, dict_inverseModel, start_date_test, finish_date_test)

    # Forward model for Simulation, Prepare features for Simulation
    if Simulation:
        for i in range(num_scenarios):
            scenario_key = f'scenario_{i + 1}'
            scenario_data = data_scenarios[scenario_key]
            X_scenario = featureExtractorFtuure(data, scenario_data, country, start_date_future, end_date_future)
            dict_forwardModel = forwardOptimizationSolver(scenario_data, X_scenario, dict_inverseModel, start_date_future,
                                                          end_date_future)

            # Add 'out_predicted_prices' to 'data_scenarios[scenario_key]['param_real_prices']'
            data_scenarios[scenario_key]['param_real_prices'] = dict_forwardModel['out_predicted_prices']

    # Post-process for Validation
    if Validation:
        results = plot_prices(dict_forwardModel, data, start_date_test, finish_date_test)
        plot_captured_prices(dict_forwardModel, data, start_date_test, finish_date_test)

        # create a table of Normalized Mean Absolute Error (NMAE) based on the day of the week and hours of a day.
        summary_df = summary_table(dict_forwardModel, data, start_date_test, finish_date_test)

    # Post-process for Simulation
    if Simulation:
        plotScenarios(data_scenarios, num_scenarios)