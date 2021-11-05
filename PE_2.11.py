#!/usr/bin/env python
# coding: utf-8

# In[149]:


import PySimpleGUI as sg
import os
import shutil

# In[150]:


sg.theme("LightGrey1")


# ## Functions for power

# In[152]:


# функция создания массива строк элементов Q, R, D и М из файле
def list_elems(name: str):
    a: list[str]
    a = []
    f_cir = open(name, 'rt')
    for line in f_cir:
        if line[0] == 'Q':
            a.append(line)
        elif line[0] == 'R':
            a.append(line)
        elif line[0] == 'D':
            a.append(line)
        elif line[0] == 'M':
            a.append(line)
    f_cir.close()
    return a


# In[154]:


# считывание
def el_read(element: list[str]):
    if (element[0][0] == 'q') or (element[0][0] == 'Q'):
        if element[1] == '0':
            return '.meas ' + element[0] + '_power ABS AVG Ic(' + element[0] + ')*(-V(' + element[3] + ')' + '\n'
        elif element[3] == '0':
            return '.meas ' + element[0] + '_power ABS AVG Ic(' + element[0] + ')*V(' + element[1] + ')' + '\n'
        return '.meas ' + element[0] + '_power ABS AVG Ic(' + element[0] + ')*V(' + element[1] + ',' + element[3] + \
               ')' + '\n'
    elif (element[0][0] == 'r') or (element[0][0] == 'R'):
        if element[1] == '0':
            return '.meas ' + element[0] + '_power ABS AVG I(' + element[0] + ')*(-V(' + element[2] + '))' + '\n'
        elif element[2] == '0':
            return '.meas ' + element[0] + '_power ABS AVG I(' + element[0] + ')*V(' + element[1] + ')' + '\n'
        return '.meas ' + element[0] + '_power ABS AVG I(' + element[0] + ')*V(' + element[1] + ',' + element[2] + \
               ')' + '\n'
    elif (element[0] == 'd') or (element[0][0] == 'D'):
        if element[1] == '0':
            return '.meas ' + element[0] + '_power ABS AVG I(' + element[0] + ')*(-V(' + element[2] + '))' + '\n'
        elif element[2] == '0':
            return '.meas ' + element[0] + '_power ABS AVG I(' + element[0] + ')*V(' + element[1] + ')' + '\n'
        return '.meas ' + element[0] + '_power ABS AVG I(' + element[0] + ')*V(' + element[1] + ',' + element[2] + \
               ')' + '\n'
    elif (element[0] == 'm') or (element[0][0] == 'M'):
        if element[1] == '0':
            return '.meas ' + element[0] + '_power ABS AVG Ic(' + element[0] + ')*(-V(' + element[3] + ')' + '\n'
        elif element[3] == '0':
            return '.meas ' + element[0] + '_power ABS AVG Ic(' + element[0] + ')*V(' + element[1] + ')' + '\n'
        return '.meas ' + element[0] + '_power ABS AVG Id(' + element[0] + ')*V(' + element[1] + ',' + element[3] + \
               ')' + '\n'


# In[155]:


# функция перевода файла в текстовый массив, если присутствует знаки кириллицы
def file2strarr1(name):
    file = None
    with open(name, encoding='utf-16-le') as fh:
        file = fh.read()
    mylix = file.splitlines(True)
    return mylix


# In[156]:


# функция перевода файла в текстовый массив
def file2strarr(name):
    sor = open(name, 'r')
    mylix = sor.read().splitlines(True)
    sor.close()
    return mylix


# ## Variables

# In[157]:


# ввод глобальных элементов для списков элементов, адреса и сохранения выбранных элементов
k = []
adrs = []
slist = []

# In[158]:


# здесь находятся тексотовые переменные.
text_exit_button = 'Выйти'
text_browse_file = "Выберите файл-netlist вашей схемы в формате .txt, .net или .cir:"
text_open, key_open = "Выбрать файл", "-IN-"
text_show_the_list = "Вывести список элементов"
text_choose_elements, key_list = "Выберите элементы для расчета мощностей \n(среди биполярных и МОП-транзисторов, \n\
резисторов и диодов): ", "-listbox-"
text_help = 'Для выбора элемента щёлкните по нему левой кнопкой мыши,для выбора нескольких элементов зажмите клавишу \
Ctrl и щёлкните по нужным элементам левой кнопкой мыши. \nПосле выбора элементов нажмите "Сохранить", чтобы сохранить \
файл с командами для расчёта мощностей выбранных компонентов.'
text_save = "Сохранить"
text_copy = "Копировать"
text_close = "Закрыть"
text_for_error_file_open = "После запуска файла со схемой в LTSpice обработайте файл с выходными данными (Spice Error \
Log), чтобы сохранить мощности компонентов в файл. \n(Для программы АСОНИКА-ТМ мощности выводятся в милливаттах!)"
errt = "Ошибка"
chft = 'ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ Выберите файлᅠ ᅠ ᅠ ᅠ ᅠ ᅠ '
ches = 'ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ Выберите элементы!ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ '
errt2 = 'Пустой файл'
text1_open_error = 'Открыть файл ошибки в другой папке'
key_open_error = '-errorfile-'
text_open_error_default = 'Обработать выходные данные'
open_power_file = 'Открыть полученный файл'
error_text_error_log = 'ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ Файл error_log отсутствует!ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ '
final_popup_text = 'Программа посчитала выбранные мощности. Нажмите \"Открыть полученный файл\" для просмотра.'
text_hint = 'Чтобы получить файл Netlist откройте схему в LTSpice. В верхнем меню View выберите \"SPICE Netlist\". \n\
В папке со схемой появится временный файл с форматом данных .net\n(Вы можете сохранить файл в формате .cir, щелкнув ПКМ\
 по диалоговому окну Netlist в LTSpice,\nчтобы сделать файл постоянным, и иметь возможность работать с ним вне \
 зависимости от LTSpice).'
