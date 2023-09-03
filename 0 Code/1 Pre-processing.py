import openpyxl
import numpy as np
import random

donthave3years = []  # check if any 28 dimensional user has less than 3 years in data


########################################################
def random_selection(self, count):
    keys = list(self.All.keys())
    return random.sample(keys, count)


######################################
def data_reduce(All):
    reduce = {}
    a = random_selection(All, 100000)
    for key in a:
        reduce[key] = All[key]
    return reduce


###################################
def read_file(file, number_of_cluster):  # reads data from csv file
    All = {}
    total_years = {}
    skip = 0
    with open(file) as fp:
        for line in fp:
            if skip == 0:  # skip header
                skip += 1
                continue

            line = line.split('\n')[0]
            line = line.split(',')
            user_id = int(line[0])
            number_of_unit = int(line[1])
            year = int(line[2])

            if year == 88:
                data = np.array(line[3:7]).astype(float)
                if number_of_cluster == 12:
                    data = np.append(data, np.zeros(8, dtype=float), axis=0)
            else:
                data = np.array(line[3:]).astype(float)
            data_per_unit = data / number_of_unit

            if user_id not in All:
                All[user_id] = data_per_unit
                total_years[user_id] = 1
            elif number_of_cluster == 12:
                All[user_id] = np.sum([All[user_id], data_per_unit], axis=0)
                total_years[user_id] += 1
            elif number_of_cluster == 28:
                All[user_id] = np.append(All[user_id], data_per_unit, axis=0)
                total_years[user_id] += 1

    if number_of_cluster == 12:
        for key in All:
            for i in range(0, 4):
                All[key][i] = All[key][i] / 3
            for j in range(4, 12):
                All[key][j] = All[key][j] / 2
    for key in All:
        if total_years[key] < 3:
            donthave3years.append(key)
    print(len(donthave3years))

    return All


###################################
def save(All, reduce_mode, clustering_mode, filename, donthave3years):
    wb = openpyxl.Workbook()
    header = [u'ID', u'1st_month', u'2nd_month', u'3rd_month', u'4th_month', u'5th_month', u'6th_month', u'7th_month', u'8th_month', u'9th_month',
              u'10th_month', u'11th_month', u'12th_month']
    if clustering_mode == 28:  # fixing the 28 dimensional headers
        header = header + header[1:] + header[1:5]
    sheet = wb.active
    sheet.append(header)
    if reduce_mode == 0:
        mydictionary = All
    else:
        mydictionary = data_reduce(All)

    for key in mydictionary:
        if key not in donthave3years:
            sheet.append([key] + list(All[key]))

    wb.save(filename)


##############################################################

if __name__ == '__main__':
    dimensions = 12  # Choose between 12 dimensional pre-processing and 28 dimensional pre-processing modes
    mode = 0  # Choose whether our data should be reduced or not. mode = 1 for no data reduction, mode = 0 for data reduction
    input_filename = fr'D:\Clustering\Final\1 Pre-processing data\Input\Input data.csv'
    output_filename = fr'D:\Clustering\Final\1 Pre-processing data\Output - {dimensions} dimensional\{dimensions} Dimensional data.xlsx'
    All = read_file(input_filename, dimensions)
    save(All, mode, dimensions, output_filename, donthave3years)
