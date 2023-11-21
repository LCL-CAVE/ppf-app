import pandas as pd


def dataReader(country, country_full):
    caps = pd.read_csv(f'Historical_data/ES_data.csv', delimiter=';', decimal=",")
    caps = caps.set_index('date').fillna(0)
    caps.index = pd.to_datetime(caps.index)
    caps['date'] = caps.index

    fuels = pd.read_csv(r'Historical_data/ES_data_prices.csv', delimiter=';', decimal=",")
    fuels['Delivery Date'] = pd.to_datetime(fuels['Delivery Date'])
    fuels = fuels.resample('H', on='Delivery Date').first().interpolate().fillna(method="bfill")

    temperature = pd.read_csv(r'Historical_data/hist_temp.csv', delimiter=';', decimal=",")
    temperature['date'] = pd.to_datetime(temperature['date'])
    temperature = temperature.sort_values(by='date').groupby(
        pd.Grouper(key="date", freq="H")).first().interpolate().fillna(method="bfill")

    data = {
        'param_demand': caps.filter(regex='^ActualTotalLoad'),
        'param_generation_cap': caps.filter(regex=r'(InstalledGenerationCapacity).*\b(Gas|coal|Nuclear)\b'),
        'param_generation': caps.filter(regex=r'(ActualGeneration).*\b(Gas|coal|Nuclear)\b'),
        'installed_capacities_RE': caps.filter(regex=r'(InstalledGenerationCapacity).*\b(Hydro|Solar|Wind|Biomass)\b'),
        'actual_productions_RE': caps.filter(regex=r'(ActualGeneration).*\b(Hydro|Solar|Wind|Biomass)\b'),
        'param_real_prices': caps.filter(regex='^DayAheadPrices'),
        'param_discharge_cap': caps.filter(regex='(?=.*InstalledGeneration)(?=.*Hydro Pumped Storage)'),
        'param_discharge': caps.filter(regex='(?=.*ActualGeneration)(?=.*Hydro Pumped Storage)'),
        'temperature': temperature,
        'gas': fuels['NatGas - TTF\n(€/MWh)'],
        'coal': fuels['Thermal Coal - API2\n($/t)'],
        'carbon': fuels['Carbon (€/t)'],
    }

    return data
