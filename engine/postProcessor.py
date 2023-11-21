import plotly.graph_objects as go
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
# Simulation:
# Show demand, RoR, wind, solar, temperature, captured solar, captured wind, captured ror
# OoS: PEs, PEw

def plot_and_calculate_errors(indices, param_real_prices, param_predicted_prices, title):
    # Create the plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=indices, y=param_real_prices, mode='lines', name='Real Prices'))
    fig.add_trace(go.Scatter(x=indices, y=param_predicted_prices, mode='lines', name='Predicted Prices'))

    # Set the plot layout
    fig.update_layout(
        title= title,
        xaxis_title='Index',
        yaxis_title='Price',
        showlegend=True
    )

    # Display the plot
    fig.show()

    # Calculate MAE
    mae = np.mean(np.abs(param_real_prices - param_predicted_prices))
    # Calculate NMAE
    nmae = mae / np.mean(np.abs(param_real_prices))

    # Store MAE and NMAE in a dictionary
    results = {
        'MAE': mae,
        'NMAE': nmae
    }

    return results


def calculate_capture(param_generation_renewable, param_prices, indeces):
    # Calculate revenue for renewable generation
    revenue = param_generation_renewable.values * param_prices

    # Create the DataFrame with the columns
    df = pd.DataFrame({
        'revenue': revenue,
        'generation': param_generation_renewable,
    }, index=indeces)

    # Calculate the capture values per day
    df_capture = pd.DataFrame()
    df_capture['revenue_per_day'] = df['revenue'].groupby(pd.Grouper(freq='D')).sum()
    df_capture['generation_per_day'] = df['generation'].groupby(pd.Grouper(freq='D')).sum()

    # Calculate captured_price
    df_capture['captured_price'] = df_capture['revenue_per_day'] / df_capture['generation_per_day']

    # Replace NaN (from division by zero) with 0
    df_capture['captured_price'] = np.where(df_capture['generation_per_day'] == 0, 0, df_capture['captured_price'])

    return df_capture['captured_price']

def replace_zero(row):
    # If there are any zeros in the row
    if 0 in row.values:
        non_zero_values = row[row != 0].values
        # If there are any non-zero values in the row
        if len(non_zero_values) > 0:
            value_to_use = np.random.choice(non_zero_values)
            random_multiplier = np.random.uniform(0.95, 1.05)
            value_to_replace = value_to_use * random_multiplier
            row[row == 0] = value_to_replace
    return row

def plot_prices(dict_foewardModel, data, start_date_test, finish_date_test):
    indices = data['param_real_prices'].loc[start_date_test:finish_date_test].index
    # Parameters
    param_real_prices = data['param_real_prices'].loc[start_date_test:finish_date_test].values
    param_real_prices = param_real_prices.reshape(-1)
    param_predicted_prices = dict_foewardModel['out_predicted_prices']

    plot_and_calculate_errors(indices, param_real_prices, param_predicted_prices, title = 'Real Prices vs Predicted Prices')