message_treatment = 'Чтобы открыть файл схемы в LTSpice нажмите на кнопку "Открыть LTSpice"\n\
Через .op (SPICE Directive) вставьте скопированную команду (.include...) на схему и запустите её (Simulate → Run)'
rus_lower = set('аоуыэяеёюибвгдйжзклмнпрстфхцчшщ')
rus_upper = set('АОУЫЭЯЕЁЮИБВГДЙЖЗКЛМНПРСТФХЦЧШЩ')
text_for_somebody = 'Вы можете выйти из программы, нажав кнопку "Выйти". \nВы также можете выполнить расчет заново \
или выполнить его для новой схемы, для этого начните выполнять действия с первого шага.'


# ## Functions for reader_saver

# In[159]:


def mes_generator(svadrs: str, inmes: str):
    mes = 'Откройте файл со схемой, Netlist которой обрабатывали.\nДиректория Netlist — ' + svadrs + '\nИ соответствует\
        директории схемы.\n' + 'Для дальнейших расчетов вам необходимо добавить на схему следующую команду: ' + '\n' + \
          inmes + '\nЧтобы скопировать команду в буфер обмена, нажмите "Копировать"'
    return mes


# In[160]:


def include_address(ss: str):
    down = ''
    for i in ss:
        if i != '.':
            down += i
        elif i == '.':
            break
    down += '-1.inc'
    return down


# In[161]:


def error_file_adrs(a: str):
    down = a.replace('.asc', '')
    down += '.log'
    return down


# In[162]:


def listreader(a: str):
    if '.txt' in a:
        mylix = file2strarr(a)
    else:
        mylix = file2strarr1(a)
    schema_adrs = mylix[0].replace('* ', '')
    names = []
    list_with_info = []
    for line in mylix:
        gar = line.split()
        if (gar[0][0] == 'Q') or (gar[0][0] == 'R') or (gar[0][0] == 'M') or (gar[0][0] == 'D'):
            names.append(gar[0])
            list_with_info.append(line)
    return mylix, names, schema_adrs, list_with_info


# In[163]:


def saving(a1: list[str], a2: str, z):
    with open(a2, 'w') as f:
        for iz in a1:
            se = iz.split()
            prov = se[0]
            for stroka in z:
                if stroka == prov:
                    f.write(el_read(se))


# In[164]:


def read_with_decoder(name, first_name, n):
    file = None
    lix = []
    with open(name, encoding='utf-16-le') as fh:
        file = fh.read()
    lix = file.splitlines()
    spisok = []
    for l in range(len(lix)):
        if lix[l].find(first_name) == 0:
            for i in range(l, l + n):
                spisok.append(lix[i])
            break
    return spisok


# In[165]:


def read_without_decoder(name, first_name, n):
    sor = open(name, 'r')
    mylix = sor.read().splitlines(True)
    sor.close()
    spisok = []
    for l in range(len(mylix)):
        if mylix[l].find(first_name) == 0:
            for i in range(l, l + n):
                print(mylix[i])
                spisok.append(mylix[i])
                break
    return spisok


# In[166]:

# проверка на наличие символов кириллицы в названии или адресе
def checkk(a, first_name, n):
    f = True
    rus_lower = 'аоуыэяеёюибвгдйжзклмнпрстфхцчшщ'
    rus_upper = 'АОУЫЭЯЕЁЮИБВГДЙЖЗКЛМНПРСТФХЦЧШЩ'
    for letter in a:
        if (rus_lower.find(letter) != -1) or (rus_upper.find(letter) != -1):
            f = False
            break
    if f == True:
        return read_without_decoder(a, first_name, n)
    else:
        return read_with_decoder(a, first_name, n)


# In[167]:

# сюда приходит адрес и выбранные элементы, на выходе формируется файл
def power_file_saving(address, first_name, number_of_elements, final_file):
    n = number_of_elements
    spisok = checkk(address, first_name, n)
    output_file = open(final_file, 'w')
    for s in spisok:
        list1 = s.split('=')
        value = ''
        tt = list1[0].split('_')[0]
        for letter in list1[1]:
            if letter != ' ':
                value += letter
            else:
                break
        output_file.write(tt + ' ' + str(float(value) * 1000) + '\n')
    output_file.close()


