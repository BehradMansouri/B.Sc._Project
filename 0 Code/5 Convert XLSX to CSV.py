import jpype
import asposecells
import os
import pandas as pd


def convertXlsxTotCsv(main_path):
    for root, dirs, files in os.walk(main_path):
        for file in files:
            if file.endswith(".xlsx"):
                name = file.split('.')[0]
                path = os.path.join(root, file)
                read_file = pd.read_excel(path)
                csvfile = os.path.join(root, 'CSV files', name + '.csv')
                read_file.to_csv(csvfile, encoding='utf-8', index=False)


if __name__ == '__main__':
    jpype.startJVM()
    from asposecells.api import Workbook
    convertXlsxTotCsv(r'D:\Clustering\Final\3 Output clusters\12 Dimensional')
    convertXlsxTotCsv(r'D:\Clustering\Final\3 Output clusters\28 Dimensional')
    jpype.shutdownJVM()
