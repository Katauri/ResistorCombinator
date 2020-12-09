from openpyxl import load_workbook
from kivy.metrics import dp
from kivymd.uix.label import MDLabel
import queue

caption_height = dp(20)
wb_val = load_workbook(filename = 'nominals.xlsx', data_only = True)

sheet_E24 = wb_val['E24']
sheet_E96 = wb_val['E96']
sheet_E192 = wb_val['E192']

sheets = (sheet_E24, sheet_E96, sheet_E192)

list_E24 = []
list_E96 = []
list_E192 = []

max_str_chunk = 500



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




def serial_combine(value, tolerance, power, count, tol_list, chunks, thread_state, widget_pagination, chunk_view_index):
    value_min = value * (1 - (tolerance / 100))
    value_max = value * (1 + (tolerance / 100))

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

    def update_pagination():
        widget_pagination.text = '%d/%d' % (chunk_view_index + 1, len(chunks))

    if count == 2:
        for i in list_nominals_cut:
            for j in list_nominals_cut[list_nominals_cut.index(i):]:
                if i[0] * (1 + (i[1] / 100)) + j[0] * (1 + (j[1] / 100)) <= value_max and i[0] * (1 - (i[1] / 100)) + j[0] * (1 - (j[1] / 100)) >= value_min:

                    if not thread_state:
                        return

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

                    chunk_string += '  R1: '+str(r1) + r1_dimension + str(i[1])+'%' + '  R2: ' +str(r2)+ r2_dimension +str(j[1])+'% \n'
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
                    if i[0] * (1 + (i[1] / 100)) + j[0] * (1 + (j[1] / 100)) + k[0] * (1 + (k[1] / 100)) <= value_max and i[0] * (1 - (i[1] / 100)) + j[0] * (1 - (j[1] / 100)) + k[0] * (1 - (k[1] / 100)) >= value_min:
                        if not thread_state:
                            return

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

                        r3 = round(r2, 10)

                        chunk_string += '  R1: ' + str(r1) + r1_dimension + str(i[1]) + '%' + '  R2: ' + str(
                            r2) + r2_dimension + str(j[1]) + '%'  + '  R3: ' + str(r3) + r3_dimension + str(k[1]) + '% \n'
                        str_index += 1
                        if str_index == max_str_chunk:
                            chunks.append(chunk_string[:-2])
                            str_index = 0
                            chunk_string = ''
                            update_pagination()

    if chunk_string != '':
        chunks.append(chunk_string[:-2])
        update_pagination()


def parallel_combine(value, tolerance, power, count, tol_list, chunks, thread_state, widget_pagination, chunk_view_index):
    value_min = value * (1 - (tolerance / 100))
    value_max = value * (1 + (tolerance / 100))

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

    for nominal in list_nominals:
        if value * 100 < nominal[0]:
            index_max = list_nominals.index(nominal)
            break

    for nominal in list_nominals:
        if nominal[0] > value * 0.95:
            index_min = list_nominals.index(nominal)
            break

    list_nominals_cut = list_nominals[index_min:index_max]

    chunk_string = ''
    str_index = 0

    def update_pagination():
        widget_pagination.text = '%d/%d' % (chunk_view_index + 1, len(chunks))

    if count == 2:
        for i in list_nominals_cut:
            for j in list_nominals_cut[list_nominals_cut.index(i):]:
                if (i[0] * (1 + (i[1] / 100)) * j[0] * (1 + (j[1] / 100))) / (i[0] * (1 + (i[1] / 100)) + j[0] * (1 + (j[1] / 100))) <= value_max and (i[0] * (1 - (i[1] / 100)) * j[0] * (1 - (j[1] / 100))) / (i[0] * (1 - (i[1] / 100)) + j[0] * (1 - (j[1] / 100))) >= value_min:

                    if not thread_state:
                        return

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

                    chunk_string += '  R1: '+str(r1) + r1_dimension + str(i[1])+'%' + '  R2: ' +str(r2)+ r2_dimension +str(j[1])+'% \n'
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
                    if (i[0] * (1 + (i[1] / 100)) * j[0] * (1 + (j[1] / 100))) / (i[0] * (1 + (i[1] / 100)) + j[0] * (1 + (j[1] / 100))) <= value_max and (i[0] * (1 - (i[1] / 100)) * j[0] * (1 - (j[1] / 100))) / (i[0] * (1 - (i[1] / 100)) + j[0] * (1 - (j[1] / 100))) >= value_min:
                        if not thread_state:
                            return

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

                        r3 = round(r2, 10)

                        chunk_string += '  R1: ' + str(r1) + r1_dimension + str(i[1]) + '%' + '  R2: ' + str(
                            r2) + r2_dimension + str(j[1]) + '%'  + '  R3: ' + str(r3) + r3_dimension + str(k[1]) + '% \n'
                        str_index += 1
                        if str_index == max_str_chunk:
                            chunks.append(chunk_string[:-2])
                            str_index = 0
                            chunk_string = ''
                            update_pagination()

    if chunk_string != '':
        chunks.append(chunk_string[:-2])
        update_pagination()





#output = serial_combine(value = 591, tolerance = 5, power = 0, count = 3, tol_list = ['E192'])
#print(output)

