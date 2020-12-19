from openpyxl import load_workbook
from kivy.metrics import dp

import time

wb_val = load_workbook(filename = 'nominals.xlsx', data_only = True)

sheet_E24 = wb_val['E24']
sheet_E96 = wb_val['E96']
sheet_E192 = wb_val['E192']

sheets = (sheet_E24, sheet_E96, sheet_E192)

list_E24 = []
list_E96 = []
list_E192 = []

max_str_chunk = 250

standart_power_nominals = [0.05, 0.063, 0.1, 0.125, 0.25, 0.5, 0.75, 1.0, 2.0, 3.0, 4, 5, 8, 10, 16, 25, 40, 50, 63, 75, 80, 100]

for sheet in sheets:
    num = 2
    while(sheet['A' + str(num)].value):
        if sheet == sheet_E24:
            list_E24.append((sheet['A' + str(num)].value, 5))
        elif sheet == sheet_E96:
            list_E96.append((sheet['A' + str(num)].value, 1))
        elif sheet == sheet_E192:
            list_E192.append((sheet['A' + str(num)].value, 0.5))
        num += 1



def serial_combine(value, tolerance, power, count, tol_list, chunks, thread_state, widget_pagination, chunk_view):
    value_min = value * (1 - (tolerance / 100))
    value_max = value * (1 + (tolerance / 100))

    q_current = power / value

    list_nominals = []

    for tolerance in tol_list:
        if tolerance == 'E24':
            for nom in list_E24:
                list_nominals.append(nom)
        elif tolerance == 'E96':
            for nom in list_E96:
                list_nominals.append(nom)
        elif tolerance == 'E192':
            for nom in list_E192:
                list_nominals.append(nom)


    list_nominals.sort(key=lambda x: x[::1])

    index_min = 0
    index_max = 1

    for nominal in list_nominals:
        if value * 0.95 < nominal[0]:
            index_max = list_nominals.index(nominal)
            break

    for nominal in list_nominals:
        if nominal[0] > value * 0.05:
            index_min = list_nominals.index(nominal)
            break

    list_nominals_cut = list_nominals[index_min:index_max]

    chunk_string = ''
    str_index = 0

    power_r1 = ''
    power_r2 = ''
    power_r3 = ''

    def update_pagination():
        widget_pagination.text = '%d/%d' % (chunk_view.index + 1, len(chunks))

    if count == 2:
        for i in list_nominals_cut:
            for j in list_nominals_cut[list_nominals_cut.index(i):]:
                if thread_state.stop:
                    return
                if i[0] * (1 + (i[1] / 100)) + j[0] * (1 + (j[1] / 100)) <= value_max and i[0] * (1 - (i[1] / 100)) + j[0] * (1 - (j[1] / 100)) >= value_min:


                    if power != 0:
                        pwr_r1 = q_current * i[0] * 1.05
                        pwr_r2 = q_current * j[0] * 1.05


                        for power in standart_power_nominals:
                            if power >= pwr_r1:
                                power_r1 = str(power) + 'W '
                                break

                        for power in standart_power_nominals:
                            if power >= pwr_r2:
                                power_r2 = str(power) + 'W '
                                break



                    r1 = i[0]
                    if r1 < 1000:
                        r1_dimension = ' Om '
                    elif r1 < 1000000:
                        r1_dimension = ' kOm '
                        r1 /= 1000
                    else:
                        r1_dimension = ' MOm '
                        r1 /= 1000000
                    r1 = round(r1, 10)

                    r2 = j[0]
                    if r2 < 1000:
                        r2_dimension = ' Om '
                    elif r2 < 1000000:
                        r2_dimension = ' kOm '
                        r2 /= 1000
                    else:
                        r2_dimension = ' MOm '
                        r2 /= 1000000

                    r2 = round(r2, 10)

                    chunk_string += 'R1: '+str(r1) + r1_dimension + power_r1 + str(i[1])+'%' + '  R2: ' +str(r2)+ r2_dimension + power_r2 +str(j[1])+'% \n'
                    str_index += 1
                    if str_index == max_str_chunk:
                        chunks.append(chunk_string[:-2])
                        str_index = 0
                        chunk_string = ''
                        update_pagination()

    elif count == 3:
        for i in list_nominals_cut:
            for j in list_nominals_cut[list_nominals_cut.index(i):]:
                for k in list_nominals_cut[list_nominals_cut.index(j):]:
                    if thread_state.stop:
                        return
                    if i[0] * (1 + (i[1] / 100)) + j[0] * (1 + (j[1] / 100)) + k[0] * (1 + (k[1] / 100)) <= value_max and i[0] * (1 - (i[1] / 100)) + j[0] * (1 - (j[1] / 100)) + k[0] * (1 - (k[1] / 100)) >= value_min:

                        if power != 0:
                            pwr_r1 = q_current * i[0] * 1.05
                            pwr_r2 = q_current * j[0] * 1.05
                            pwr_r3 = q_current * k[0] * 1.05

                            for power in standart_power_nominals:
                                if power >= pwr_r1:
                                    power_r1 = str(power) + 'W '
                                    break

                            for power in standart_power_nominals:
                                if power >= pwr_r2:
                                    power_r2 = str(power) + 'W '
                                    break

                            for power in standart_power_nominals:
                                if power >= pwr_r3:
                                    power_r3 = str(power) + 'W '
                                    break

                        r1 = i[0]
                        if r1 < 1000:
                            r1_dimension = ' Om '
                        elif r1 < 1000000:
                            r1_dimension = ' kOm '
                            r1 /= 1000
                        else:
                            r1_dimension = ' MOm '
                            r1 /= 1000000
                        r1 = round(r1, 10)

                        r2 = j[0]
                        if r2 < 1000:
                            r2_dimension = ' Om '
                        elif r2 < 1000000:
                            r2_dimension = ' kOm '
                            r2 /= 1000
                        else:
                            r2_dimension = ' MOm '
                            r2 /= 1000000

                        r2 = round(r2, 10)

                        r3 = k[0]
                        if r3 < 1000:
                            r3_dimension = ' Om '
                        elif r3 < 1000000:
                            r3_dimension = ' kOm '
                            r3 /= 1000
                        else:
                            r3_dimension = ' MOm '
                            r3 /= 1000000

                        r3 = round(r3, 10)

                        chunk_string += 'R1: ' + str(r1) + r1_dimension + power_r1 + str(i[1]) + '%' + '  R2: ' + str(
                            r2) + r2_dimension + power_r2 + str(j[1]) + '%'  + '  R3: ' + str(r3) + r3_dimension + power_r3 + str(k[1]) + '% \n'
                        str_index += 1
                        if str_index == max_str_chunk:
                            chunks.append(chunk_string[:-2])
                            str_index = 0
                            chunk_string = ''
                            update_pagination()
                            if thread_state.stop:
                                return
                            time.sleep(0.1)


    if chunk_string != '':
        chunks.append(chunk_string[:-2])
        update_pagination()
    else:
        chunks.append('Combination not found!')


