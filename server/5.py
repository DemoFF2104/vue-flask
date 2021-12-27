# 5 Лаба Криптография ч2 Эль-Гамаль
import random
import time
from tkinter import *
from tkinter import Tk, Text, messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.ttk import Progressbar, Style
from tkinter import scrolledtext

view_size = 650
bufer_out = ""
bufer_in = ""

q = 0
p = 0
g = 0


def generate_g(p):
    global q
    x = random.randint(2, p - 2)
    while True:
        if bin_pow(x, q, p) != 1:
            g = x
            break
        else:
            x = random.randint(2, p - 2)

    if g == 0:
        messagebox.showinfo('Ошибка генерации',
                            'Не удалось сгенерировать число G!')
        return 0
    else:
        return g


# Функция разбиения сообщения на блоки
def to_blocks(message):
    # Вычисляем количество блоков
    blocks_number = len(message) // 12
    if len(message) % 12 != 0:
        blocks_number += 1

    blocks = [""] * blocks_number

    for i in range(blocks_number):
        for j in range(12):
            # Проверка навыход за пределы сообщения
            if (12 * i + j) > (len(message) - 1):
                break
            else:
                # Записываем кодировку текущего символа

                # Запрещаем символ с кодом 9999 (используем его для замены 0)
                if ord(message[12 * i + j]) == 9999:
                    messagebox.showinfo('Ошибка преобразования',
                                        'Символ с кодом 9999 недопустим')
                    return 0
                # Если попадается символ с кодом 0, то код 0 заменяем кодом 9999 (так как 0 дозаполняем пустое пространство)
                elif ord(message[12 * i + j]) == 0:
                    tmp = "9999"
                # Получаем код символа и переводим его в строчный формат
                else:
                    tmp = str(ord(message[12 * i + j]))

                # Ставим в начало нули, если код не 4-значный
                for k in range(4 - len(tmp)):
                    tmp = "0" + tmp

                # Формируем блок
                blocks[i] += tmp

        # Преобразуем блок в 48-значное число
        blocks[i] = int(blocks[i])

    return blocks


# Функция получения сообщения из блоков
def from_blocks(blocks):
    text_size = 0
    for i in range(len(blocks)):
        blocks[i] = str(blocks[i])
        text_size += len(blocks[i]) // 4
        remainder = len(blocks[i]) % 4

        if remainder != 0:
            text_size += 1
            for j in range(4 - remainder):
                blocks[i] = "0" + blocks[i]

    text = ""
    for i in range(len(blocks)):
        for j in range(0, len(blocks[i]), 4):
            tmp = ""
            for k in range(j, j + 4):
                tmp += blocks[i][k]
            tmp = int(tmp)
            if tmp == 9999:
                text += chr(0)
            else:
                text += chr(tmp)

    return list(text)


# Алгоритм бинарного возведения в степень
def bin_pow(a, x, p):
    if x == 1:
        return a % p
    else:
        bin_x = bin(x)[2:]
        result = a
        for i in range(1, len(bin_x)):
            result = ((result * result) * pow(a, int(bin_x[i]))) % p
        return result


# Проверка простоты тестом Миллера-Рабина
def prime_check(n):
    print("Проверка на простоту")
    print("Число - ", n)
    x = n - 1
    s = 0

    # Раскладываем число n-1 на (2^s) * d
    while True:
        if x % 2 != 0:
            d = x
            break
        else:
            x = x // 2
            s += 1

    print("d - ", d, "s - ", s)
    print("Проверка - ", (pow(2, s) * d) + 1)

    prime_found = False
    a = 10
    # Проверка первого условия
    if bin_pow(a, d, n) == 1:
        prime_found = True
    else:
        # Проверка второго условия
        for i in range(s):
            if bin_pow(a, pow(2, i) * d, n) == n - 1:
                prime_found = True

    if prime_found:
        print("Проверка пройдена!")
        return True
    else:
        print("Проверка не пройдена!")
        return False


# Функция генерации n-значного простого числа (degree = n)
def prime_generate(degree):
    while True:
        # Генерируем число d
        d = random.randint(2, 10000000)
        # Если число чётное, прибавляем единицу, делая нечётным
        if d % 2 == 0:
            d += 1

        s = 0
        a = 10
        prime = d
        while True:
            if prime // pow(a, degree) > 0:
                if prime % 2 == 0:
                    prime += 1
                break
            else:
                prime *= 2
                s += 1
        print("Вариант числа", prime)

        prime_found = False

        # Проверка первого условия
        if bin_pow(a, d, prime) == 1:
            print("Проверка пройдена")
            prime_found = True
            break
        else:
            # Проверка второго условия
            for i in range(s):
                if bin_pow(a, pow(2, i) * d, prime) == prime - 1:
                    print("Проверка пройдена")
                    prime_found = True

        if prime_found:
            break

    return prime


