from modules import data_processing as dp

# Read dataframes
file_path0 = './files/output/DBSCAN/data/useful_data/real_useful5perc/DBSCAN-eps1.7-ms4.csv'
file_path1 = './files/output/LOF/data/LOF-n10.csv'
output_df0 = dp.load_csv(file_path0)
output_df1 = dp.load_csv(file_path1)


# Transform data if DBSCAN
if 'DBSCAN' in file_path0:
    output_df0['anomaly_score'] = output_df0['anomaly_score'].apply(lambda x: 1 if x != -1 else -1)
elif 'DBSCAN' in file_path1:
    output_df1['anomaly_score'] = output_df1['anomaly_score'].apply(lambda x: 1 if x != -1 else -1)

# Compare
mismatches = dp.get_mismatches(output_df0, output_df1)
print(mismatches)
