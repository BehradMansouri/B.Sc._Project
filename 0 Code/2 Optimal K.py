import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


#############################################################
def readData(path):
    skip = 0
    data = []
    with open(path, encoding="utf-8") as fp:
        for line in fp:
            if skip == 0:  # skip header
                skip += 1
                continue
            line = line.split('\n')[0]
            line = line.split(',')
            user_data = np.array(line[1:]).astype(float)
            data.append(user_data)
    return data


##############################################
dimensions = 12    # Choose between 12 dimensional clustering and 28 dimensional clustering modes
df = readData(fr'D:\Clustering\Final\1 Pre-processing data\Output - {dimensions} dimensional\{dimensions} Dimensional data.csv')

distortions = []
silhouette_avg = []
for k in range(2, 10):
    kmeanModel = KMeans(init='random', n_clusters=k, n_init=50, max_iter=300)
    kmeanModel.fit(df)
    distortions.append(kmeanModel.inertia_)
    cluster_labels = kmeanModel.labels_
    silhouette_avg.append(silhouette_score(df, cluster_labels, metric='euclidean'))

print(distortions)
plt.figure(figsize=(16, 8))
plt.plot(range(2, 10), distortions, 'bx-')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('The Elbow method for finding the optimal K')
plt.show()
##################################################################################
plt.plot(range(2, 10), silhouette_avg, 'bx-')
plt.xlabel('k')
plt.ylabel('Silhouette score')
plt.title('Silhouette analysis for finding the optimal K')
plt.show()
##############################################
