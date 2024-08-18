from sklearn.cluster import DBSCAN, OPTICS
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler

def execute_isolation(input_data, n_estimators, max_samples, contamination='auto', max_features=1.0):
    # Create model
    model = isolation_forest(n_estimators, max_samples, contamination, max_features=1.0)

    return model.fit_predict(input_data)


def isolation_forest(n_estimators, max_samples, contamination='auto', max_features=1.0):
    model = IsolationForest(n_estimators=n_estimators,
                            max_samples=max_samples,
                            contamination=contamination,
                            max_features=max_features)

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