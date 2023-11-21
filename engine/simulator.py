### the out put should be a dictionary "data" with these keys: param_demand, gas, coal, carbon, temperature, actual_productions_RE
### data['actual_productions_RE'] is a df with columns: 'ActualGenerationOutput ES Solar', 'ActualGenerationOutput ES Wind Onshore','ActualGenerationOutput ES Hydro Run-of-river and poundage'

import pandas as pd
import math
import numpy as np
from sklearn.linear_model import LassoCV, LinearRegression
from sklearn.preprocessing import PolynomialFeatures, QuantileTransformer
from sklearn.cluster import KMeans
import holidays
from scenarioGenerator import SolarRegression, WindRegression, TemperatureRegression, DemandRegression, RorRegression
import warnings
warnings.filterwarnings("ignore")


def dataReaderFuture(start_date_future, end_date_future):

    # Read data for installed capacities in future
    param_capacities_future = (
        pd.read_excel(r'Future_data/scenario_ESP_PPApricing.xlsx', header=0, sheet_name='Capacities')
            .set_index('year')
            .pipe(lambda df: df.groupby(pd.Grouper(freq='H')).first())
            .interpolate()
            .loc[start_date_future:end_date_future])

    # Read data for demand in future
    param_demand_future = (
        pd.read_excel(r'Future_data/scenario_ESP_PPApricing.xlsx', header=0, sheet_name='Demand').set_index("year"))

    # Read data for fuel prices in future
    param_fuel_future = (
        pd.read_excel(r'Future_data/scenario_ESP_PPApricing.xlsx', header=0, sheet_name='Fuel price')
            .set_index('year')
            .pipe(lambda df: df.groupby(pd.Grouper(freq='H')).first())
            .interpolate()
            .loc[start_date_future:end_date_future])

    # Create a dictionary to store variables
    data_future = {
        'param_capacities_future': param_capacities_future,
        'param_demand_future': param_demand_future,
        'param_fuel_future': param_fuel_future
    }

    return data_future
