from sklearn.cluster import DBSCAN, OPTICS
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler

def execute_isolation(input_data, n_estimators, max_samples, contamination='auto', max_features=1.0, bootstrap=True):
    # Create model
    model = isolation_forest(n_estimators, max_samples, contamination, max_features=max_features, bootstrap=bootstrap)

    return model.fit_predict(input_data)


def isolation_forest(n_estimators, max_samples, contamination='auto', max_features=1.0, bootstrap=True):
    model = IsolationForest(n_estimators=n_estimators,
                            max_samples=max_samples,
                            contamination=contamination,
                            max_features=max_features,
                            bootstrap=bootstrap,
                            random_state=42)

    return model

def execute_dbscan(input_data, eps, min_samples):
    # Create model
    model = dbscan(eps=eps, min_samples=min_samples)

    return model.fit_predict(input_data)


def dbscan(eps, min_samples):
    model = DBSCAN(eps=eps, min_samples=min_samples)

    return model

def scale_data(input_data):
    scaled_data = StandardScaler().fit_transform(input_data)
    return scaled_data

def execute_lof(input_data, n_neighbors):
    # Create model
    model = local_outlier_factor(n_neighbors)

    return model.fit_predict(input_data)


def local_outlier_factor(n_neighbors):
    model = LocalOutlierFactor(n_neighbors=n_neighbors)

    return model
