import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN
import plotly.express as px

# df = pd.read_csv('../Data/Motor3Vibrator.csv')
#
# ## To be removed ##
# df['index'] = range(0, len(df))
# ##               ##
#
# vibe_time = df[['vibration (mm/s)', 'index']]
# vibe, timee = df['vibration (mm/s)'], df['index']
#
# plt.scatter(timee,vibe)
# plt.savefig('./plt.png')
#
# X = vibe_time.to_numpy()
# print(X.shape)
#
# dbscan_cluster_model = DBSCAN(eps=3, min_samples=5).fit(X)
# df['cluster'] = dbscan_cluster_model.labels_
# print(df['cluster'].value_counts())
#
# fig = px.scatter(x=timee, y=vibe, color=df['cluster'])
# fig.write_image('./pltcolor.png')