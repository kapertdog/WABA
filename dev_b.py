# -*- coding: utf-8 -*-
"""
    WABA (Windows automatic brightness adjustment) v.DEV_B
"""
import os
import threading
import PIL.Image
import screen_brightness_control as sbc
import imageio as iio
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msb
from statistics import mean
from pathlib import Path
from autostart import autostart
import pystray
import yaml
import time

title = "Waba (v.Dev_B)"
version = "0.2.4.1"
github_tag = "dev_b_pre-4"
edition = "venv"  # Всего 3 издания: "venv", "folder" и "exe"

# camera = iio.get_reader("<video0>")
# screenshot = camera.get_data(0)

# print("Размер скрина:", screenshot.shape)
# print("Среднее яркости:", int(screenshot.mean()))
# input()

"""
    Defaults
"""
# Default settings values
settings_version = 6
settings_path = Path(os.getenv("APPDATA", ""), "waba", "settings.yaml")
waba_user_files_path = Path(os.getenv("APPDATA", ""), "waba")
settings = {
    "_venv_dir": os.getcwd(),
    "settings_version": settings_version,
    "theme": "dark",
    "autostart": False,
    "checking_for_updates": False,
    # features
    "features": {
        # Обновляются только после перезапуска!!
        "autoupdate": False,
        "autostart": True,
        "custom_icons": True,  # Пока ничего не делает
        "safe_math_mode": True,
        "threading": True,
        "notifications": True,
        "tray": True,
    },
    # tray
    "hiding_to_tray": True,
    "hide_after_start": False,
    "im_hiding_message": True,
    "notifications": True,
    # display
    "device": "<video0>",
    "display": None,
    # snapshot
    "cycle_timer": 60,
    "timer_tick_delay": 10,
    "snapshot_delay": 1,
    "amount_of_shots": 1,
    # math
    "do_use_custom_method": False,
    "module_method": "{} * 100 // 255 ** 2 // 100",
}

# Потом по желанию сокращу
features_values_of_switches = {
    "autoupdate": {
        True: {
            "main": True,
            "tkinter": "normal",
        },
        False: {
            "main": False,
            "tkinter": "disabled"
        }
    },
    "autostart": {
        True: {
            "tray": True,
            "tkinter": "normal",
        },
        False: {
            "tray": False,
            "tkinter": "disabled",
        }
    },
    "notifications": {
        True: {
            "tkinter": "normal",
        },
        False: {
            "tkinter": "disabled"
        }
    },
    "threading": {
        True: {
            "tkinter": "normal",
            "tray": True,
            "thread": True,
        },
        False: {
            "tkinter": "disabled",
            "tray": False,
            "thread": False
        }
    },
    "tray": {
        True: {
            "tkinter": "normal",
            "main": True
        },
        False: {
            "tkinter": "disabled",
            "main": False
        }
    }
}

timer_values_of_names = {
    "30 с.": 30,
    "1 м.": 60,
    "5 м.": 300,
    "10 м.": 600,
    "15 м.": 900,
    "30 м.": 1800,
    "1 ч.": 3600,
    "": None,
    "Не обновлять": None,
    "30 секунд": 30,
    "1 мин.": 60,
    "5 мин.": 300,
    "10 мин.": 600,
    "15 мин.": 900,
    "30 мин.": 1800,
    "1 час": 3600,
}

timer_names_of_values = dict()
for key in timer_values_of_names:
    timer_names_of_values[timer_values_of_names[key]] = key

"""
    Settings
"""


def f_settings(keyword: str, element: str) -> str:
    return features_values_of_switches[keyword][settings["features"][keyword]][element]


