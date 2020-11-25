from openpyxl import load_workbook

wb_val = load_workbook(filename = 'nominals.xlsx', data_only = True)
sheet_E24 = wb_val['E24']
sheet_E96 = wb_val['E96']
sheet_E192 = wb_val['E192']

#A1_val = sheet_val['A3'].value

def serial_combine(value, dimension, tolerance, power, count):
    value_min = value * (1 - (tolerance / 100))
    value_max = value * (1 + (tolerance / 100))

    combinations_list = []


    num = 2
    while(sheet_E24['C' + str(num)].value):
        next_num = num + 1
        while(sheet_E24['C' + str(next_num)].value):

            if (value_min >= (sheet_E24['C' + str(next_num)].value + sheet_E24['C' + str(num)].value)) and (value_max <= (sheet_E24['D' + str(next_num)].value + sheet_E24['D' + str(num)].value)):
                nom_list = []
                nom_list.append(sheet_E24['A' + str(next_num)].value)
                nom_list.append(sheet_E24['A' + str(num)].value)

                combinations_list.append(nom_list)

            next_num += 1

        num += 1



    return combinations_list

output = serial_combine(value = 10, dimension = 'Ом', tolerance = 5, power = 0, count = 2)
print(output)

