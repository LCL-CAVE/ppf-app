import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import holidays
import itertools


def featureExtractor(data, country):
    df = data['param_demand'].join(data['gas']).join(data['coal']).join(data['carbon']).join(
        data['temperature']).dropna().join(
        data['actual_productions_RE'][['ActualGenerationOutput ES Solar',
                                            'ActualGenerationOutput ES Wind Onshore',
                                            'ActualGenerationOutput ES Hydro Run-of-river and poundage']],
        how='left')
    existing_columns = df.columns.tolist()

    # Generate all possible combinations of existing columns
    column_combinations = list(itertools.combinations(existing_columns, 2))

    # Create new columns for the multiplication of existing column pairs
    df = df.join(pd.DataFrame({f'{col1}_{col2}_mult': df[col1] * df[col2] for col1, col2 in column_combinations}))

    df['datetime'] = df.index

    holidays_list = holidays.CountryHoliday(country)
    is_holiday = df.datetime.iloc[0] in holidays_list

    X = (df
         .join(pd.get_dummies(df.datetime.dt.day_name()))
         .join(pd.get_dummies(df.datetime.dt.hour))
         .assign(holiday=lambda x: x.datetime.dt.date.isin(holidays_list).astype(int))
         .set_index("datetime"))

    scaler = MinMaxScaler()
    scaled_X = pd.DataFrame(scaler.fit_transform(X.values), columns=X.columns, index=X.index)

    return X, scaled_X, scaler

def dateSlicer(data, country, start_date, finish_date):
    X, scaled_X, scaler = featureExtractor(data, country)
    features_for_selected_period = scaled_X.loc[start_date:finish_date]
    return features_for_selected_period

def featureExtractorFtuure(data, scenario_data, country, start_date, finish_date):
    X_historical, scaled_X_historical, scaler_historical = featureExtractor(data, country)
    X_future, scaled_X_future, scaler_future = featureExtractor(scenario_data, country)

    # Perform min-max scaling on X_future
    df_scaled = pd.DataFrame(scaler_historical.transform(X_future), index=X_future.index, columns=X_future.columns)

    features_for_selected_period = df_scaled.loc[start_date:finish_date]

    return features_for_selected_period