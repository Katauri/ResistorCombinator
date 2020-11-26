from openpyxl import load_workbook

wb_val = load_workbook(filename = 'nominals.xlsx', data_only = True)

sheet_E24 = wb_val['E24']
sheet_E96 = wb_val['E96']
sheet_E192 = wb_val['E192']

sheets = (sheet_E24, sheet_E96, sheet_E192)

list_E24 = []
list_E96 = []
list_E192 = []

for sheet in sheets:
    num = 2
    while(sheet['A' + str(num)].value):
        if sheet == sheet_E24:
            list_E24.append(sheet['A' + str(num)].value)
        elif sheet == sheet_E96:
            list_E96.append(sheet['A' + str(num)].value)
        elif sheet == sheet_E192:
            list_E192.append(sheet['A' + str(num)].value)
        num += 1


def serial_combine(value, dimension, tolerance, power, count):
    value_min = value * (1 - (tolerance / 100))
    value_max = value * (1 + (tolerance / 100))

    combinations_list = []
    list_E24_pairs = []
    list_E96_pairs = []
    list_E192_pairs = []

    tiers = [list_E24, list_E96, list_E192]
    for tier in tiers:
        index = 1
        for nominal in tier:
            if nominal >= value_max:
                break
            for next_nominal in tier[index:]:
                if next_nominal >= value:
                    break

                if tier == list_E24:
                    list_E24_pairs.append([nominal, next_nominal])
                elif tier == list_E96:
                    list_E96_pairs.append([nominal, next_nominal])
                elif tier == list_E192:
                    list_E192_pairs.append([nominal, next_nominal])


            index += 1




    print(list_E24_pairs)
    return combinations_list


output = serial_combine(value = 5, dimension = 'Ом', tolerance = 5, power = 0, count = 2)
print(output)

