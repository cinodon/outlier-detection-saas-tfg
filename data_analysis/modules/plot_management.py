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
    print("Saving plot...")
    plt.savefig(image_path)
    plt.close()
    print("Plot saved successfully")


def get_plot3D(title, dataframe, path):
    create_anomaly_plot3D(title, dataframe)

    save_plot(path)

    plt.close()

def create_anomaly_plot3D(title, dataframe):
    # Create 3D plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    setup_plot_legend3D(ax, dataframe)

    # Add legend
    ax.legend(title="Anomaly Score")

    # Title and tags
    ax.set_title(title)
    ax.set_xlabel('PAR 1')
    ax.set_ylabel('PAR 2')
    ax.set_zlabel('PAR 3')

def setup_plot_legend3D(ax, dataframe):
    # Inliers
    ax.scatter(dataframe[dataframe['anomaly_score'] == 1]['VAR1'],
               dataframe[dataframe['anomaly_score'] == 1]['VAR2'],
               dataframe[dataframe['anomaly_score'] == 1]['VAR3'],
               color='#49E685', label='Inliers', s=30, alpha=0.5)

    # Outliers
    ax.scatter(dataframe[dataframe['anomaly_score'] == -1]['VAR1'],
               dataframe[dataframe['anomaly_score'] == -1]['VAR2'],
               dataframe[dataframe['anomaly_score'] == -1]['VAR3'],
               color='#E84C4C', label='Outliers', s=30, alpha=0.7)