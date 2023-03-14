from threading import Thread
from pygame import mixer
import sqlite3
from tkinter import *
from tkinter import ttk
from datetime import datetime as dt
from time import sleep

root = Tk()

alarmes = sqlite3.connect("Alarms.db")
cursor = alarmes.cursor()
banco = [rw for rw in cursor.execute("SELECT * FROM Alarms")]


def watch():
    tempo = dt.now()
    dia_semana = tempo.strftime("%A")
    time = tempo.strftime("%H:%M:%S")
    dia = tempo.day
    mes = tempo.strftime("%b")
    ano = tempo.strftime("%Y")
    Timer.config(text=time)
    Timer.after(200, watch)
    Date.config(text=f"{dia_semana} {dia}/{mes}/{ano}")


Timer = Label(root, text="", bg="gray70", fg="black", font="Arial 30")
Timer.place(relx=0.08, rely=0.1, relwidth=0.4, relheight=0.1)
Date = Label(root, text="", bg="gray70", fg="black", font="Arial 13")
Date.place(relx=0.08, rely=0.2, relwidth=0.4, relheight=0.03)

watch()

vSunday = IntVar()
vMonday = IntVar()
vTuesday = IntVar()
vWednesday = IntVar()
vThursday = IntVar()
vFriday = IntVar()
vSaturnday = IntVar()


def PlayAlarm(info):
    pop = Toplevel(root)
    pop.title("ALARM")
    pop.geometry("500x300")
    pop.config(bg="white")
    label = Label(pop, text=f"Alarm\n{info[0]}:{info[1]}:{info[2]}\n{info[4]}", font="Arial 30", bg="white")
    label.place(relx=0.15, rely=0.1, relwidth=0.7, relheight=0.8)
    mixer.init()
    mixer.Sound("mixkit-morning-clock-alarm-1003.wav").play()
    sleep(5)
    mixer.stop()


def VerifyAlarm():
    while True:
        for alarm in banco:
            sleep(0.032)
            if (f"{str(dt.now().strftime('%A'))[:2]} {str(dt.now().hour)}/{str(dt.now().minute)}/{str(dt.now().second)}"
                    == f"{alarm[4]} {alarm[0]}/{alarm[1]}/{alarm[2]}"):
                PlayAlarm(alarm)
                break


if __name__ == '__main__':
    Thread(target=VerifyAlarm).start()


def Limpar():
    hour_entry.delete(0, END)
    minute_entry.delete(0, END)
    second_entry.delete(0, END)
    nome_entry.delete(0, END)
    ChBt_Sun.deselect()
    ChBt_Mon.deselect()
    ChBt_Tue.deselect()
    ChBt_Wed.deselect()
    ChBt_Thu.deselect()
    ChBt_Fri.deselect()
    ChBt_Satu.deselect()


def Add_Alarm():
    hra = hour_entry.get()
    mnuto = minute_entry.get()
    sgundo = second_entry.get()
    day = ""
    listdays = {"Su": str(vSunday.get()), "Mo": str(vMonday.get()),
                "Tu": str(vTuesday.get()), "We": str(vWednesday.get()),
                "Th": str(vThursday.get()), "Fr": str(vFriday.get()),
                "Sa": str(vSaturnday.get())}
    for Day, key in listdays.items():
        if key == "1":
            day += Day
            day += " "
    nme = nome_entry.get()
    banco.append((hra, mnuto, sgundo, day, nme))
    cursor.execute("INSERT INTO Alarms (Hour, Minute, Second, Day, Name) VALUES (?, ?, ?, ?, ?)",
                   (hra, mnuto, sgundo, day, nme))
    alarmes.commit()
    title.insert("", END, values=(hra, mnuto, sgundo, day, nme))
    Limpar()


def Remove_Alarm():
    col1, col2, col3, col4, col5 = title.item(title.selection()[0], "values")
    cursor.execute("""DELETE FROM Alarms WHERE Hour = ? and Minute = ? and Second = ? and Day = ? and Name = ?""",
                   (str(col1), str(col2), str(col3), str(col4), str(col5)))
    alarmes.commit()
    selected_item = title.selection()[0]
    title.delete(selected_item)


root.title("Alarmes")
root.configure(background="gray70")
root.geometry("1000x600")
root.resizable(False, False)

Frame(root, bd=0, bg='black').place(relx=0.55, rely=0.02, relwidth=0.005, relheight=0.96)

