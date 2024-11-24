import redis
from tkinter import *
from tkinter import ttk
from tkinter import colorchooser, messagebox, font
import re


# 1 пункт
def choose_color():
    color = colorchooser.askcolor()
    if color:
        color_font_var.set(color[1])

     
def is_valid_size(value):
    return re.match('^\d{,2}$' , value) is not None

def is_valid_key(value):
    return re.fullmatch('^\d{,5}-[A-Za-z]+-[A-Za-z0-9]+$', value) is not None
    
def refresh_keys():
    keys = []
    for key in client.keys():
        text = key.decode()
        if re.match('22303-Demoev-[A-Za-z0-9]+$', text):
            keys.append(text)
    style_text_box['values'] = keys
    
def save_settings():
    key = key_entry.get()
    name_font = name_font_var.get()
    size_font = size_font_entry.get()
    color_font = color_font_var.get()
    type_font = type_font_var.get()
    
    if not key:
        messagebox.showwarning("Ошибка", "Введите ключ для сохранения")
        return
    
    if not is_valid_key(key):
        messagebox.showwarning("Ошибка", "Неверно введен ключ (<номер группы (до 5 чисел)>-<фамилия>-<ключ>)")
        return

    if not name_font:
        messagebox.showwarning("Ошибка", "Выберите название шрифта")
        return
    
    if not size_font:
        messagebox.showwarning("Ошибка", "Введите размер шрифта")
        return
    
    if not color_font:
        messagebox.showwarning("Ошибка", "Выберите цвет шрифта")
        return
    
    info = {'name_font': name_font,
            'size_font': size_font,
            'color_font': color_font,
            'type_font': type_font}
    
    for key_user in client.keys():
        if key == key_user.decode():
            messagebox.showwarning('Ошибка', 'Такой ключ уже существует')
            return
    
    client.hmset(key, info)
    refresh_keys()
    messagebox.showinfo("Успех", "Настройки сохранены")

    
def display_text(event):
    text = text_entry.get()
    selected = style_text_box.get()
    
    if selected:
        style_font = client.hgetall(selected)
        if style_font:
            name_font = style_font[b'name_font'].decode()
            size_font = int(style_font[b'size_font'].decode())
            color_font = style_font[b'color_font'].decode()
            type_font = style_font[b'type_font'].decode()
            
            if type_font == 'italic':
                font_selected = font.Font(family=name_font, size=size_font, slant=type_font)
            else:
                font_selected = font.Font(family=name_font, size=size_font, weight=type_font)
            text_label.config(text=text, font=font_selected, fg=color_font)
    else:
        text_label.config(text=text)

client = redis.Redis(host='192.168.112.103', password='student')

app = Tk()
app.title("Настройки текста пользователя")
app.geometry('570x650')

frame = Frame(app, borderwidth=4, relief=SOLID)
frame.pack(fill=X, padx=10, pady=10)

Label(frame, text='Ключ для сохранения: ', font=('Arial', 16)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
#check_key = (app.register(is_valid_key), "%P")
key_entry = Entry(frame, font=('Arial', 16)) #, validate="key", validatecommand=check_key)
key_entry.grid(row=0, column=1, padx=10, pady=10)

Label(frame, text='Название шрифта: ', font=('Arial', 16)).grid(row=1, column=0, padx=10, pady=10, sticky='w')
name_font = font.families()
name_font_var = StringVar()
name_font_box = ttk.Combobox(frame, font=('Arial', 16),textvariable=name_font_var, values=name_font, state="readonly")
name_font_box.grid(row=1, column=1, padx=10, pady=10)

Label(frame, text='Размер шрифта: ', font=('Arial', 16)).grid(row=2, column=0, padx=10, pady=10, sticky='w')
check_size = (frame.register(is_valid_size), "%P")
size_font_entry = Entry(frame, font=('Arial', 16), validate="key", validatecommand=check_size)
size_font_entry.grid(row=2, column=1, padx=10, pady=10)

Label(frame, text='Цвет шрифта: ', font=('Arial', 16)).grid(row=3, column=0, padx=10, pady=10, sticky='w')
color_font_var = StringVar()
color_button = Button(frame, text="Выбрать цвет", font=('Arial', 16), command=choose_color)
color_button.grid(row=3, column=1, padx=10, pady=10)

Label(frame, text='Начертание шрифта: ', font=('Arial', 16)).grid(row=4, column=0, padx=10, pady=10, sticky='w')
type = ['normal', 'bold', 'italic']
type_font_var = StringVar(value=type[0])
type_font_box = ttk.Combobox(frame, font=('Arial', 16),textvariable=type_font_var, values=type, state="readonly")
type_font_box.grid(row=4, column=1, padx=10, pady=10)

save_button = Button(frame, text="Сохранить настройки", font=('Arial', 16), command=save_settings)
save_button.grid(row=5, columnspan=2, padx=10, pady=10)

frame2 = Frame(app, borderwidth=4, relief=SOLID)
frame2.pack(fill=X, padx=10, pady=10)
Label(frame2, text="Текст для отображения:", font=('Arial', 16)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
text_entry = Entry(frame2, font=('Arial', 16))
text_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')
text_entry.bind("<KeyRelease>", display_text)

Label(frame2, text='Готовые стили: ', font=('Arial', 16)).grid(row=1, column=0, padx=10, pady=10, sticky='w')
style_text_box = ttk.Combobox(frame2, font=('Arial', 16), state="readonly")
style_text_box.bind("<<ComboboxSelected>>", display_text)
style_text_box.grid(row=1, column=1, padx=10, pady=10)
refresh_keys()
    
text_label = Label(frame2, text='', font=('Arial', 16))
text_label.grid(row=3, columnspan=2, padx=10, pady=10, sticky='n')

app.mainloop()