# This function calculates solar and wind capture prices
def plot_captured_prices(dict_foewardModel, data, start_date_test, finish_date_test):
    # Select the relevant data within the desired date range
    df_prices = data['param_real_prices'].loc[start_date_test:finish_date_test]
    df_generation_solar = data['actual_productions_RE']['ActualGenerationOutput ES Solar'].loc[
                          start_date_test:finish_date_test]
    df_generation_wind = data['actual_productions_RE']['ActualGenerationOutput ES Wind Onshore'].loc[
                         start_date_test:finish_date_test]

    # Calculate the revenue for solar and wind generation
    param_real_prices = df_prices.values.reshape(-1)
    param_predicted_prices = dict_foewardModel['out_predicted_prices']
    revenue_solar = df_generation_solar.values * param_real_prices
    revenue_pr_solar = df_generation_solar.values * param_predicted_prices
    revenue_wind = df_generation_wind.values * param_real_prices
    revenue_pr_wind = df_generation_wind.values * param_predicted_prices

    # Create the DataFrame with the columns
    df = pd.DataFrame({
        'revenue_solar': revenue_solar,
        'revenue_pr_solar': revenue_pr_solar,
        'revenue_wind': revenue_wind,
        'revenue_pr_wind': revenue_pr_wind,
        'generation_solar': df_generation_solar,
        'generation_wind': df_generation_wind
    }, index=df_prices.index)

    # Calculate the capture values per day
    df_capture = pd.DataFrame()
    df_capture['revenue_solar_per_day'] = df['revenue_solar'].groupby(pd.Grouper(freq='D')).sum()
    df_capture['revenue_pr_solar_per_day'] = df['revenue_pr_solar'].groupby(pd.Grouper(freq='D')).sum()
    df_capture['total_solar_generation'] = df['generation_solar'].groupby(pd.Grouper(freq='D')).sum()
    df_capture['capture_solar'] = df_capture['revenue_solar_per_day'] / df_capture['total_solar_generation']
    df_capture['capture_pr_solar'] = df_capture['revenue_pr_solar_per_day'] / df_capture['total_solar_generation']
    df_capture['revenue_wind_per_day'] = df['revenue_wind'].groupby(pd.Grouper(freq='D')).sum()
    df_capture['revenue_pr_wind_per_day'] = df['revenue_pr_wind'].groupby(pd.Grouper(freq='D')).sum()
    df_capture['total_wind_generation'] = df['generation_wind'].groupby(pd.Grouper(freq='D')).sum()
    df_capture['capture_wind'] = df_capture['revenue_wind_per_day'] / df_capture['total_wind_generation']
    df_capture['capture_pr_wind'] = df_capture['revenue_pr_wind_per_day'] / df_capture['total_wind_generation']

    plot_and_calculate_errors(df_prices.index, param_real_prices = df_capture['capture_wind'], param_predicted_prices = df_capture['capture_pr_wind'], title = 'Real Wind Prices vs Predicted Prices')
    plot_and_calculate_errors(df_prices.index, param_real_prices = df_capture['capture_solar'], param_predicted_prices = df_capture['capture_pr_solar'], title = 'Real Solar Prices vs Predicted Prices')

# Function for making a table for out of sample test
def summary_table(dict_foewardModel, data, start_date_test, finish_date_test):
    param_real_prices = data['param_real_prices'].loc[start_date_test:finish_date_test].values
    param_real_prices = param_real_prices.reshape(-1)
    param_predicted_prices = dict_foewardModel['out_predicted_prices']
    indices = data['param_real_prices'].loc[start_date_test:finish_date_test].index

    # Create a data frame which separates days and hours
    df_compare = pd.DataFrame(param_real_prices, columns=['real prices'], index=indices) \
        .assign(predicted_prices=param_predicted_prices,
                weekday=lambda x: x.index.weekday,
                hour=lambda x: x.index.hour,
                month=lambda x: x.index.month)

    # Calculate NMAE
    mae = np.mean(np.abs(param_real_prices - param_predicted_prices))
    nmae = mae / np.mean(np.abs(param_real_prices))

    # Create a data frame and store the results
    summary_data = []

    weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    for hour in range(24):
        prices = df_compare[df_compare['hour'] == hour]['real prices']
        predicted_prices = df_compare[df_compare['hour'] == hour]['predicted_prices']
        nmae_hour = np.mean(np.abs(prices - predicted_prices)) / np.mean(np.abs(prices))
        summary_data.append({'Criteria': f'h{hour:02}', 'NMAE': nmae_hour})

    for weekday in range(7):
        prices = df_compare[df_compare['weekday'] == weekday]['real prices']
        predicted_prices = df_compare[df_compare['weekday'] == weekday]['predicted_prices']
        nmae_weekday = np.mean(np.abs(prices - predicted_prices)) / np.mean(np.abs(prices))
        summary_data.append({'Criteria': f'{weekday_names[weekday]}', 'NMAE': nmae_weekday})

    summary_data.append({'Criteria': 'NMAE', 'NMAE': nmae})

    summary_df = pd.DataFrame(summary_data)

    return summary_df