title = ttk.Treeview(root, height=0.05, column=("con1", "con2", "con3", "con4", "con4", "con5"))
title.heading("#0", text="")
title.heading("#1", text="Hora")
title.heading("#2", text="Min")
title.heading("#3", text="Seg")
title.heading("#4", text="Dias")
title.heading("#5", text="Nome")
title.column("#0", width=0)
title.column("#1", width=35)
title.column("#2", width=35)
title.column("#3", width=35)
title.column("#4", width=130)
title.column("#5", width=150)
title.place(relx=0.56, rely=0.02, relwidth=0.41, relheight=0.95)

for hora, minuto, segundo, dias, nome in cursor.execute("SELECT * FROM Alarms"):
    title.insert("", END, values=(hora, minuto, segundo, dias, nome))

scroll = Scrollbar(root, orient="vertical")
title.configure(yscroll=title)
scroll.place(relx=0.97, rely=0.02, relwidth=0.025, relheight=0.95)

Hour = Label(root, text="Hora", bg="gray70")
Hour.place(relx=0.06, rely=0.5, relwidth=0.1, relheight=0.1)
hour_entry = Entry(root, bd=0, bg='white', fg='black')
hour_entry.place(relx=0.06, rely=0.57, relwidth=0.1, relheight=0.04)
Minute = Label(root, text="Minuto", bg="gray70")
Minute.place(relx=0.22, rely=0.5, relwidth=0.1, relheight=0.1)
minute_entry = Entry(root, bd=0, bg='white', fg='black')
minute_entry.place(relx=0.22, rely=0.57, relwidth=0.1, relheight=0.04)
Second = Label(root, text="Segundo", bg="gray70")
Second.place(relx=0.4, rely=0.5, relwidth=0.1, relheight=0.1)
second_entry = Entry(root, bd=0, bg='white', fg='black')
second_entry.place(relx=0.4, rely=0.57, relwidth=0.1, relheight=0.04)
Nome = Label(root, text="Nome", bg="gray70")
Nome.place(relx=0.13, rely=0.65, relwidth=0.1, relheight=0.03)
nome_entry = Entry(root, bd=0, bg='white', fg='black')
nome_entry.place(relx=0.16, rely=0.69, relwidth=0.21, relheight=0.04)

bt_Salvar = Button(root, text="Salvar", bd=0, command=Add_Alarm)
bt_Salvar.place(relx=0.165, rely=0.75, relwidth=0.2, relheight=0.05)
bt_Excluir = Button(root, text="Excluir", bd=0, command=Remove_Alarm)
bt_Excluir.place(relx=0.165, rely=0.82, relwidth=0.2, relheight=0.05)
bt_Alterar = Button(root, text="Alterar", bd=0)
bt_Alterar.place(relx=0.165, rely=0.89, relwidth=0.2, relheight=0.05)

ChBt_Sun = Checkbutton(root, text="Sun", bd=0, bg="gray70", variable=vSunday, onvalue=1, offvalue=0)
ChBt_Mon = Checkbutton(root, text="Mon", bd=0, bg="gray70", variable=vMonday, onvalue=1, offvalue=0)
ChBt_Tue = Checkbutton(root, text="Tue", bd=0, bg="gray70", variable=vTuesday, onvalue=1, offvalue=0)
ChBt_Wed = Checkbutton(root, text="Wed", bd=0, bg="gray70", variable=vWednesday, onvalue=1, offvalue=0)
ChBt_Thu = Checkbutton(root, text="Thu", bd=0, bg="gray70", variable=vThursday, onvalue=1, offvalue=0)
ChBt_Fri = Checkbutton(root, text="Fri", bd=0, bg="gray70", variable=vFriday, onvalue=1, offvalue=0)
ChBt_Satu = Checkbutton(root, text="Satu", bd=0, bg="gray70", variable=vSaturnday, onvalue=1, offvalue=0)
ChBt_Sun.place(relx=0.03, rely=0.62, relwidth=0.07, relheight=0.025)
ChBt_Mon.place(relx=0.10, rely=0.62, relwidth=0.07, relheight=0.025)
ChBt_Tue.place(relx=0.17, rely=0.62, relwidth=0.07, relheight=0.025)
ChBt_Wed.place(relx=0.24, rely=0.62, relwidth=0.07, relheight=0.025)
ChBt_Thu.place(relx=0.31, rely=0.62, relwidth=0.07, relheight=0.025)
ChBt_Fri.place(relx=0.38, rely=0.62, relwidth=0.07, relheight=0.025)
ChBt_Satu.place(relx=0.45, rely=0.62, relwidth=0.07, relheight=0.025)

root.mainloop()
