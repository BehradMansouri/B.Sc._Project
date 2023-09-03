import matplotlib.pyplot as plt
import numpy as np
import math

##########################################################
main = {}

# Read region code
with open(r'D:\Clustering\Final\4 Histogram outputs\Main.csv') as fp:
    skip = 0
    for row in fp:
        if skip == 0:  # skip header
            skip += 1
            continue
        row = row.split('\n')[0]
        row = row.split(',')
        person_id = int(row[0])
        region_code = int(row[1])
        number_of_units = int(row[2])
        measured_area = int(row[3])
        main[person_id, 0] = region_code
        main[person_id, 1] = number_of_units
        main[person_id, 2] = measured_area


##########################################################
# Read Cluster Data to histogram
def readData(path, clustering_dimensions):
    skip2 = 0
    region_data = []
    unit_data = []
    area_data = []
    usage_data = []
    real_usage_data = []
    with open(path, encoding="utf-8") as file:
        for line in file:
            if skip2 == 0:  # skip header
                skip2 += 1
                continue
            line = line.split('\n')[0]
            line = line.split(',')
            user_id = int(line[0])
            region = main[user_id, 0]
            units = main[user_id, 1]
            area = main[user_id, 2]
            usage_list1 = np.array(line[1:]).astype(float)
            if clustering_dimensions == 12:
                usage_list2 = np.array(line[1:5]).astype(float)
                usage = (sum(usage_list1) * 2) + (sum(usage_list2) * 1)
            elif clustering_dimensions == 28:
                usage = sum(usage_list1)
            real_usage = usage * units
            region_data.append(region)
            unit_data.append(units)
            area_data.append(area)
            usage_data.append(usage)
            real_usage_data.append(real_usage)
        return region_data, unit_data, area_data, usage_data, real_usage_data