### Graphs for scenarios ###
def graph(df, graph_type, light, medium, dark, title, Y_Axis_Title):
    # df = pd.read_excel(r'report_example.xlsx', sheet_name=graph_type)
    # df.index = df['dates']
    # df = df[start_date:end_date]
    df['0.95'] = df.iloc[:, :].dropna().quantile(q=.95, axis=1)
    df['0.05'] = df.iloc[:, :].dropna().quantile(q=.05, axis=1)
    df['0.5'] = df.iloc[:, :].dropna().quantile(q=.5, axis=1)
    df['0.25'] = df.iloc[:, :].dropna().quantile(q=.25, axis=1)
    df['0.75'] = df.iloc[:, :].dropna().quantile(q=.75, axis=1)
    fig = go.Figure()
    fig.add_traces(
        go.Scatter(x=df.index, y=df['0.05'], line=dict(color=medium, width=0), showlegend=False,
                   mode='lines', name='Q 0.05'))
    fig.add_traces(
        go.Scatter(x=df.index, y=df['0.95'], fill='tonexty', line=dict(color=medium, width=0),
                   mode='lines', name='Q 0.95'))
    fig.add_traces(
        go.Scatter(x=df.index, y=df['0.5'], line=dict(color=dark, width=1), mode='lines',
                   name='Q 0.5'))
    fig.add_traces(
        go.Scatter(x=df.index, y=df['0.25'], fill='tonexty', line=dict(color=medium, width=0),
                   mode='lines', name='Q 0.25'))
    fig.add_traces(
        go.Scatter(x=df.index, y=df['0.75'], fill='tonexty', line=dict(color=light, width=0),
                   mode='lines', name='Q 0.75'))
    # fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)', })
    fig.update_layout({'plot_bgcolor': 'rgb(250,250,250)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)', })
    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99))
    fig.update_layout(title={'text': title, 'y': 0.95, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                      yaxis_title=Y_Axis_Title,
                      )
    fig.show()


import matplotlib.pyplot as plt


def create_histogram(dataframe, title_histo, color):
    import numpy as np
    import plotly.express as px

    # Assuming 'dataframe' is your numpy array
    dataframe = np.nan_to_num(dataframe, nan=0)
    dataframe = dataframe.reshape(-1)  # Reshape to one dimension
    dataframe = dataframe[dataframe != 0]

    # Define your title and Y-axis title
    title = title_histo
    Y_Axis_Title = 'Frequency'

    # Create a histogram using Plotly Express and set the bar color
    fig = px.histogram(dataframe, nbins=30, opacity=0.7)
    fig.update_traces(marker_color=color)

    # Update axis labels and title
    fig.update_xaxes(title_text='Values')
    fig.update_yaxes(title_text=Y_Axis_Title)

    # Update legend position
    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99))

    # Update title and Y-axis title position
    fig.update_layout(
        title={'text': title, 'y': 0.95, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
        yaxis_title=Y_Axis_Title
    )

    # Update background colors
    fig.update_layout(
        plot_bgcolor='rgb(250,250,250)',
        paper_bgcolor='rgba(0, 0, 0, 0)'
    )

    # Show the plot
    fig.show()


def plotScenarios(data_scenarios, num_scenarios):
    # Create an empty DataFrame
    df_demand = pd.DataFrame()
    df_temperature = pd.DataFrame()
    df_solar = pd.DataFrame()
    df_wind = pd.DataFrame()
    df_ror = pd.DataFrame()
    df_price = pd.DataFrame()
    df_solar_price = pd.DataFrame()
    df_wind_price = pd.DataFrame()

    # Iterate over the scenarios
    for i in range(num_scenarios):
        scenario_key = f'scenario_{i + 1}'

        # Extract the "param_demand" values for the current scenario
        param_demand_values = data_scenarios[scenario_key]['param_demand']
        df_demand[scenario_key] = param_demand_values

        # Extract the "temperature" values for the current scenario
        temperature_values = data_scenarios[scenario_key]['temperature']
        df_temperature[scenario_key] = temperature_values

        # Extract the "solar" values for the current scenario
        solar_values = data_scenarios[scenario_key]['actual_productions_RE']['ActualGenerationOutput ES Solar']
        df_solar[scenario_key] = solar_values

        # Extract the "wind" values for the current scenario
        wind_values = data_scenarios[scenario_key]['actual_productions_RE']['ActualGenerationOutput ES Wind Onshore']
        df_wind[scenario_key] = wind_values

        # Extract the "ror" values for the current scenario
        ror_values = data_scenarios[scenario_key]['actual_productions_RE']['ActualGenerationOutput ES Hydro Run-of-river and poundage']
        df_ror[scenario_key] = ror_values

        # Extract the "prices" values for the current scenario
        prices_values = data_scenarios[scenario_key]['param_real_prices']
        df_price[scenario_key] = prices_values

        # Extract the "captured solar prices" values for the current scenario
        solar_captured_values = calculate_capture(solar_values, prices_values, df_solar.index)
        df_solar_price[scenario_key] = solar_captured_values

        # Extract the "captured solar prices" values for the current scenario
        wind_captured_values = calculate_capture(wind_values, prices_values, df_wind.index)
        df_wind_price[scenario_key] = wind_captured_values

    df_demand = df_demand.apply(replace_zero, axis=1)
    df_temperature = df_temperature.apply(replace_zero, axis=1)
    df_solar = df_solar.apply(replace_zero, axis=1)
    df_wind = df_wind.apply(replace_zero, axis=1)
    df_ror = df_ror.apply(replace_zero, axis=1)
    df_price = df_price.apply(replace_zero, axis=1)
    df_solar_price = df_solar_price.apply(replace_zero, axis=1)
    df_wind_price = df_wind_price.apply(replace_zero, axis=1)

    # Histograms
    create_histogram(df_solar_price, title_histo = "Distribution of Solar Capture Prices", color='rgb(255, 161, 65)')
    create_histogram(df_wind_price, title_histo = "Distribution of Wind Capture Prices", color='rgb(115, 210, 255)')
    # Graphs
    graph(df_solar_price, 'Capture_price_solar', 'rgb(255, 161, 65)', 'rgb(255, 242, 228)', 'rgb(255, 128, 0)','Solar capture price', '(EUR per MWh)')
    graph(df_wind_price, 'Capture_price_wind', 'rgb(115, 210, 255)', 'rgb(202, 238, 255)', 'rgb(30, 180, 255)', 'Wind capture price',
          '(EUR per MWh)')
    graph(df_price, 'price', 'rgb(164, 232, 198)', 'rgb(230, 247, 239)', 'rgb(0, 153, 76)', 'Day-ahead pricees',
          '(EUR per MWh)')
    graph(df_demand, 'demand', 'rgb(255, 153, 153)', 'rgb(255, 204, 204)', 'rgb(255, 102, 102)', 'Demand Scenarios', 'MW')
    graph(df_temperature, 'temperature', 'rgb(115, 157, 255)', 'rgb(202, 220, 255)', 'rgb(30, 136, 255)', 'Temperature Scenarios',
          'Celsius (°C)')
    graph(df_solar, 'solar_Generation', 'rgb(255, 161, 65)', 'rgb(255, 242, 228)', 'rgb(255, 128, 0)',
          'Solar Generation Scenarios', 'MW')
    graph(df_wind, 'wind onshore_Generation', 'rgb(115, 210, 255)', 'rgb(202, 238, 255)', 'rgb(30, 180, 255)',
          'Wind Generation Scenarios', 'MW')
    graph(df_ror, 'ror_Generation', 'rgb(153, 204, 255)', 'rgb(204, 229, 255)', 'rgb(102, 178, 255)',
          'RoR Generation Scenarios', 'MW')