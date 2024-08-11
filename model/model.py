import pandas as pd
import numpy
from sklearn.ensemble import IsolationForest

# Leer el archivo CSV
df = pd.read_csv('/app/model/files/data-model.csv')

# Convertir los datos a un array NumPy
input_data = df.values
