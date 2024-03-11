import numpy as np
from sklearn.cluster import KMeans

def perform_clustering_and_create_transition_matrix(errors, cluster_count):
    """
    Performs KMeans clustering on the provided error data and creates a transition matrix.

    Parameters:
    - errors: DataFrame containing the error data for clustering.
    - cluster_count: Number of clusters to use in KMeans.

    Returns:
    - kmeans_model: The trained KMeans model.
    - transition_matrix: The created transition matrix.
    """
    # Perform KMeans Clustering
    kmeans_model = KMeans(n_clusters=cluster_count)
    kmeans_model.fit(errors)

    # Create Transition Matrix
    transition_matrix = np.zeros((cluster_count, cluster_count))
    for i in np.c_[kmeans_model.labels_[:-1], kmeans_model.labels_[1:]]:
        transition_matrix[i[0], i[1]] += 1
    if (transition_matrix.sum(axis=0) == 0).any():
        raise Exception("Non-ergodic Markov chain for transitions between clusters.")
    transition_matrix = transition_matrix.cumsum(axis=1)

    return kmeans_model, transition_matrix