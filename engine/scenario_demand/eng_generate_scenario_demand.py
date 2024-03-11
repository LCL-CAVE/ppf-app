import pandas as pd
import numpy as np


def serve_eng_generate_scenario_demand(config,
                                       p,
                                       kmeans_model,
                                       transition_matrix,
                                       errors_,
                                       prediction_errors,
                                       demand_reg,
                                       qt,
                                       demand_profile):
    num_scenarios = config["num_scenarios"]
    scenario_start_date = config["scenario_start_date"]
    periods = config["periods"]
    cluster_count = config["cluster_count"]
    transition_frequency = config["transition_frequency"]
    number_of_periods = config["number_of_periods"]

    date_range = pd.date_range(scenario_start_date, periods=periods, freq=transition_frequency)
    clusters = pd.DataFrame(kmeans_model.labels_, columns=["label"]).reset_index().groupby("label")
    cluster_sizes = clusters.count()
    count = transition_matrix[:, -1]
    scenarios = pd.DataFrame()

    for s in range(num_scenarios):
        sample_size = len(date_range)
        sample = np.zeros((sample_size, p * number_of_periods))
        state = kmeans_model.labels_[np.random.randint(len(kmeans_model.labels_))]  # random starting state
        index = np.arange(cluster_count)
        for i in range(sample_size):
            state = index[np.random.randint(count[state]) < transition_matrix[state]][0]
            cluster = clusters.get_group(state)
            cluster_member_index = np.random.randint(cluster_sizes.loc[state])
            cluster_member_label = cluster.iloc[cluster_member_index].index[0]
            sample[i] = errors_[cluster_member_label]
        sample = sample.reshape((sample_size * number_of_periods, p))

        simulated_data = pd.DataFrame(sample,
                                      index=pd.date_range(scenario_start_date, periods=periods * number_of_periods,
                                                          freq="H", name="datetime"), columns=prediction_errors.columns)
        simulated_data['Actual Load'] += demand_reg.predict(simulated_data.index)
        simulated_data = pd.DataFrame(qt.inverse_transform(simulated_data.values), index=simulated_data.index,
                                      columns=simulated_data.columns)

        # simulated_data[generation_type] = simulated_data[generation_type] * RE_capacity_series
        # simulated_data['Actual Load'] = simulated_data.groupby(pd.Grouper(freq="D"))['Actual Load'].transform(lambda x: x.mul(demand_profile))
        ##########################
        unique_years = simulated_data.index.year.unique()

        # Iterate through each unique year
        for i, year in enumerate(unique_years):
            if i < len(demand_profile):  # Ensure there's a corresponding demand_profile value
                # Apply the transformation for the specific year
                simulated_data.loc[simulated_data.index.year == year, 'Actual Load'] = \
                    simulated_data[simulated_data.index.year == year].groupby(pd.Grouper(freq="D"))[
                        'Actual Load'].transform(lambda x: x * demand_profile[i])

        scenarios[f'scenario_{s + 1}'] = simulated_data['Actual Load']

    return scenarios