def migrate_settings(data):
    def check(old, new):
        ret = dict()
        for name in new:
            if name in old:
                # Если элемент есть в старой версии
                if type(new[name]) == dict:
                    # Но это словарь
                    ret[name] = check(old[name], new[name])
                else:
                    ret[name] = old[name]
            else:
                # Если элемент вообще отсутствует
                print("# Добавляю недостающий элемент", name)
                ret[name] = new[name]
        return ret

    global settings
    print("-=- Происходит миграция -=-")
    data = check(data, settings)
    data["settings_version"] = settings_version
    print("-=-  Успешная миграция  -=-")
    return data


def save_settings(path: Path = settings_path):
    with path.open("w+") as s:
        yaml.dump(settings, s, default_flow_style=False)


def load_settings(path: Path = settings_path):
    # Path(os.getenv("APPDATA"), "Microsoft", "Window", "Start Menu", "Programs", "Startup")
    global settings
    if path.exists():
        with path.open("r+") as s:
            data = yaml.safe_load(s)
        if data["settings_version"] != settings_version:
            try:
                settings = migrate_settings(data)
            except Exception as err:
                print("# Ошибка при миграции!!", err, "\n# Файл настроек будет перезаписан")
                msb.showerror("Waba: ошибка миграции настроек", f"{err}\n"
                                                                f"Настройки будут сброшены!")
            save_settings(path)
        else:
            settings = data
    else:
        if not path.parent.exists():
            path.parent.mkdir()
        save_settings(path)
    if Path(settings["_venv_dir"]).exists():
        ...
    else:
        settings["_venv_dir"] = str(Path.cwd())
        save_settings(path)
    os.chdir(settings["_venv_dir"])
    return settings


def load_version_file():
    if Path("version.yaml").exists():
        with open("version.yaml") as v:
            data = yaml.safe_load(v)
        global edition, github_tag, version
        edition = data["edition"]
        github_tag = data["version"]
        version = f'{data["version"][:7]}'


"""
    Functions
"""


# noinspection GrazieInspection
def get_brightness(device: str = "<video0>", wait: int = 0, repeats: int = 1):
    """
    Returns the brightness received from the camera

    :param device: Device mode and name
    :param wait: Waiting time before taking a picture (seconds)
    :param repeats: Amount of pictures (from 1 to inf.)
    :return: int value from 0 to 255
    """
    brightness_list = list()

    with iio.get_reader(device) as camera:
        for _ in range(repeats):
            time.sleep(wait)
            screenshot = camera.get_data(0)
            brightness_list.append(int(screenshot.mean()))
    # noinspection PyBroadException
    try:
        return int(mean(brightness_list))
    except Exception as err:
        msb.showerror("Waba: Ошибка настроек", f'Возможно, вы указали "0" в строке "amount_of_shots".\n'
                                               f'Так нельзя.\n\n'
                                               f'Ошибка Python: {err}')


def calc_custom(value: int, func: str):
    if settings["features"]["safe_math_mode"]:
        return int(eval(func.format(value), {"value": value, "x": value}))
    else:
        return eval(func.format(value))


def calc_value_v1(value: int):
    result = value * 100 // 255
    result = result ** 2 // 100
    return result


def calc_value_v2(value: int, *args: int):
    result = 0
    count = len(args)
    result += (1 - value) ** count * value * 0
    if args != ():
        for i in args:
            result += count * (1 - value) ** 2 * value * i
    result += value ** count * 255
    return result


def update_brightness(icon: pystray.Icon = None, *_, method: str = None):
    load_settings()
    if settings["do_use_custom_method"] and (method is None):
        method = settings["module_method"]
    d = settings["display"]
    old_b = sbc.get_brightness(d)[0]
    cam_b = get_brightness(settings["device"], settings["snapshot_delay"], settings["amount_of_shots"])
    if method:
        m_b = calc_custom(cam_b, method)
    else:
        m_b = calc_value_v1(cam_b)
    sbc.set_brightness(m_b, d)
    if icon is not None and settings["notifications"]:
        icon.notify(
            f"{cam_b}/255 | {old_b}% -> {m_b}%",
            "Яркость обновлена",
        )
    return d, old_b, cam_b, m_b


