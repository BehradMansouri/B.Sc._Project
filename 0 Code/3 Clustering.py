import numpy as np
from sklearn.cluster import KMeans
import openpyxl


######################################################################################################
def read_data(path):
    id = []
    data = []
    skip = 0
    with open(path, encoding="utf-8") as fp:
        for line in fp:
            if skip == 0:  # skip header
                skip += 1
                continue
            line = line.split('\n')[0]
            line = line.split(',')
            user_id = line[0]
            user_data = np.array(line[1:]).astype(float)
            id.append(user_id)
            data.append(user_data)
    return id, data


###################################################
def assign_cluster(path, num_of_cluster):
    id, data = read_data(path)
    kmean_model = KMeans(init='random', n_clusters=num_of_cluster, n_init=100, max_iter=300)
    kmean_model.fit(data)
    label = list(kmean_model.labels_)   # List of what cluster each id falls int. looks something like [0, 1, 0, 2, 2, 0, 3, 1, 0, 2, 0, 3, 0, 3, 1, ...] for 4 cluster clustering attempts
    print(kmean_model.n_iter_)
    return id, data, label


###################################################
def save_clusters(id, data, label, num_of_cluster, clustering_mode):
    header = [u'ID', u'1st_month', u'2nd_month', u'3rd_month', u'4th_month', u'5th_month', u'6th_month', u'7th_month', u'8th_month', u'9th_month',
              u'10th_month', u'11th_month', u'12th_month']
    if clustering_mode == 28:  # fixing the 28 dimensional headers
        header = header + header[1:] + header[1:5]

    unsorted_cluster = [[] for _ in range(num_of_cluster)]  # [[],[],[]] or [[],[],[],[]] depending of number of clusters

    for i in range(len(label)):
        unsorted_cluster[label[i]].append([id[i], ] + list(data[i]))  # [[[id,usage1,usage2,usage3,...],[id,usage1,...],[id,usage1,...]...],[Cluster 2 users],[Cluster 3 users],[Cluster 4 users]]

    sorted_cluster = list(sorted(unsorted_cluster, key=len, reverse=True))
    i = 1
    for cluster in sorted_cluster:
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.append(header)
        for member in cluster:
            sheet.append(member)
        wb.save(fr'D:\Clustering\Final\3 Output clusters\{clustering_mode} Dimensional\{num_of_cluster}_{i}.xlsx')
        i += 1


###################################################
if __name__ == '__main__':
    dimensions = 12         # Choose between 12 dimensional clustering and 28 dimensional clustering modes
    Cluster_number = 5      # Choose the number of output clusters. 3 and 4 are the best values as determined by Elbow and Silhouette
    path = fr'D:\Clustering\Final\1 Pre-processing data\Output - {dimensions} dimensional\{dimensions} Dimensional data.csv'
    id, data, label = assign_cluster(path, Cluster_number)
    save_clusters(id, data, label, Cluster_number, dimensions)
