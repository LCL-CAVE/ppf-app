# Fuel Price Scenario Generator
# This script loads historical fuel price data and uses mean reverting models to simulate and plot future fuel price scenarios. It calculates mean reverting rates, simulates future prices for different commodities, and plots the residuals for analysis.

from engine.scenario_fuel.eng_load_data_fuel import load_data
from engine.scenario_fuel.eng_simulate_future_fuel_prices import simulateFutureFuelPrices
import os


def serve_read_scenario_fuel(fuelType, initialFuelPrice, growthRate, START_DATE_FUTURE, END_DATE_FUTURE):
    # Configuration for simulations and data paths
    simulation_config = {
        'numScenarios': 10,
        'fuelType': fuelType,  # can be 'gas', 'coal', or 'carbon'
        'initialFuelPrice': initialFuelPrice,  # Euro
        'growthRate': growthRate/100,  # equals to 20%
        'windowSizes': {
            'gas': 28,  # window size for gas (constant)
            'coal': 28,  # window size for coal (constant)
            'carbon': 28  # window size for carbon (constant)
        },
        'dataConfig': {
            'HISTORICAL_DATA_PATH': os.path.join(os.getcwd(),"engine/scenario_fuel/HistoricalFuelPrices.xlsx"),
            'HISTORICAL_SHEET': "Prices",
            'START_DATE_FUTURE': START_DATE_FUTURE,
            'END_DATE_FUTURE': END_DATE_FUTURE
        }
    }

    # Load historical and future fuel price data
    param_historical_fuels, param_fuel_future = load_data(simulation_config)

    # Perform simulations and plot the results
    future_fuel_prices = simulateFutureFuelPrices(param_historical_fuels, param_fuel_future,
                                                  simulation_config)
    return future_fuel_prices