##################################################################################
def markovChain(data, num_clusters, start_date_future, end_date_future, num_scenarios):
    param_demand = data['param_demand']
    param_solar_cap = data['installed_capacities_RE']['InstalledGenerationCapacityAggregated ES Solar']
    param_wind_cap = data['installed_capacities_RE']['InstalledGenerationCapacityAggregated ES Wind Onshore']
    param_ror_cap = data['installed_capacities_RE']['InstalledGenerationCapacityAggregated ES Hydro Run-of-river and poundage']
    param_solar_generation = data['actual_productions_RE']['ActualGenerationOutput ES Solar']
    param_wind_generation = data['actual_productions_RE']['ActualGenerationOutput ES Wind Onshore']
    param_ror_generation = data['actual_productions_RE']['ActualGenerationOutput ES Hydro Run-of-river and poundage']
    param_temperature = data['temperature']
    k = num_clusters

    # Join the DataFrames based on time stamps
    joined_data = pd.concat([param_demand, param_solar_generation, param_wind_generation, param_ror_generation, param_temperature], axis=1, join='inner')

    # Change the column names
    joined_data.columns = ['demand', 'solar', 'wind', 'ror', 'temperature']

    trans_freq = "2W"
    n_periods = 24 * pd.Timedelta(trans_freq).days
    train_data = "Spain_solar_wind(generate&installed).xlsx"

    # remove hourly demand profile
    X = pd.get_dummies(joined_data.index.hour)
    y = joined_data.demand
    reg = LinearRegression(fit_intercept=False)
    reg.fit(X, y)
    demand_profile = reg.coef_
    df = joined_data.copy()
    df.solar /= param_solar_cap
    df.wind /= param_wind_cap
    df.ror /= param_ror_cap
    df.demand = y / reg.predict(X)
    ax = pd.DataFrame(reg.coef_, columns=["demand_cap"]).plot(title="Demand Profile")
    # spanish holidays
    es_holidays = holidays.Spain()

    qt = QuantileTransformer(n_quantiles=100, output_distribution="normal")
    Y = pd.DataFrame(qt.fit_transform(df), index=df.index, columns=df.columns)
    errors = Y.copy()
    datetime = Y.index
    ############################# Solar
    y = Y.solar
    solar_reg = SolarRegression()
    solar_reg.fit(datetime, y)
    pred = solar_reg.predict(datetime)
    errors["solar"] = y - pred
    ############################# Wind
    y = Y.wind
    wind_reg = WindRegression()
    wind_reg.fit(datetime, y)
    pred = wind_reg.predict(datetime)
    errors["wind"] = y - pred
    ############################# Temperature
    y = Y.temperature
    temp_reg = TemperatureRegression()
    temp_reg.fit(datetime, y)
    pred = temp_reg.predict(datetime)
    errors["temperature"] = y - pred
    ############################# RoR
    y = Y.ror
    ror_reg = RorRegression()
    ror_reg.fit(datetime, y)
    pred = ror_reg.predict(datetime)
    errors["ror"] = y - pred
    ############################# Demand
    y = Y.demand
    demand_reg = DemandRegression()
    demand_reg.holidays = es_holidays
    demand_reg.fit(datetime, y)
    pred = demand_reg.predict(datetime)
    errors["demand"] = y - pred
    # 3 ######################### Cluster errors and estimate transition probabilities between clusters (Markov chain)
    # errors.describe().round(4)
    errors_ = errors.groupby(pd.Grouper(freq="H")).mean().interpolate()
    n, p = errors.shape
    clipsize = (n // n_periods) * n_periods
    errors_ = errors.values[:clipsize].reshape((n // n_periods, p * n_periods))

    km = KMeans(n_clusters=k)
    km.fit(errors_)

    clusters = pd.DataFrame(km.labels_, columns=["label"]).reset_index().groupby("label")
    sizes = clusters.count()
    sizes.describe().round(0).T

    tm = np.zeros((k, k))
    for i in np.c_[km.labels_[:-1], km.labels_[1:]]:
        tm[i[0], i[1]] += 1
    if (tm.sum(axis=0) == 0).any():
        raise Exception("Non-ergodic Markoc chain for transitions between clusters.")
    tm = tm.cumsum(axis=1)
    count = tm[:, -1]
    # 4 ######################### Scenario generations
    start = start_date_future
    # Create a DatetimeIndex from the start and end dates
    date_range = pd.date_range(start_date_future, end_date_future, freq='H')

    # Calculate the number of weeks between the two dates
    num_weeks = (len(date_range) + 1) // (7 * 24)

    # Ceil the result of (num_weeks + 1) / 2
    periods = math.ceil((num_weeks + 1) / 2)

    date_range = pd.date_range(start, periods=periods, freq=trans_freq)

    # Read user data for future
    data_future = dataReaderFuture(start_date_future, end_date_future)
    param_fuel_future = data_future['param_fuel_future']
    param_solar_cap_future = data_future['param_capacities_future']['solar']
    param_wind_cap_future = data_future['param_capacities_future']['wind onshore']
    param_ror_cap_future = data_future['param_capacities_future']['RoR']
    param_demand_future = data_future['param_demand_future']
    # param_generation_cap = data_future['param_capacities_future'][['Lignite','gas', 'coal', 'oil','Oil shale','Nuclear']]
    param_generation_cap = data_future['param_capacities_future'][['Lignite','gas', 'coal','Nuclear']]
    param_discharge_cap = data_future['param_capacities_future'][['Hydro Pumped Storage']]

    scenarios_list = []
    for s in range(num_scenarios):
        sample_size = len(date_range)
        sample = np.zeros((sample_size, p * n_periods))
        state = km.labels_[np.random.randint(len(km.labels_))]  # random starting state
        index = np.arange(k)
        for i in range(sample_size):
            state = index[np.random.randint(count[state]) < tm[state]][0]
            cluster = clusters.get_group(state)
            cluster_member_index = np.random.randint(sizes.loc[state])
            cluster_member_label = cluster.iloc[cluster_member_index].index[0]
            sample[i] = errors_[cluster_member_label]
        sample = sample.reshape((sample_size * n_periods, p))

        # Simulation
        sim = pd.DataFrame(sample, index=pd.date_range(start, periods=periods * n_periods, freq="H", name="datetime"),
                           columns=errors.columns)
        sim.solar += solar_reg.predict(sim.index)
        sim.wind += wind_reg.predict(sim.index)
        sim.temperature += temp_reg.predict(sim.index)
        sim.demand += demand_reg.predict(sim.index)
        sim = pd.DataFrame(qt.inverse_transform(sim.values), index=sim.index, columns=sim.columns)
        sim = sim.loc[start_date_future: end_date_future]
        # sim['year'] = sim.index.year

        # sim['demand'] = sim.groupby(['year', pd.Grouper(freq="D")]).demand.transform(
        #     lambda x: x.mul(demand_profile.loc[x.index.year[0]]))
        sim.demand = sim.groupby(pd.Grouper(freq="D")).demand.transform(lambda x: x.mul(demand_profile))
        sim.solar = sim['solar'].mul(param_solar_cap_future)
        sim.wind = sim['wind'].mul(param_wind_cap_future)
        sim.ror = sim['ror'].mul(param_ror_cap_future)

        scenarios_list.append(sim)

    dict_scenarios = {}

    for i in range(1, num_scenarios + 1):
        scenario_key = f'scenario_{i}'
        dict_scenarios[scenario_key] = {
            'param_demand': scenarios_list[i - 1]['demand'].to_frame(),
            'param_generation_cap': param_generation_cap,
            'param_discharge_cap': param_discharge_cap,
            'gas': param_fuel_future['Gas'],
            'coal': param_fuel_future['Coal'],
            'carbon': param_fuel_future['Carbon'],
            'temperature': scenarios_list[i - 1]['temperature'].to_frame(),
            'actual_productions_RE': pd.DataFrame({
                'ActualGenerationOutput ES Solar': scenarios_list[i - 1]['solar'],
                'ActualGenerationOutput ES Wind Onshore': scenarios_list[i - 1]['wind'],
                'ActualGenerationOutput ES Hydro Run-of-river and poundage': scenarios_list[i - 1]['ror']
            })
        }

    return dict_scenarios


