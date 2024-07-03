import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans

# Function gotten from https://youtu.be/iNlZ3IU5Ffw?si=Xu5nMiMEwdU9vJoC
def optimise_k_means(data, max_k):
    means = []
    inertias = []

    for k in range(1, max_k):
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(data)

        means.append(k)
        inertias.append(kmeans.inertia_)

    # Generate the elbow plot
    fig = plt.subplots(figsize=(10,5))
    plt.plot(means, inertias, 'o-')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Inertia')
    plt.grid(True)
    plt.savefig('./KMeansElbow.png')


df = pd.read_csv('../Data/Motor3Vibrator.csv', index_col='Date/Time')
df['index'] = range(0, len(df))

optimise_k_means(df[['vibration (mm/s)']], 10)

kmeans = KMeans(n_clusters=3)
kmeans.fit(df[['vibration (mm/s)']])
df['kmeans_3'] = kmeans.labels_

plt.clf()
plt.scatter(y=df['vibration (mm/s)'], x=df['index'], c=df['kmeans_3'])
plt.savefig('./KMeans3.png')