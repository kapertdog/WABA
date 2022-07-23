import keyboard
from pystray import MenuItem as item
import pystray
from PIL import Image
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
import notification

title = "WABA (v.Dev_A)"
show_notify = True

window = tk.Tk()
window.title(title)

hiding_to_tray = tk.BooleanVar()
hiding_to_tray.set(True)

with Image.open("logo.ico") as i:
    i_logo = i.copy()
with Image.open("exit.ico") as i:
    i_exit = i.copy()


def full_quit():
    window.destroy()


def quit_window(icon, _):  # item
    icon.stop()
    full_quit()


def show_window(icon, _):
    icon.stop()
    window.after(0, window.deiconify)


def debug_notify(icon, _):
    icon.notify("Вот так должно выглядеть нормальное уведомление", "Пиздец")


def withdraw_window():
    # print(f"Hiding: {hiding_to_tray.get()}\nKey pressed: {keyboard.is_pressed('shift')}")
    if hiding_to_tray.get() and not keyboard.is_pressed("shift"):
        window.withdraw()
        tray_menu = (item('Показать', show_window, default=True), item('Закрыть', quit_window), item("DEBUG", debug_notify))
        icon = pystray.Icon("WABA", i_logo, title, tray_menu)
        global show_notify
        if show_notify:
            notification.notify(
                title="WABA Скрылась в трее",
                msg="Это можно выключить в настройках",
                icon_path="logo.ico",
                duration=6
            )
            # TODO: Нужно разобраться с этими нормальными уведомлениями.
            #       Запускать иконку при старте приложения и т. п.
            # icon.notify(
            #     title="WABA скрылась в трее",
            #     message="Это можно выключить в настройках",
            # )
            show_notify = False
        icon.run()
    else:
        if msg.askyesno("Вы уверены?", "Приложение полностью остановится"):
            full_quit()


menu = tk.Menu(window)

cascade_settings = tk.Menu(menu, tearoff=0)

cascade_settings.add_checkbutton(
    label="Сворачивать в трей",
    # command=hiding_to_tray_switch,
    offvalue=False, onvalue=True,
    variable=hiding_to_tray
)
cascade_settings.add_separator()
cascade_settings.add_command(label="Закрыть приложение", command=window.destroy)

menu.add_cascade(label="Настройки...", menu=cascade_settings)

tab_main = ttk.Notebook()
tab_main.grid()

window.config(menu=menu)
window.protocol('WM_DELETE_WINDOW', withdraw_window)
window.geometry("400x250")


window.iconbitmap("logo.ico")
window.mainloop()