# Функция генерации чисел p и g
def options_generate():
    global q
    global p
    global g
    global Cb
    global Db

    # Очистка полей вывода P и G
    text_P.delete(1.0, END)
    text_G.delete(1.0, END)
    text_Cb.delete(1.0, END)
    text_Db.delete(1.0, END)

    s.configure("LabeledProgressbar",
                text="Генерация чисел P,G,Cb и Db",
                foreground='black',
                background='mediumseagreen')
    Progres_bar.configure(value=0)
    Progres_bar.update()

    # Генерируем и выводим число P
    q = prime_generate(50)
    p = 2 * q + 1
    while True:
        if prime_check(p) == True:
            break
        else:
            q = prime_generate(50)
            p = 2 * q + 1

    text_P.insert(INSERT, p)
    print("\nЧисло P найдено")

    g = generate_g(p)
    text_G.insert(INSERT, g)

    # Вычисляем ключи
    Cb = random.randint(1, p - 1)
    Db = bin_pow(g, Cb, p)

    # Выводим ключи
    text_Cb.insert(INSERT, Cb)
    text_Db.insert(INSERT, Db)

    s.configure("LabeledProgressbar",
                text="Числа P,G,Cb и Db сгенерированы",
                foreground='black',
                background='mediumseagreen')
    Progres_bar.configure(value=0)
    Progres_bar.update()

    return 0


# Функция чтения файла
def open_file():
    global bufer_in
    print("Загрузка из файла")

    s.configure("LabeledProgressbar",
                text="Чтение файла",
                foreground='black',
                background='mediumseagreen')
    Progres_bar.configure(value=0)
    Progres_bar.update()

    filename = askopenfilename()

    if filename == "":
        return 0

    print(filename)

    # Пытаемся открыть файл
    try:
        file = open(filename, "rb")
        inputText = file.read()
        inputText2 = ''
        for i in range(len(inputText)):
            int_value = int(inputText[i])
            letter = chr(int_value)
            inputText2 += letter
        file.close()
    except Exception as error:
        messagebox.showinfo('Ошибка при открытии файла',
                            'Не удалось открыть файл')
        return 0

    s.configure("LabeledProgressbar",
                text="Файл прочитан",
                foreground='black',
                background='mediumseagreen')
    Progres_bar.configure(value=0)
    Progres_bar.update()

    txt_Input.delete(1.0, END)
    # Выводими содержимое файла
    bufer_in = inputText2

    if len(inputText2) > view_size:
        txt_Input.insert(INSERT, inputText2[:view_size])
    else:
        txt_Input.insert(INSERT, inputText2)


# Функция записи в файл
def save_file():
    global bufer_out
    print("Выгрузка в файл")
    txt_original = bufer_out
    filename = asksaveasfilename()
    A = [0] * len(txt_original)
    for i in range(len(txt_original)):
        A[i] = ord(txt_original[i])
    A = bytearray(A)

    try:
        file = open(filename, "w+b")
        file.write(A)
        messagebox.showinfo('Выгрузка в файл', 'Данные успешно записаны!')
    except Exception as error:
        messagebox.showinfo(
            'Ошибка при выгрузке в файл',
            'Не удалось открыть файл, либо записать данные в файл')
        return 0


