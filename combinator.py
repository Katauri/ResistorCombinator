from openpyxl import load_workbook

wb_val = load_workbook(filename = 'nominals.xlsx', data_only = True)

sheet_E24 = wb_val['E24']
sheet_E96 = wb_val['E96']
sheet_E192 = wb_val['E192']

sheets = (sheet_E24, sheet_E96, sheet_E192)

list_E24 = []
list_E96 = []
list_E192 = []
list_nominals = []

for sheet in sheets:
    num = 2
    while(sheet['A' + str(num)].value):

        if sheet == sheet_E24:
            list_E24.append(sheet['A' + str(num)].value)
            list_nominals.append((sheet['A' + str(num)].value, 5))
        elif sheet == sheet_E96:
            list_E96.append(sheet['A' + str(num)].value)
            list_nominals.append((sheet['A' + str(num)].value, 1))
        elif sheet == sheet_E192:
            list_E192.append(sheet['A' + str(num)].value)
            list_nominals.append((sheet['A' + str(num)].value, 0.5))
        num += 1

list_nominals.sort(key=lambda x: x[::1])

def serial_combine(value, dimension, tolerance, power, count):
    value_min = value * (1 - (tolerance / 100))
    value_max = value * (1 + (tolerance / 100))

    combinations_list = []
    tiers = [list_E24, list_E96, list_E192]

    count_list = []
    for i in range(count):
        count_list.append(1)

    for index in count_list:
        for i



    print(list_nominals)
    return combinations_list


output = serial_combine(value = 5, dimension = 'Ом', tolerance = 5, power = 0, count = 4)
print(output)

