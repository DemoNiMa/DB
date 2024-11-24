import redis
from tkinter import *
from tkinter import ttk
from tkinter import colorchooser, messagebox, font
import re

def is_valid_count(value):
    return re.match('^\d{,2}$' , value) is not None

def refresh_sporstman():
    s = []
    sportsmens_points_listbox.delete(0, 2)
    for sportsman in sportsmans:
        points = 0
        for keys in client.keys():
            pattern = f'22303-Demoev-[А-Яа-я0-9]+-{sportsman}+$'
            key = keys.decode()
            if re.match(pattern, key):
                sportsman_key = client.hgetall(key)
                points += int(sportsman_key[b'count'])
            text = f'{sportsman} - {points} баллов'
        s.append(text)
        s = sorted(s, key=lambda x: int(x.split('-')[1].split()[0]), reverse=True)
    for data in s:
        sportsmens_points_listbox.insert(END, data)

def save_settings():
    referee = referees_entry.get()
    sportsman = sportsmans_var.get()
    count = count_entry.get()
    
    if not referee:
        messagebox.showwarning("Ошибка", "Выберите судью")
        return
    
    if not sportsman:
        messagebox.showwarning("Ошибка", "Выберите спорстмена")
        return

    if not count:
        messagebox.showwarning("Ошибка", "Введите количество баллов")
        return
    
    key = f'22303-Demoev-{referee}-{sportsman}'
    
    for key_user in client.keys():
        if key == key_user.decode():
            sportsman_referee = client.hgetall(key)
            count_new = int(sportsman_referee[b'count'].decode())
            count_new += int(count)
            
            info = {'referee': referee,
                    'sportsman': sportsman,
                    'count': count_new}
            
            client.hmset(key, info)
            refresh_sporstman()
            messagebox.showinfo("Успех", "Данные сохранены")
            return

    info = {'referee': referee,
        'sportsman': sportsman,
        'count': count}
            
    client.hmset(key, info)
    refresh_sporstman()
    messagebox.showinfo("Успех", "Данные сохранены")
    
client = redis.Redis(host='192.168.112.103', password='student')

app = Tk()
app.title("Мониторинг спортивных соревнований")
app.geometry('570x650')

frame = Frame(app, borderwidth=4, relief=SOLID)
frame.pack(fill=X, padx=10, pady=10)

Label(frame, text='Выберите судью: ', font=('Arial', 16)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
referees = ['Судья1', 'Судья2', 'Судья3']
referees_var = StringVar()
referees_entry = ttk.Combobox(frame, font=('Arial', 16), textvariable=referees_var, values=referees, state="readonly")
referees_entry.grid(row=0, column=1, padx=10, pady=10)

Label(frame, text='Выберите спортсмена: ', font=('Arial', 16)).grid(row=1, column=0, padx=10, pady=10, sticky='w')
sportsmans = ['Спортсмен1', 'Спортсмен2', 'Спортсмен3']
sportsmans_var = StringVar()
sportsmans_entry = ttk.Combobox(frame, font=('Arial', 16), textvariable=sportsmans_var, values=sportsmans, state="readonly")
sportsmans_entry.grid(row=1, column=1, padx=10, pady=10)

Label(frame, text='Количество баллов: ', font=('Arial', 16)).grid(row=2, column=0, padx=10, pady=10, sticky='w')
check_count = (frame.register(is_valid_count), "%P")
count_entry = Entry(frame, font=('Arial', 16), validate="key", validatecommand=check_count)
count_entry.grid(row=2, column=1, padx=10, pady=10)

save_button = Button(frame, text="Сохранить данные", font=('Arial', 16), command=save_settings)
save_button.grid(row=5, columnspan=2, padx=10, pady=10)

frame2 = Frame(app, borderwidth=4, relief=SOLID)
frame2.pack(fill=X, padx=10, pady=10)

Label(frame2, text='Список спортсменов: ', font=('Arial', 16)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
sportsmens_points_listbox = Listbox(frame2, font=('Arial', 14), width=25)
refresh_sporstman()
sportsmens_points_listbox.grid(row=0, column=1, padx=10, pady=10)

app.mainloop()

client = redis.Redis(host='192.168.112.103', password='student')
sportsmans = ['Спортсмен1', 'Спортсмен2', 'Спортсмен3']
for key in client.keys():
    for sportsman in sportsmans:
        pattern = f'22303-Demoev-[А-Яа-я0-9]+-{sportsman}+$'
        if re.match(pattern, key.decode()):
            sportsman_key = client.hgetall(key)
            s = sportsman_key[b'referee'].decode()
            ss = sportsman_key[b'sportsman'].decode()
            sss = sportsman_key[b'count'].decode()
            print(s, ss, sss)
