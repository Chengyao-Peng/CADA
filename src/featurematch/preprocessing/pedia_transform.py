import pandas as pd
import xlrd
import csv

with open("../../../data/raw/supplementary_table_PEDIA/SupplementaryTable1_03092019.csv", "wb") as myCsvfile:
    wr = csv.writer(myCsvfile, delimiter="\t")
    myfile = xlrd.open_workbook('../../../data/raw/supplementary_table_PEDIA/SupplementaryTable1_03092019.xlsx')
    mysheet = myfile.sheet_by_index(0)
    for rownum in range(mysheet.nrows):
        wr.writerow(mysheet.row_values(rownum))

# xls = pd.ExcelFile('../../../data/raw/supplementary_table_PEDIA/SupplementaryTable1_03092019.xlsx')
# df = pd.read_excel(xls, header=0)
# df = df[['Case ID', 'Submitter',  'HPO', 'HPO Features', 'Absent HPO', 'Absent HPO Features', 'Gene','Diagnosis']]

# for patient in df.values.tolist():
#     for element in patient:
#         # if isinstance(element, list):
#         #     print('oooooooooooo')
#         #     s = " ".join(element)
#         #     print(s)
#         # else:
#         #     (print(element))
#         print(element)
#     print("\n")
