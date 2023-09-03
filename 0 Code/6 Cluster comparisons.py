import glob
import os
import plotly.graph_objects as go

################################################################################################
_12_3 = []  # [{3_1},{3_2},{3_3}]
_12_4 = []  # [{4_1},{4_2},{4_3},{4_4}]
_28_3 = []
_28_4 = []


################################################################################################
def readFile(path):
    skip = 0
    s = set()
    with open(path, encoding="utf-8") as fp:
        for line in fp:
            if skip == 0:  # skip header
                skip += 1
                continue
            user_id = line.split(',')[0]
            s.add(user_id)
    return s


################################################################################################
def readFolder(main_path):
    files = glob.glob(os.path.join(main_path, '*.csv'))
    for file in files:
        s = readFile(file)
        if file.count('3_') > 0 and file.count('12 Dimensional') > 0:
            _12_3.append(s)
        elif file.count('4_') > 0 and file.count('12 Dimensional') > 0:
            _12_4.append(s)
        elif file.count('3_') > 0 and file.count('28 Dimensional') > 0:
            _28_3.append(s)
        elif file.count('4_') > 0 and file.count('28 Dimensional') > 0:
            _28_4.append(s)


################################################################################################
def compare(c1: set, c2: set):  # C1 C14
    c = c1.intersection(c2)
    u1 = (len(c) / len(c2)) * 100
    u2 = (len(c) / len(c1)) * 100
    return u1, u2


################################################################################################
if __name__ == '__main__':

    link = [[] for _ in range(0, 4)]        # [[],[],[],[]]
    nodes = [[] for _ in range(0, 4)]       # [[],[],[],[]]
    thicknesses = [[] for _ in range(0, 4)]  # [[],[],[],[]]

    colors = [[] for _ in range(0, 4)]       # [[],[],[],[]]
    color_input = [['deepskyblue', 'blue', 'darkblue', 'aqua'], ['lime',  'lawngreen', 'green', 'yellowgreen'],
                   ['orange', 'goldenrod', 'gold', 'darkgoldenrod'], ['darkred', 'orangered', 'red', 'crimson']]
    # color_input = ['', '', '', 'aquamarine', '', '', 'forestgreen', 'mediumspringgreen', 'darkorange', '', '', '', '', '', '', '']

    readFolder(r'D:\Clustering\Final\3 Output clusters\12 Dimensional\CSV files')
    readFolder(r'D:\Clustering\Final\3 Output clusters\28 Dimensional\CSV files')

    ############################################################################################
    # compare the 12 dim clustering attempts with each other
    for i in range(len(_12_4)):
        for j in range(len(_12_3)):
            x, y = compare(_12_3[j], _12_4[i])
            link[0].append({'source': i + 3, 'target': j, 'value': x * len(_12_4[i])})
            colors[0].append(color_input[i][j])
            print(f"{x} percent of Cluster_12_4_{i + 1} is also present in Cluster_12_3_{j + 1}")
            print(f"{y} percent of Cluster_12_3_{j + 1} is also present in Cluster_12_4_{i + 1}")
            print('=======================================================')
    print('\n\n\n')

    ############################################################################################
    # compare the 28 dim clustering attempts with each other
    for i in range(len(_28_4)):
        for j in range(len(_28_3)):
            x, y = compare(_28_3[j], _28_4[i])
            link[1].append({'source': i + 3, 'target': j, 'value': x * len(_28_4[i])})
            colors[1].append(color_input[i][j])
            print(f"{x} percent of Cluster_28_4_{i + 1} is also present in Cluster_28_3_{j + 1}")
            print(f"{y} percent of Cluster_28_3_{j + 1} is also present in Cluster_28_4_{i + 1}")
            print('=======================================================')
    print('\n\n\n')

    ############################################################################################
    # compare the 28 dim clustering attempts with the 12 dim ones
    for i in range(len(_28_3)):
        for j in range(len(_12_3)):
            x, y = compare(_12_3[j], _28_3[i])
            link[2].append({'source': i + 3, 'target': j, 'value': x * len(_28_3[i])})
            colors[2].append(color_input[i][j])
            print(f"{x} percent of Cluster_28_3_{i + 1} is also present in Cluster_12_3_{j + 1}")
            print(f"{y} percent of Cluster_12_3_{j + 1} is also present in Cluster_28_3_{i + 1}")
            print('=======================================================')

    ############################################################################################
    # compare the 28 dim clustering attempts with the 12 dim ones, again
    for i in range(len(_28_4)):
        for j in range(len(_12_4)):
            x, y = compare(_12_4[j], _28_4[i])
            link[3].append({'source': i + 4, 'target': j, 'value': x * len(_28_4[i])})
            colors[3].append(color_input[i][j])
            print(f"{x} percent of Cluster_28_4_{i + 1} is also present in Cluster_12_4_{j + 1}")
            print(f"{y} percent of Cluster_12_4_{j + 1} is also present in Cluster_28_4_{i + 1}")
            print('=======================================================')

    # Define the names for each node
    for i in range(0, 3):
        nodes[0].append(fr'Cluster_12_3_{i+1}')
        nodes[1].append(fr'Cluster_28_3_{i+1}')

    for j in range(0, 4):
        nodes[0].append(fr'Cluster_12_4_{j+1}')
        nodes[1].append(fr'Cluster_28_4_{j+1}')

    # nodes[0] = ['Cluster_12_3_1', 'Cluster_12_3_2', 'Cluster_12_3_3',
    #            'Cluster_12_4_1', 'Cluster_12_4_2', 'Cluster_12_4_3', 'Cluster_12_4_4']
    # nodes[1] = ['Cluster_28_3_1', 'Cluster_28_3_2', 'Cluster_28_3_3',
    #            'Cluster_28_4_1', 'Cluster_28_4_2', 'Cluster_28_4_3', 'Cluster_28_4_4']
    nodes[2] = ['Cluster_12_3_1', 'Cluster_12_3_2', 'Cluster_12_3_3',
                'Cluster_28_3_1', 'Cluster_28_3_2', 'Cluster_28_3_3']
    nodes[3] = ['Cluster_12_4_1', 'Cluster_12_4_2', 'Cluster_12_4_3', 'Cluster_12_4_4',
                'Cluster_28_4_1', 'Cluster_28_4_2', 'Cluster_28_4_3', 'Cluster_28_4_4']

    for i in range(0, 4):
        # Define the links between nodes
        links = link[i]

        # Create the Sankey diagram
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=75,
                thickness=20,
                line=dict(color='black', width=0.5),
                label=nodes[i],
                color='black'),

            link=dict(
                source=[link['source'] for link in links],
                target=[link['target'] for link in links],
                value=[link['value'] for link in links],
                color=colors[i]))])

        # Customize the Sankey diagram layout
        fig.update_layout(
            title="Cluster Relationships",
            font=dict(size=30, color='black'),
            plot_bgcolor='white',
            paper_bgcolor='white')

        # Display the Sankey diagram
        fig.show()