def parallel_combine(value, tolerance, power, count, tol_list, chunks, thread_state, widget_pagination, chunk_view):
    value_min = value * (1 - (tolerance / 100))
    value_max = value * (1 + (tolerance / 100))

    q_voltage = power * value

    list_nominals = []

    for tolerance in tol_list:
        if tolerance == 'E24':
            for nom in list_E24:
                list_nominals.append(nom)
        elif tolerance == 'E96':
            for nom in list_E96:
                list_nominals.append(nom)
        elif tolerance == 'E192':
            for nom in list_E192:
                list_nominals.append(nom)


    list_nominals.sort(key=lambda x: x[::1])

    index_min = 0
    index_max = 1

    for nominal in list_nominals:
        if nominal[0] > value:
            index_min = list_nominals.index(nominal)
            break

    r_multiplier = 25

    cycle = True
    while cycle:
        for nominal in list_nominals[index_min:]:
            if value * r_multiplier < nominal[0]:
                index_max = list_nominals.index(nominal)
                cycle = False
                break
        r_multiplier /= 2


    list_nominals_cut = list_nominals[index_min:index_max]

    chunk_string = ''
    str_index = 0

    def update_pagination():
        widget_pagination.text = '%d/%d' % (chunk_view.index + 1, len(chunks))

    power_r1 = ''
    power_r2 = ''
    power_r3 = ''

    if count == 2:
        for i in list_nominals_cut:
            for j in list_nominals_cut[list_nominals_cut.index(i):]:
                if thread_state.stop:
                    return
                if (i[0] * (1 + (i[1] / 100)) * j[0] * (1 + (j[1] / 100))) / (i[0] * (1 + (i[1] / 100)) + j[0] * (1 + (j[1] / 100))) <= value_max and (i[0] * (1 - (i[1] / 100)) * j[0] * (1 - (j[1] / 100))) / (i[0] * (1 - (i[1] / 100)) + j[0] * (1 - (j[1] / 100))) >= value_min:

                    if power != 0:
                        pwr_r1 = (q_voltage / i[0]) * 1.05
                        pwr_r2 = (q_voltage / j[0]) * 1.05

                        for power in standart_power_nominals:
                            if power >= pwr_r1:
                                power_r1 = str(power) + 'W '
                                break

                        for power in standart_power_nominals:
                            if power >= pwr_r2:
                                power_r2 = str(power) + 'W '
                                break

                    r1 = i[0]
                    if r1 < 1000:
                        r1_dimension = ' Om '
                    elif r1 < 1000000:
                        r1_dimension = ' kOm '
                        r1 /= 1000
                    else:
                        r1_dimension = ' MOm '
                        r1 /= 1000000
                    r1 = round(r1, 10)

                    r2 = j[0]
                    if r2 < 1000:
                        r2_dimension = ' Om '
                    elif r2 < 1000000:
                        r2_dimension = ' kOm '
                        r2 /= 1000
                    else:
                        r2_dimension = ' MOm '
                        r2 /= 1000000

                    r2 = round(r2, 10)

                    chunk_string += 'R1: '+str(r1) + r1_dimension + power_r1 + str(i[1])+'%' + '  R2: ' +str(r2)+ r2_dimension + power_r2 + str(j[1])+'% \n'
                    str_index += 1
                    if str_index == max_str_chunk:
                        chunks.append(chunk_string[:-2])
                        str_index = 0
                        chunk_string = ''
                        update_pagination()


    elif count == 3:
        for i in list_nominals_cut:
            for j in list_nominals_cut[list_nominals_cut.index(i):]:
                for k in list_nominals_cut[list_nominals_cut.index(j):]:
                    if thread_state.stop:
                        return
                    r2_r3_max = (j[0] * (1 + (j[1] / 100)) * k[0] * (1 + (k[1] / 100)))
                    r2_r3_min = (j[0] * (1 - (j[1] / 100)) * k[0] * (1 - (k[1] / 100)))

                    if (r2_r3_max / (j[0] * (1 + (j[1] / 100)) + k[0] * (1 + (k[1] / 100)) + r2_r3_max / (i[0] * (1 + (i[1] / 100))))) <= value_max and (r2_r3_min / (j[0] * (1 - (j[1] / 100)) + k[0] * (1 - (k[1] / 100)) + r2_r3_min / (i[0] * (1 - (i[1] / 100))))) >= value_min:

                        if power != 0:
                            pwr_r1 = (q_voltage / i[0]) * 1.05
                            pwr_r2 = (q_voltage / j[0]) * 1.05
                            pwr_r3 = (q_voltage / k[0]) * 1.05

                            for power in standart_power_nominals:
                                if power >= pwr_r1:
                                    power_r1 = str(power) + 'W '
                                    break

                            for power in standart_power_nominals:
                                if power >= pwr_r2:
                                    power_r2 = str(power) + 'W '
                                    break

                            for power in standart_power_nominals:
                                if power >= pwr_r3:
                                    power_r3 = str(power) + 'W '
                                    break

                        r1 = i[0]
                        if r1 < 1000:
                            r1_dimension = ' Om '
                        elif r1 < 1000000:
                            r1_dimension = ' kOm '
                            r1 /= 1000
                        else:
                            r1_dimension = ' MOm '
                            r1 /= 1000000
                        r1 = round(r1, 10)

                        r2 = j[0]
                        if r2 < 1000:
                            r2_dimension = ' Om '
                        elif r2 < 1000000:
                            r2_dimension = ' kOm '
                            r2 /= 1000
                        else:
                            r2_dimension = ' MOm '
                            r2 /= 1000000

                        r2 = round(r2, 10)

                        r3 = k[0]
                        if r3 < 1000:
                            r3_dimension = ' Om '
                        elif r3 < 1000000:
                            r3_dimension = ' kOm '
                            r3 /= 1000
                        else:
                            r3_dimension = ' MOm '
                            r3 /= 1000000

                        r3 = round(r3, 10)

                        chunk_string += 'R1: ' + str(r1) + r1_dimension + power_r1 + str(i[1]) + '%' + '  R2: ' + str(
                            r2) + r2_dimension + power_r2 + str(j[1]) + '%'  + '  R3: ' + str(r3) + r3_dimension + power_r3 + str(k[1]) + '% \n'
                        str_index += 1
                        if str_index == max_str_chunk:
                            chunks.append(chunk_string[:-2])
                            str_index = 0
                            chunk_string = ''
                            update_pagination()
                            if thread_state.stop:
                                return
                            time.sleep(0.1)



    if chunk_string != '':
        chunks.append(chunk_string[:-2])
        update_pagination()
    else:
        chunks.append('Combination not found!')






#output = serial_combine(value = 591, tolerance = 5, power = 0, count = 3, tol_list = ['E192'])
#print(output)

