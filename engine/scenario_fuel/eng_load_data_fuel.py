import pandas as pd
import numpy as np

def load_data(simulation_config):
    """
    Loads historical and future fuel data from specified Excel files and sheets.

    :param data_config: Dictionary containing data file paths, sheet names, and date range.
    :return: Tuple of DataFrames (historical_fuels, future_fuels)
    """
    try:
        # Extracting configuration
        HISTORICAL_DATA_PATH = simulation_config['dataConfig']['HISTORICAL_DATA_PATH']
        HISTORICAL_SHEET = simulation_config['dataConfig']['HISTORICAL_SHEET']
        START_DATE_FUTURE = simulation_config['dataConfig']['START_DATE_FUTURE']
        END_DATE_FUTURE = simulation_config['dataConfig']['END_DATE_FUTURE']
        initial_value = simulation_config['initialFuelPrice']
        growth_rate = simulation_config['growthRate']
        fuelType = simulation_config['fuelType']

        # Loading historical data
        fuels = pd.read_excel(HISTORICAL_DATA_PATH, sheet_name=HISTORICAL_SHEET, header=0)
        # fuels = pd.read_csv(HISTORICAL_DATA_PATH, delimiter=';', decimal=",")
        fuels = fuels.resample('D', on='Delivery Date').first().interpolate().fillna(method="bfill")
        fuels = fuels[fuelType]
        fuels = fuels.to_frame(name=fuelType)
        # df['price'] = param_historical_fuels

        # Loading future data
        date_range = pd.date_range(start=START_DATE_FUTURE, end=END_DATE_FUTURE)
        final_value = initial_value * (1 + growth_rate)
        linear_values = np.linspace(start=initial_value, stop=final_value, num=len(date_range))
        param_fuel_future = pd.DataFrame(linear_values, index=date_range, columns=[fuelType])
        param_fuel_future.index.name = "year"

        return fuels, param_fuel_future

    except Exception as e:
        # Handle exceptions like FileNotFoundError, KeyError, etc.
        print(f"An error occurred: {e}")
        return None, None