##########################################################
def showPlt(data, dimension, number_of_clusters):
    plt.figure()

    # Define the colours of our clusters. Add more colors if needed.
    colors1 = ['blue', 'green', 'orange', 'red', 'purple']
    colors2 = ['deepskyblue', 'lawngreen', 'gold', 'orangered', 'mediumpurple']
    colors3 = ['darkblue', 'yellowgreen', 'darkgoldenrod', 'darkred', 'plum']
    colors4 = ['aqua', 'lime', 'goldenrod', 'crimson', 'magenta']
    labels = []

    # define the bins for out histograms
    region_bins = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    unit_bins = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 3000]
    area_bins = [25]
    for i in range(35, 72):
        area_bins.append(math.floor(10 ** (i / 20)))
    area_bins.append(10000)
    usage_bins = []
    for i in range(10, 23):
        usage_bins.append(math.floor(10 ** (i / 8)))
    for i in range(115, 186):
        usage_bins.append(math.floor(10 ** (i / 40)))
    real_usage_bins = []
    for i in range(56, 140):
        real_usage_bins.append(math.floor(10 ** (i / 25)))

    # correct the tick positions of our bar charts to turn them into histograms
    region_ticks = np.arange(len(region_bins)) + 1
    unit_ticks = np.arange(len(unit_bins)) + 0.5
    area_ticks = np.arange(len(area_bins)) + 0.5
    usage_ticks = np.arange(len(usage_bins)) + 0.5
    real_usage_ticks = np.arange(len(real_usage_bins)) + 0.5

    # we define our bin height variables
    region_population_list = []
    unit_population_list = []
    area_population_list = []
    usage_population_list = []
    real_usage_population_list = []
    region_total_headcount = np.zeros(len(region_bins), dtype=int)
    normalized_region_population_list = [[] for _ in range(0, number_of_clusters)]              # [[],[],[]] or [[],[],[],[]] depending of number of clusters
    unit_total_headcount = np.zeros(len(unit_bins) - 1, dtype=int)
    normalized_unit_population_list = [[] for _ in range(0, number_of_clusters)]                # [[],[],[]] or [[],[],[],[]] depending of number of clusters

    for current_cluster, user_data in enumerate(data):  # for _, (region_data, unit_data) in enumerate(user_data):
        # Find the population of each region bin, for all of our clusters
        region_headcount = [user_data[0].count(region) for region in region_bins]
        region_population_list.append(region_headcount)
        region_total_headcount = np.sum([region_total_headcount, region_headcount], axis=0)

        # Find the population of each unit bin, for all of our clusters
        unit_headcount = np.zeros(len(unit_bins) - 1, dtype=int)
        for i in range(0, len(user_data[1])):
            for j in range(0, len(unit_bins) - 1):
                if unit_bins[j] <= user_data[1][i] < unit_bins[j + 1]:
                    unit_headcount[j] += 1
                    continue
        unit_population_list.append(unit_headcount)
        unit_total_headcount = np.sum([unit_total_headcount, unit_headcount], axis=0)

        # Find the population of each area bin, for all of our clusters
        area_headcount = np.zeros(len(area_bins) - 1, dtype=int)
        for i in range(0, len(user_data[2])):
            for j in range(0, len(area_bins) - 1):
                if area_bins[j] <= user_data[2][i] < area_bins[j + 1]:
                    area_headcount[j] += 1
                    continue
        area_population_list.append(area_headcount)

        # Find the population of each usage bin, for all of our clusters
        usage_headcount = np.zeros(len(usage_bins) - 1, dtype=int)
        for i in range(0, len(user_data[3])):
            for j in range(0, len(usage_bins) - 1):
                if usage_bins[j] <= user_data[3][i] < usage_bins[j + 1]:
                    usage_headcount[j] += 1
                    continue
        usage_population_list.append(usage_headcount)

        # Find the population of each "real" usage bin (usage not divided by unit count), for all of our clusters
        real_usage_headcount = np.zeros(len(real_usage_bins) - 1, dtype=int)
        for i in range(0, len(user_data[4])):
            for j in range(0, len(real_usage_bins) - 1):
                if real_usage_bins[j] <= user_data[4][i] < real_usage_bins[j + 1]:
                    real_usage_headcount[j] += 1
                    continue
        real_usage_population_list.append(real_usage_headcount)

        labels.append(f'Cluster {current_cluster + 1}')

    # Normalize the population list our region bins, for all of our cumulative data
    for i in range(0, number_of_clusters):
        for j in range(0, len(region_bins)):
            normalized_region_population_list[i].append(region_population_list[i][j] * 950000 / region_total_headcount[j])

    # Normalize the population list our unit bins, for all of our cumulative data
    for i in range(0, number_of_clusters):
        for j in range(0, len(unit_bins) - 1):
            normalized_unit_population_list[i].append(unit_population_list[i][j] * 9500 / unit_total_headcount[j])

    bottom = None
    for i, population in enumerate(region_population_list):
        plt.bar(region_bins, population, bottom=bottom, width=0.75, color=colors1[i], alpha=0.5, label=labels[i])
        plt.xticks(region_ticks, region_bins)
        if bottom is None:
            bottom = population
        else:
            bottom = [b + c for b, c in zip(bottom, population)]
    plt.xlabel("Region")
    plt.ylabel("Number of users")
    plt.legend()
    plt.title(f'{dimension} Dimensional clustering - {number_of_clusters} Clusters - All users')
    plt.show()

    bottom = None
    for i, population in enumerate(normalized_region_population_list):
        plt.bar(region_bins, population, bottom=bottom, width=0.75, color=colors1[i], alpha=0.5, label=labels[i])
        plt.xticks(region_ticks, region_bins)
        plt.ylim([0, 1000000])
        if bottom is None:
            bottom = population
        else:
            bottom = [b + c for b, c in zip(bottom, population)]
    plt.xlabel("Region")
    plt.ylabel("Normalized number of users")
    plt.legend()
    plt.title(f'{dimension} Dimensional clustering - {number_of_clusters} Clusters - All users')
    plt.show()

    bottom = None
    for i, population in enumerate(unit_population_list):
        plt.bar(range(1, 12), population, bottom=bottom, width=0.98, color=colors2[i], alpha=0.5, label=labels[i])
        plt.xticks(unit_ticks, unit_bins)
        if bottom is None:
            bottom = population
        else:
            bottom = [b + c for b, c in zip(bottom, population)]
    plt.xlabel("Units")
    plt.ylabel("Number of users")
    plt.legend()
    plt.title(f'{dimension} Dimensional clustering - {number_of_clusters} Clusters - All users')
    plt.show()

    bottom = None
    for i, population in enumerate(normalized_unit_population_list):
        plt.bar(range(1, 12), population, bottom=bottom, width=0.98, color=colors2[i], alpha=0.5, label=labels[i])
        plt.xticks(unit_ticks, unit_bins)
        plt.ylim([0, 10000])
        if bottom is None:
            bottom = population
        else:
            bottom = [b + c for b, c in zip(bottom, population)]
    plt.xlabel("Units")
    plt.ylabel("Normalized number of users")
    plt.legend()
    plt.title(f'{dimension} Dimensional clustering - {number_of_clusters} Clusters - All users')
    plt.show()

    bottom = None
    for i, population in enumerate(area_population_list):
        plt.bar(range(1, 39), population, bottom=bottom, width=0.96, color=colors3[i], alpha=0.5, label=labels[i])
        plt.xticks(area_ticks, area_bins, rotation=30)
        if bottom is None:
            bottom = population
        else:
            bottom = [b + c for b, c in zip(bottom, population)]
    plt.xlabel("Area in square meters")
    plt.ylabel("Number of users")
    plt.legend()
    plt.title(f'{dimension} Dimensional clustering - {number_of_clusters} Clusters - All users')
    plt.show()

    bottom = None
    for i, population in enumerate(usage_population_list):
        plt.bar(range(1, 84), population, bottom=bottom, width=0.933, color=colors4[i], alpha=0.5, label=labels[i])
        plt.xticks(usage_ticks, usage_bins, rotation=75)
        plt.ylim([0, 15000])
        if bottom is None:
            bottom = population
        else:
            bottom = [b + c for b, c in zip(bottom, population)]
    plt.xlabel("Total usage across 3 years (divided by unit count)")
    plt.ylabel("Number of users")
    plt.legend()
    plt.title(f'{dimension} Dimensional clustering - {number_of_clusters} Clusters - All users')
    plt.show()

    bottom = None
    for i, population in enumerate(real_usage_population_list):
        plt.bar(range(1, 84), population, bottom=bottom, width=0.933, color=colors4[i], alpha=0.5, label=labels[i])
        plt.xticks(real_usage_ticks, real_usage_bins, rotation=75)
        plt.ylim([0, 17500])
        if bottom is None:
            bottom = population
        else:
            bottom = [b + c for b, c in zip(bottom, population)]
    plt.xlabel("Real total usage across 3 years")
    plt.ylabel("Number of users")
    plt.legend()
    plt.title(f'{dimension} Dimensional clustering - {number_of_clusters} Clusters - All users')
    plt.show()


##########################################################
if __name__ == '__main__':
    dimensions = 12
    Cluster_number = 4
    Cluster_data = [[] for _ in range(0, Cluster_number)]
    Cluster_data_list = []
    for k in range(0, Cluster_number):
        Cluster_data[k] = readData(fr'D:\Clustering\Final\3 Output clusters\{dimensions} Dimensional\CSV files\{Cluster_number}_{k + 1}.csv', dimensions)
        Cluster_data_list.append(Cluster_data[k])
    showPlt(Cluster_data_list, dimensions, Cluster_number)
