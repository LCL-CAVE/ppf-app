from sklearn.linear_model import LinearRegression
from engine.scenario_fuel.eng_load_data_fuel import load_data
import numpy as np

def calculate_rolling_log_diff(simulation_config, commodity, window=28):
    """
    Calculates the mean reverting rate and residuals for a given commodity using a rolling log difference method.

    :param param_historical_fuels: DataFrame containing historical fuel prices.
    :param commodity: The commodity for which to calculate the mean reverting rate.
    :param window: The window size for rolling calculation.
    :return: Mean reverting rate (mrr) and residuals.
    """
    param_historical_fuels, _ = load_data(simulation_config)

    df = param_historical_fuels.assign(price=param_historical_fuels[commodity])
    df = df.assign(mean=lambda x: x['price'].rolling(window=window, center=True).mean())
    df = df.assign(differences=lambda x: np.log(x['price']) - np.log(x['mean']))
    df = df.assign(shifted_diff=lambda x: x['differences'].shift(-1))
    df = df.dropna(subset=['price', 'mean', 'differences', 'shifted_diff'])  # ensure no NaN values
    Z = df['differences'].values.reshape(-1, 1)  # 'Z' as the differences
    y = df['shifted_diff'].values  # 'y' as the shifted differences

    # Perform linear regression
    reg = LinearRegression(fit_intercept=False)
    reg.fit(Z, y)

    # Get the model parameter (coefficient)
    mrr = reg.coef_[0]  # mean reverting rate

    # Calculate residuals (epsilons)
    residuals = y - reg.predict(Z)

    return mrr, residuals