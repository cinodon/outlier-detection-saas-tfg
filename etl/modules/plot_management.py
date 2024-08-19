import matplotlib.pyplot as plt

def get_plot(title, dataframe, path):
    create_anomaly_plot(title, dataframe)
    save_plot(path)

def create_anomaly_plot(title, dataframe):
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(dataframe['PC1'], dataframe['PC2'], c=dataframe['anomaly_score'], cmap='viridis', s=50, alpha=0.7)
    plt.colorbar(scatter, label='Anomaly Score (DBSCAN clusters)')
    plt.title(title)
    plt.xlabel('(PC1)')
    plt.ylabel('(PC2)')

def save_plot(path):
    plt.savefig(path)
    plt.close()

