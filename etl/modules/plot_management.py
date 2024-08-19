import matplotlib.pyplot as plt

def get_plot(title, dataframe, path):
    create_anomaly_plot(title, dataframe)

    # Save Figure
    save_plot(path)

    # Close
    plt.close()

def create_anomaly_plot(title, dataframe):
    # Create plot
    plt.figure(figsize=(10, 6))

    setup_plot_legend(dataframe)

    # Añadir la leyenda
    plt.legend(title="Anomaly Score")

    # Etiquetas y título
    plt.title(title)
    plt.xlabel('PC1')
    plt.ylabel('PC2')

def setup_plot_legend(dataframe):
    # Define Colors
    colors = {1: 'blue', -1: 'red'}

    # Config for legend
    plt.scatter(dataframe[dataframe['anomaly_score'] == 1]['PC1'],
                dataframe[dataframe['anomaly_score'] == 1]['PC2'],
                color=colors[1], label='Inliers', s=50, alpha=0.7)

    plt.scatter(dataframe[dataframe['anomaly_score'] == -1]['PC1'],
                dataframe[dataframe['anomaly_score'] == -1]['PC2'],
                color=colors[-1], label='Outliers', s=50, alpha=0.7)

def save_plot(image_path):
    plt.savefig(image_path)
    plt.close()