thread_alive = True


def timer_thread(_):
    last_time = 0
    while thread_alive:
        if settings["cycle_timer"]:
            if int(time.monotonic()) - last_time > settings["cycle_timer"]:
                try:
                    update_brightness()
                except Exception as err:
                    msb.showerror("Waba: Сбой", f"{err}")
                last_time = int(time.monotonic())
        time.sleep(settings["timer_tick_delay"])


"""
    Interface
"""


def get_interface():
    ...


"""
    Main things
"""


def github_page():
    # with open("about.txt", "r+", encoding="UTF-8") as f:
    #     about_txt = f.read()
    # msb.showinfo(
    #     "Waba: about",
    #     about_txt
    # )
    __import__("webbrowser").open_new_tab(r"https://github.com/kapertdog/WABA")


def about():
    with open("about.txt", "r+", encoding="UTF-8") as f:
        about_txt = f.read()
    msb.showinfo(
        "Waba: about",
        about_txt
    )
    # __import__("webbrowser").open_new_tab(r"https://github.com/kapertdog/WABA")


def main():
    main_window = tk.Tk()
    main_window.title("Waba - настройки")
    ...
    top_frame = tk.Frame(main_window)
    bottom_frame = tk.Frame(main_window, padx=10, pady=10, background="#ABB2B9")
    ...
    left_side_frame = tk.Frame(top_frame)
    right_side_frame = tk.Frame(top_frame)
    ...

    def submit(*_):
        # settings["hide_after_start"] =
        ...
        if settings["autostart"] != autostart_chbtn_var.get():
            settings["autostart"] = autostart(autostart_chbtn_var.get())
        settings["checking_for_updates"] = checking_for_updates_chbtn_var.get()
        settings["hiding_to_tray"] = hiding_to_tray_chbtn_var.get()
        settings["hide_after_start"] = hiding_when_start_chbtn_var.get()
        settings["notifications"] = notifications_chbtn_var.get()
        settings["cycle_timer"] = timer_values_of_names[update_rate_lst_var.get()]
        settings["display"] = display_list_var.get()
        settings["snapshot_delay"] = spinbox_shot_delay_var.get()
        settings["do_use_custom_method"] = do_use_custom_method_chbtn_var.get()
        settings["module_method"] = entry_custom_func_var.get()
        save_settings()
        check()

    submit_button = tk.Button(
        bottom_frame,
        command=submit,
        text="Применить",
        state="disabled",
        relief=tk.GROOVE,
    )
    ...
    hiding_to_tray_chbtn_var = tk.BooleanVar()
    hiding_when_start_chbtn_var = tk.BooleanVar()
    notifications_chbtn_var = tk.BooleanVar()
    autostart_chbtn_var = tk.BooleanVar()
    checking_for_updates_chbtn_var = tk.BooleanVar()
    update_rate_lst_var = tk.StringVar()
    display_list_var = tk.StringVar()
    spinbox_shot_delay_var = tk.IntVar()
    do_use_custom_method_chbtn_var = tk.BooleanVar()
    entry_custom_func_var = tk.StringVar()

    def update():
        hiding_to_tray_chbtn_var.set(settings["hiding_to_tray"])
        hiding_when_start_chbtn_var.set(settings["hide_after_start"])
        notifications_chbtn_var.set(settings["notifications"])
        autostart_chbtn_var.set(settings["autostart"])
        checking_for_updates_chbtn_var.set(settings["checking_for_updates"])
        display_list_var.set(settings["display"])
        update_rate_lst_var.set(timer_names_of_values[settings["cycle_timer"]])
        spinbox_shot_delay_var.set(settings["snapshot_delay"])
        do_use_custom_method_chbtn_var.set(settings["do_use_custom_method"])
        entry_custom_func_var.set(settings["module_method"])
    update()
    ...

    def check():
        changes = 0
        try:
            changes += int(hiding_to_tray_chbtn_var.get() != settings["hiding_to_tray"])
            changes += int(hiding_when_start_chbtn_var.get() != settings["hide_after_start"])
            changes += int(notifications_chbtn_var.get() != settings["notifications"])
            changes += int(autostart_chbtn_var.get() != settings["autostart"])
            changes += int(checking_for_updates_chbtn_var.get() != settings["checking_for_updates"])
            changes += int(timer_values_of_names[update_rate_lst_var.get()] != settings["cycle_timer"])
            changes += int(display_list_var.get() != settings["display"])
            changes += int(spinbox_shot_delay_var.get() != settings["snapshot_delay"])
            changes += int(do_use_custom_method_chbtn_var.get() != settings["do_use_custom_method"])
            changes += int(entry_custom_func_var.get() != settings["module_method"])
        except Exception as err:
            msb.showerror("Waba: сбой при проверке настроек", f"{err}")
        if changes == 0:
            submit_button.config(state="disabled")
            main_window.update()
        else:
            submit_button.config(state="active")
            main_window.update()
        check_two()
        ...

    ...
    waba_title_image = tk.PhotoImage(file="resources/waba_title.png")
    waba_image = tk.Label(
        left_side_frame,
        image=waba_title_image,
        state="active",
    )
    waba_image.image_ref = waba_title_image
    waba_image.pack()

    hiding_to_tray_chbtn = tk.Checkbutton(
        left_side_frame,
        text="Сворачивать в трей",
        padx=10,
        anchor="w",
        command=check,
        state=f_settings("tray", "tkinter"),
        variable=hiding_to_tray_chbtn_var
    )
    hiding_to_tray_chbtn.pack(fill=tk.X)

    hiding_when_start_chbtn = tk.Checkbutton(
        left_side_frame,
        text="Запускать свёрнутым",
        padx=10,
        anchor="w",
        command=check,
        state=f_settings("tray", "tkinter"),
        variable=hiding_when_start_chbtn_var
    )
    hiding_when_start_chbtn.pack(fill=tk.X)

    notifications_chbtn = tk.Checkbutton(
        left_side_frame,
        text="Уведомления",
        padx=10,
        anchor="w",
        command=check,
        state=f_settings("notifications", "tkinter"),
        variable=notifications_chbtn_var
    )
    notifications_chbtn.pack(fill=tk.X)

    autostart_chbtn = tk.Checkbutton(
        left_side_frame,
        text="Автозапуск",
        padx=10,
        anchor="w",
        command=check,
        state=f_settings("autostart", "tkinter"),
        variable=autostart_chbtn_var
    )
    autostart_chbtn.pack(fill=tk.X)

    checking_for_updates_chbtn = tk.Checkbutton(
        left_side_frame,
        text="Искать обновления",
        padx=10,
        anchor="w",
        command=check,
        state=f_settings("autoupdate", "tkinter"),
        variable=checking_for_updates_chbtn_var
    )
    checking_for_updates_chbtn.pack(fill=tk.X)
    ...
    lbl_update_rate_lst = tk.Label(
        right_side_frame,
        text="Обновлять каждые:",
        padx=10,
        anchor="w",
        state=f_settings("threading", "tkinter")
    )
    lbl_update_rate_lst.pack(fill=tk.X)

    update_rate_lst = ttk.Combobox(
        right_side_frame,
        postcommand=check,
        validatecommand=check,
        invalidcommand=check,
        textvariable=update_rate_lst_var,
        values=[
            "Не обновлять",
            "30 секунд",
            "1 мин.",
            "5 мин.",
            "10 мин.",
            "15 мин.",
            "30 мин.",
            "1 час"
        ],
        state=f_settings("threading", "tkinter")
    )
    update_rate_lst.pack(fill=tk.X)

    lbl_display_lst = tk.Label(
        right_side_frame,
        text="Дисплей:",
        padx=10,
        anchor="w"
    )
    lbl_display_lst.pack(fill=tk.X)

    display_lst = ttk.Combobox(
        right_side_frame,
        postcommand=check,
        textvariable=display_list_var,
        values=sbc.list_monitors(),
        validate="key",
    )
    display_lst.pack(fill=tk.X)

    lbl_shot_delay = tk.Label(
        right_side_frame,
        text="Задержка кадра: ",
        padx=10,
        anchor="w"
    )
    lbl_shot_delay.pack(fill=tk.X)

    spinbox_shot_delay = tk.Spinbox(
        right_side_frame,
        from_=0,
        to=100,
        command=check,
        textvariable=spinbox_shot_delay_var
    )
    spinbox_shot_delay.pack(fill=tk.X)

    ...
    do_use_custom_func_chbtn = tk.Checkbutton(
        right_side_frame,
        text="Своя функция",
        anchor="w",
        command=check,
        variable=do_use_custom_method_chbtn_var,
    )
    do_use_custom_func_chbtn.pack(fill=tk.X)

    # def validate_func(func):
    #    check()
    #    print(func)
    #    return True
    entry_custom_func = tk.Entry(
        right_side_frame,
        textvariable=entry_custom_func_var,
    )
    entry_custom_func.pack(fill=tk.X)
    ...
    tk.Label(
        top_frame,
        text=f"v.Dev_B ({version})   |   made with 💕",
        foreground="gray"
    ).pack(side=tk.BOTTOM)
    ...

    def upd_bright(icon=None, *_):
        if not icon:
            icon = sys_icon
        # subprocess.run(update_brightness, input=icon)
        try:
            answ = update_brightness(icon)
        except Exception as err:
            msb.showerror("Waba: сбой", f"{err}")
            return
        print(f"-=- {time.ctime()} -=-\n"
              f"Дисплей: {answ[0]}\n"
              f"Яркость до изменения: {answ[1]}/100%\n"
              f"Данные с камеры: {answ[2]}/255\n"
              f"Итоговая яркость: {answ[3]}/100%\n")

    check_button = tk.Button(
        bottom_frame,
        command=upd_bright,
        text="Обновить яркость",
        anchor="center",
        relief=tk.GROOVE,
    )
    check_button.pack(side=tk.LEFT)
    ...
    submit_button.pack(side=tk.RIGHT)
    ...

    def check_two():
        if do_use_custom_method_chbtn_var.get():
            entry_custom_func.config(state="normal")
        else:
            entry_custom_func.config(state="disabled")
        ...
    ...
    left_side_frame.pack(side=tk.LEFT, fill=tk.BOTH)
    right_side_frame.pack(side=tk.LEFT, fill=tk.BOTH)
    top_frame.pack(fill=tk.X)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
    ...
    # main_window.geometry("400x250")
    main_window.geometry("315x250")
    main_window.resizable(width=False, height=False)
    ...

    def show_window():
        main_window.after(0, main_window.deiconify)
        check()

    def quit_all(icon: pystray.Icon = None, *_, window: tk.Tk = main_window, do_destroy=False):
        def q():
            if icon is not None:
                icon.stop()
            if f_settings("threading", "thread"):
                global thread_alive
                thread_alive = False
                thread.join()
            window.withdraw()
            window.deiconify()
            if do_destroy:
                window.destroy()
            else:
                window.quit()

        import loading_screen
        loading_screen.processing(q, "Waba: Завершение работы", "Выходим...")

    def set_timer(_, MenuItem: pystray.MenuItem):
        print("-- update_tray")
        global settings
        settings["cycle_timer"] = timer_values_of_names[MenuItem.text]
        save_settings()
        update()
        check()

    def autostart_checkbox(*_):
        settings["autostart"] = autostart(not settings["autostart"])
        save_settings()
        update()
        check()
    ...
    if f_settings("tray", "main"):
        tray_menu = pystray.Menu(
            pystray.MenuItem("Открыть настройки", show_window, default=True),
            pystray.MenuItem("Обновить яркость", upd_bright, default=False),
            pystray.MenuItem("Обновлять раз в:", pystray.Menu(
                    pystray.MenuItem("Не обновлять", set_timer,
                                     lambda item: settings["cycle_timer"] is None, radio=True),
                    pystray.MenuItem("30 с.", set_timer,
                                     lambda item: settings["cycle_timer"] == 30, radio=True),
                    pystray.MenuItem("1 м.", set_timer,
                                     lambda item: settings["cycle_timer"] == 60, radio=True),
                    pystray.MenuItem("5 м.", set_timer,
                                     lambda item: settings["cycle_timer"] == 300, radio=True),
                    pystray.MenuItem("10 м.", set_timer,
                                     lambda item: settings["cycle_timer"] == 600, radio=True),
                    pystray.MenuItem("15 м.", set_timer,
                                     lambda item: settings["cycle_timer"] == 900, radio=True),
                    pystray.MenuItem("30 м.", set_timer,
                                     lambda item: settings["cycle_timer"] == 1800, radio=True),
                    pystray.MenuItem("1 ч.", set_timer,
                                     lambda item: settings["cycle_timer"] == 3600, radio=True),
                ),
                             visible=f_settings("threading", "tray")
            ),
            pystray.MenuItem("Автозапуск", autostart_checkbox, lambda item: settings["autostart"],
                             visible=f_settings("autostart", "tray")),
            pystray.MenuItem("GitHub", github_page),
            pystray.MenuItem("Закрыть", quit_all),
        )
        sys_icon = pystray.Icon("WABA", PIL.Image.open("resources/settings_brightness.png"), title, tray_menu)
        sys_icon.run_detached()
    else:
        sys_icon = None

    if f_settings("threading", "thread"):
        print("-- starting timer thread")
        thread = threading.Thread(target=timer_thread, args=(sys_icon, ))
        thread.start()
    ...

    def hide_window(anyway: bool = False):
        if (settings["hiding_to_tray"] or anyway) and f_settings("tray", "main"):
            main_window.withdraw()
            if settings["im_hiding_message"] and settings["notifications"]:
                sys_icon.notify(
                    "Это можно выключить в настройках",
                    "Waba скрылась в трее"
                )
                settings["im_hiding_message"] = False
                save_settings()
        else:
            if msb.askyesno("Waba: закрыть приложение",
                            "Действительно хотите закрыть приложение?"):
                quit_all(sys_icon, window=main_window, do_destroy=True)
    ...
    main_window.protocol('WM_DELETE_WINDOW', hide_window)
    # noinspection PyUnboundLocalVariable
    if settings["hide_after_start"] and settings["features"]["tray"]:
        main_window.after(0, hide_window(True))

    main_window.iconbitmap("resources/logo2.ico")
    main_window.after(0, check)
    main_window.mainloop()


"""
    Starter
"""

if __name__ == "__main__":
    displays = sbc.list_monitors()
    if len(displays) == 0:
        debug_window = tk.Tk()
        debug_window.iconbitmap("logo2.ico")
        debug_window.withdraw()
        msb.showerror("Waba: Нет мониторов", "Нет данных о мониторах, прерываю запуск.\n"
                                             "\n"
                                             "Проверьте кабели, обновите драйвера и попробуйте снова"
                      )
        debug_window.quit()
        exit(0)
    settings["display"] = displays[0]
    del displays
    load_settings()
    load_version_file()
    do_start = True
    if settings["checking_for_updates"] and f_settings("autoupdate", "main"):
        import updater.manager
        if updater.manager.check_for_updates_with_ui(
                tag_or_sha=github_tag,
                # tag_or_sha="sus",
                edition=edition,
                user_files_path=waba_user_files_path):
            os.chdir(waba_user_files_path)
            os.system(f'"{Path(waba_user_files_path, """installer.exe""")}"')
            do_start = False
    if do_start:
        main()
