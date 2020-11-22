from openpyxl import load_workbook

wb_val = load_workbook(filename = 'nominals.xlsx', data_only = True)
sheet_val = wb_val['Sheet1']
A1_val = sheet_val['A3'].value

def serial_combine(value, dimension, tolerance, power):
    pass

print(A1_val)