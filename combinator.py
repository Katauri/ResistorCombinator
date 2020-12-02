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

list_nominals.sort(key = lambda x: x[::1])


def serial_combine(value, dimension, tolerance, power, count):
    value_min = value * (1 - (tolerance / 100))
    value_max = value * (1 + (tolerance / 100))

    combinations_list = []


    for nominal in list_nominals:
        if value_min < nominal[0]:
            index_max = list_nominals.index(nominal)
            break

    for nominal in list_nominals:
        if nominal[0] > value * 0.05:
            index_min = list_nominals.index(nominal)
            break

    list_nominals_cut = list_nominals[index_min:index_max]

    if count == 2:
        for i in list_nominals_cut:
            for j in list_nominals_cut[list_nominals_cut.index(i):]:
                if i[0] * (1 + (i[1] / 100)) + j[0] * (1 + (j[1] / 100)) <= value_max and i[0] * (1 - (i[1] / 100)) + j[0] * (1 - (j[1] / 100)) >= value_min:
                    print(i, j)

    elif count == 3:
        for i in list_nominals_cut:
            for j in list_nominals_cut[list_nominals_cut.index(i):]:
                for k in list_nominals_cut[list_nominals_cut.index(j):]:
                    if i[0] * (1 + (i[1] / 100)) + j[0] * (1 + (j[1] / 100)) + k[0] * (1 + (k[1] / 100)) <= value_max and i[0] * (1 - (i[1] / 100)) + j[0] * (1 - (j[1] / 100)) + k[0] * (1 - (k[1] / 100)) >= value_min:
                        print(i, j, k)

    elif count == 4:
        for i in list_nominals_cut:
            for j in list_nominals_cut[list_nominals_cut.index(i):]:
                for k in list_nominals_cut[list_nominals_cut.index(j):]:
                    for x in list_nominals_cut[list_nominals_cut.index(k):]:
                        if i[0] * (1 + (i[1] / 100)) + j[0] * (1 + (j[1] / 100)) + k[0] * (1 + (k[1] / 100)) + x[0] * (1 + (x[1] / 100)) <= value_max and i[0] * (1 - (i[1] / 100)) + j[0] * (1 - (j[1] / 100)) + k[0] * (1 - (k[1] / 100)) + x[0] * (1 - (x[1] / 100)) >= value_min:
                            print(i, j, k, x)


    return combinations_list



output = serial_combine(value = 568, dimension = 'Ом', tolerance = 5, power = 0, count = 4)
print(output)