# Функция шифрования
def use_cipher():
    global bufer_in
    global bufer_out
    global p
    global g
    global Db
    global Cb

    # Засекаем время выполнения
    start_time = time.time()

    txt_Output.delete(1.0, END)

    # Првоеряем, откуда сообщение (файл/поле ввода)
    if chk_message.get():
        # Читаем из поля ввода
        txt_original = list(txt_Input.get(
            1.0, END))  # Читаем весь текст из поля ввода
        del txt_original[-1]
    else:
        # Из файла
        txt_original = list(bufer_in)

    if len(txt_original) == 0:
        messagebox.showinfo('Ошибка при вводе сообщения',
                            'Сообщение не введено!')
        return 0

    # Генерируем числа p и g
    options_generate()

    s.configure("LabeledProgressbar", text="Разбиение текста на блоки")
    window.update()

    # Разбиваем сообщение на блоки
    blocks = to_blocks(txt_original)

    # Число символов на 1 процент
    one_step = len(blocks) // 60
    if one_step == 0:
        one_step = 1
    count_progress = 0

    Progres_bar.configure(value=30)
    Progres_bar.update()

    # Пытаемся открыть файл
    try:
        file = open("lab_5.txt", "w")
    except Exception as error:
        messagebox.showinfo('Ошибка записи в файл', 'Не удалось открыть файл!')
        return 0

    # Записываем в файл используемые параметры
    try:
        file.write("p = " + str(p) + "\n\n" + "g = " + str(g) + "\n\n" +
                   "Закрытый ключ(Cb) = " + str(Cb) + "\n\n" +
                   "Открытый ключ(Db) = " + str(Db) + "\n\n" +
                   "Получатель передаёт отправителю Db")
    except Exception as error:
        messagebox.showinfo('Ошибка записи в файл',
                            'Не удалось записать данные в файл')
        return 0

    s.configure("LabeledProgressbar",
                text="Имитация процесса шифрования-передачи-расшифрования")
    window.update()
    pp = p

    for i in range(len(blocks)):
        # Отправитель выбирает случайное число к
        k = random.randint(1, p - 2)

        # Отправитель шифрует
        r = bin_pow(g, k, p)
        e = bin_pow((blocks[i] * bin_pow(Db, k, p)), 1, p)

        # Получатель расшифровывает
        res = bin_pow(e * (bin_pow(r, (p - 1 - Cb), p)), 1, p)
        blocks[i] = res

        result = "\n\nБлок " + str(i + 1) + ":\n\nm = " + str(
            blocks[i]) + "\n\nОтправитель шифрует сообщение\n\nr = " + str(
                r) + "\n\ne = " + str(
                    e
                ) + "\n\nПолучатель расшифровывает сообщение\n\n m'= " + str(
                    res)

        # Записываем действия в файл
        try:
            file.write(result)
        except Exception as error:
            messagebox.showinfo('Ошибка записи в файл',
                                'Не удалось записать данные в файл')
            return 0

        # Отмечаем прогресс
        if count_progress == one_step or count_progress > one_step:
            Progres_bar.step()
            Progres_bar.update()
            count_progress -= one_step
        count_progress += 1

    # Закрываем файл
    file.close()

    s.configure("LabeledProgressbar", text="Преобразование блоков в сообщение")
    window.update()

    # Собираем сообщение из блоков
    result = from_blocks(blocks)

    Progres_bar.configure(value=100)
    Progres_bar.update()

    bufer_out = result
    if len(bufer_out) > view_size:
        txt_Output.insert(INSERT, ''.join(result[:view_size]))
    else:
        txt_Output.insert(INSERT, ''.join(result))

    result_string = "Готово. Время - " + str(time.time() -
                                             start_time)[:5] + "сек"
    s.configure("LabeledProgressbar", text=result_string)
    window.update()
    return 0


def clear_input():
    txt_Input.delete(1.0, END)


def clear_output():
    txt_Output.delete(1.0, END)


def on_enter(e):
    e.widget['background'] = 'dim gray'


def on_leave(e):
    e.widget['background'] = BUTTON_COLOR


# Функция разрешающая события copy/paste/cut/selectAll на русской раскладке
def allow_copy_paste_cut(event):
    ctrl = (event.state & 0x4) != 0

    if event.keycode == 88 and ctrl and event.keysym.lower() != "x":
        event.widget.event_generate("<<Cut>>")

    if event.keycode == 86 and ctrl and event.keysym.lower() != "v":
        event.widget.event_generate("<<Paste>>")

    if event.keycode == 67 and ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")

    if event.keycode == 65 and ctrl and event.keysym.lower() != "a":
        event.widget.event_generate("<<SelectAll>>")


# Визуальное оформление главной страницы
WINDOW_COLOR = "Antique white3"
BUTTON_COLOR = "ivory4"
FONT_FOR_LABEL = "PT Sans Bold"

window = Tk()
window.title("Криптосистема Эль-Гамаля")
window["bg"] = WINDOW_COLOR  # Фоновый цвет главного окна
window.geometry('700x500')
window.resizable(False, False)
window.bind_all("<Key>", allow_copy_paste_cut, "+")

# Ввод/вывод сообщения

lbl_Input_Text = Label(window,
                       text="Сообщение отправителя:",
                       font=(FONT_FOR_LABEL, 14),
                       background=WINDOW_COLOR)  # Бирка для ввода сообщения
lbl_Input_Text.place(relx=0.01, rely=0.01, relwidth=0.32, relheight=0.07)

txt_Input = scrolledtext.ScrolledText(window, width=70,
                                      height=10)  # Область ввода сообщения
txt_Input.place(relx=0.01, rely=0.08, relwidth=0.98, relheight=0.28)

lbl_Output_Text = Label(window,
                        text="Сообщение получателя:",
                        font=(FONT_FOR_LABEL, 14),
                        background=WINDOW_COLOR)  # Бирка для вывода результата
lbl_Output_Text.place(relx=0.01, rely=0.56, relwidth=0.3, relheight=0.07)

txt_Output = scrolledtext.ScrolledText(window, width=70,
                                       height=10)  # Область вывода результата
txt_Output.place(relx=0.01, rely=0.63, relwidth=0.98, relheight=0.28)

# Параметры