# ## Wireframe

# In[168]:


# здесь каркас интерфейса, кнопки окна и пр. из-за того,
# что Д.А. захотел написать целую книгу в одном окошке их может плохо видно :)
layout = [
    [sg.Text(text_hint)],
    [sg.Text(text_browse_file), sg.Input(), sg.FileBrowse(button_text=text_open, button_color='green',
                                                          file_types=(("Text Files", "*.txt"),
                                                                      ("Text Files", "*.net"),
                                                                      ("Text Files", "*.cir")
                                                                      ),
                                                          key=key_open)],
    [sg.Button(text_show_the_list, button_color='green')],
    [sg.Text(text_choose_elements), sg.Listbox(k, s=(50, 10), select_mode='extended', key=key_list)],
    [sg.Text(text_help)],
    [sg.Button(text_save, button_color='green')],
    [sg.Text(text_for_error_file_open)],
    [sg.Button(text_open_error_default, button_color='green')],
    [sg.Text(text_for_somebody)],
    [sg.Button(text_exit_button, button_color='red')]
]

# ## Using

# In[ ]:


# здесь работа программы самой sg. — функции библиотеки PySimpleGUI
# PopUp — всплывающие окошки, многочисленные else и elif нужны для вывода ошибок пользователя
# все переменные вроде key..что-нибудь или tetx..что-нибудь или errt или все остальное — тексты заданные в variables,
# для того, чтобы было удобней менять текст
# файлы формата .ico — мультииконки, они лежат в архиве с программой
window = sg.Window('Power Extractor', layout, icon='icon.ico')

while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, text_exit_button):
        window.close()
        break

    elif event == text_show_the_list:
        # values[<что-нибудь>] — зачения, полученные после какого-либо ивента,
        # в данном случае, функция открывает файл, но если открывать нечего, она выводит PopUp с ошибкой
        if values[key_open] == '':
            sg.Popup(chft, title=errt, button_type=0, icon='warning.ico')

        else:
            adrs = (values[key_open])
            buf, k, schema_file, info_list = listreader(adrs)
            schema_address, schema_name = os.path.split(schema_file)
            window.FindElement(key=key_list).Update(k)
    # условия типа event равно <что-нибудь>: <что-нибудь> это, в данном случае,
    # нажатие на кнопку с текстом в переменной "text_save"
    elif event == text_save:

        if values[key_open] == '':
            sg.Popup(chft, title=errt, button_type=0, icon='warning.ico')
        elif values[key_list] == []:
            sg.Popup(ches, title=errt2, button_type=0, icon='warning.ico')

        else:
            svadrs, name = os.path.split(adrs)
            include_file = include_address(name)
            sv = svadrs + '/' + include_file
            list_of_chosen_elements = values[key_list]
            first_name, number_of_elements = (list_of_chosen_elements[0].lower() + '_power',
                                              len(list_of_chosen_elements))

            for val in values[key_list]:
                slist.append(val)

            if slist == []:
                sg.Popup(ches, title=errt2, button_type=0, icon='warning.ico')

            else:
                saving(info_list, sv, slist)
                inmes = '.include ' + include_file
                zh = sg.Popup(mes_generator(svadrs, inmes), title='Внимание', custom_text=(text_copy, text_close),
                              background_color='white', icon='icon.ico')

                if zh == text_copy:
                    sg.clipboard_set(inmes)
                spice_treatment = sg.Popup(message_treatment, title='Внимание', button_type=2,
                                           custom_text='Открыть LTSpice', background_color='white', icon='icon.ico')

                if spice_treatment == 'Открыть LTSpice':
                    os.startfile(schema_file)

    elif event == text_open_error_default:

        if values[key_open] == '':
            sg.Popup(chft, title=errt, button_type=0, icon='warning.ico')

        else:
            original_error_file = error_file_adrs(schema_file)
            original_error_address, original_error_name = os.path.split(original_error_file)
            directory_test_list = os.listdir(schema_address)

            if original_error_name in directory_test_list:

                if slist == []:
                    sg.Popup(ches, title=errt2, button_type=0, icon='warning.ico')

                else:
                    final_file = svadrs + '\\power of ' + schema_name.replace('.asc', '') + '.txt'
                    # tuple_for_eror(original_error_file, first_name, number_of_elements)
                    power_file_saving(original_error_file, first_name, number_of_elements, final_file)
                    power_was_calculated = sg.Popup(final_popup_text, title='Готово', button_type=2,
                                                    custom_text=open_power_file, icon='icon.ico')

                    if power_was_calculated == open_power_file:
                        os.startfile(final_file)
            else:
                sg.Popup(error_text_error_log, title=errt, button_type=0, icon='warning.ico')
