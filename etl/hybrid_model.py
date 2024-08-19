from modules import data_processing as dp
from modules import clustering_models as cm
from sklearn.model_selection import train_test_split
from sklearn.svm import OneClassSVM
import pandas as pd

# Load CSV for Models
model_input_df = dp.load_csv('./files/input/model-input-data.csv')

# Output data
output_dataframe = dp.load_csv('./files/output/output-base.csv')

# Split input data into train_data and test_data
train_data, test_data, output_train, output_test = train_test_split(model_input_df, output_dataframe, test_size=0.5, random_state=42)
# Supongamos que cm.scale_data devuelve arrays de NumPy
train_data_scaled = cm.scale_data(train_data)
test_data_scaled = cm.scale_data(test_data)

# Convertir los resultados a DataFrames si es necesario
train_data_scaled_df = pd.DataFrame(train_data_scaled, index=train_data.index, columns=train_data.columns)
test_data_scaled_df = pd.DataFrame(test_data_scaled, index=test_data.index, columns=test_data.columns)


# Run LOF with train_data
train_data_scaled_df['anomaly_score'] = cm.execute_lof(train_data_scaled_df, 10)

# Get only the inliers
inliers_data = train_data_scaled_df[train_data_scaled_df['anomaly_score'] == 1]

# SVM
# Prepare data
inliers_data = inliers_data.drop(columns=['anomaly_score'])

# Train SVM
svm_model = OneClassSVM(kernel='rbf', gamma='auto')
svm_model.fit(inliers_data)

# Predict on test_data with SVM
svm_test_data = test_data_scaled_df
predictions = svm_model.predict(svm_test_data)
svm_test_data['anomaly_score'] = predictions
output_test_svm = output_test
output_test_svm['anomaly_score'] = predictions

# Run LOF with test_data
lof_test_data = test_data_scaled_df
lof_test_data['anomaly_score'] = cm.execute_lof(lof_test_data, 10)
output_test_lof = output_test
output_test_lof['anomaly_score'] = lof_test_data['anomaly_score']

# Save data
dp.save_to_csv(output_test_svm, './files/output/hybrid_model/output_test_svm.csv')
dp.save_to_csv(output_test_lof, './files/output/hybrid_model/output_test_lof.csv')

# Compare results > get different rows
mismatch = dp.get_mismatches(output_test_svm, output_test_lof)
print(mismatch)