lbl_Input_P = Label(window,
                    text="P:",
                    font=(FONT_FOR_LABEL, 14),
                    background=WINDOW_COLOR)  # Бирка для ввода числа P
lbl_Input_P.place(relx=0.01, rely=0.45, relwidth=0.03, relheight=0.04)

text_P = Text(window)  # Ввод числа P
text_P.place(relx=0.04, rely=0.452, relwidth=0.45, relheight=0.04)

lbl_Input_G = Label(window,
                    text="G:",
                    font=(FONT_FOR_LABEL, 14),
                    background=WINDOW_COLOR)  # Бирка для ввода числа G
lbl_Input_G.place(relx=0.01, rely=0.51, relwidth=0.03, relheight=0.04)

text_G = Text(window)  # Ввод числа G
text_G.place(relx=0.04, rely=0.512, relwidth=0.45, relheight=0.04)

lbl_Input_Cb = Label(window,
                     text="Cb:",
                     font=(FONT_FOR_LABEL, 14),
                     background=WINDOW_COLOR)  # Бирка для ввода числа Cb
lbl_Input_Cb.place(relx=0.495, rely=0.45, relwidth=0.04, relheight=0.04)

text_Cb = Text(window)  # Ввод числа Cb
text_Cb.place(relx=0.54, rely=0.452, relwidth=0.45, relheight=0.04)

lbl_Input_Db = Label(window,
                     text="Db:",
                     font=(FONT_FOR_LABEL, 14),
                     background=WINDOW_COLOR)  # Бирка для ввода числа Db
lbl_Input_Db.place(relx=0.495, rely=0.51, relwidth=0.04, relheight=0.04)

text_Db = Text(window)  # Ввод числа Db
text_Db.place(relx=0.54, rely=0.512, relwidth=0.45, relheight=0.04)

# Кнопки

chk_message = BooleanVar()
chk_message.set(False)  # По умолчанию - загрузка из файла
chk_msg = Checkbutton(window,
                      text='Ручной ввод сообщения',
                      var=chk_message,
                      font=(FONT_FOR_LABEL, 10),
                      background=WINDOW_COLOR)
chk_msg.place(relx=0.008, rely=0.38)

btn_Code = Button(window,
                  text="Запустить",
                  command=use_cipher,
                  font=("Arial Bold", 10, "bold"),
                  relief="flat",
                  background=BUTTON_COLOR)  # Кнопка шифрования
btn_Code.bind("<Enter>", on_enter)
btn_Code.bind("<Leave>", on_leave)
btn_Code.place(relx=0.01, rely=0.93)

btn_Download_File = Button(window,
                           text="Загрузить",
                           command=open_file,
                           font=("Arial Bold", 10, "bold"),
                           relief="flat",
                           background=BUTTON_COLOR)  # Кнопка загрузки из файла
btn_Download_File.bind("<Enter>", on_enter)
btn_Download_File.bind("<Leave>", on_leave)
btn_Download_File.place(relx=0.755, rely=0.93)

btn_Download_File = Button(window,
                           text="Выгрузить",
                           command=save_file,
                           font=("Arial Bold", 10, "bold"),
                           relief="flat",
                           background=BUTTON_COLOR)  # Кнопка выгрузки в файл
btn_Download_File.bind("<Enter>", on_enter)
btn_Download_File.bind("<Leave>", on_leave)
btn_Download_File.place(relx=0.874, rely=0.93)

btn_Clear_Input = Button(
    window,
    text="C",
    command=clear_input,
    font=("Arial Bold", 10, "bold"),
    relief="flat",
    background=BUTTON_COLOR)  # Кнопка очистки поля ввода текста
btn_Clear_Input.bind("<Enter>", on_enter)
btn_Clear_Input.bind("<Leave>", on_leave)
btn_Clear_Input.place(relx=0.96, rely=0.02)

btn_Clear_Output = Button(
    window,
    text="C",
    command=clear_output,
    font=("Arial Bold", 10, "bold"),
    relief="flat",
    background=BUTTON_COLOR)  # Кнопка очистки поля вывода текста
btn_Clear_Output.bind("<Enter>", on_enter)
btn_Clear_Output.bind("<Leave>", on_leave)
btn_Clear_Output.place(relx=0.96, rely=0.57)

# Прогресс бар
s = Style(window)
s.layout("LabeledProgressbar", [('LabeledProgressbar.trough', {
    'children': [('LabeledProgressbar.pbar', {
        'side': 'left',
        'sticky': 'ns'
    }), ("LabeledProgressbar.label", {
        "sticky": ""
    })],
    'sticky':
    'nswe'
})])

Progres_bar = Progressbar(window,
                          orient="horizontal",
                          length=100,
                          style="LabeledProgressbar")
Progres_bar.place(relx=0.137, rely=0.931, relwidth=0.6, relheight=0.05)

window.mainloop()
