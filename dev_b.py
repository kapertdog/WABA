"""
    WABA (Windows automatic brightness adjustment) v.DEV_B
"""
import PIL.Image
import screen_brightness_control as sbc
import imageio as iio
import tkinter as tk
from tkinter import messagebox as msb
from statistics import mean
from pathlib import Path
import pystray
import yaml
import time

title = "Waba (v.Dev_B)"

# camera = iio.get_reader("<video0>")
# screenshot = camera.get_data(0)

# print("Размер скрина:", screenshot.shape)
# print("Среднее яркости:", int(screenshot.mean()))
# input()

"""
    Defaults
"""
# Default settings values
settings_version = 1
settings = {
    "settings_version": settings_version,
    "hide_after_start": False,
    "notifications": True,
    "device": "<video0>",
    "display": sbc.list_monitors()[0],
    "snapshot_delay": 0,
    "amount_of_shots": 1,
    "do_use_custom_method": False,
    "module_method": None,
}

"""
    Settings
"""


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
    return data


def load_settings(settings_path: Path = Path("settings.yaml")):
    global settings
    if settings_path.exists():
        with settings_path.open("r+") as s:
            data = yaml.safe_load(s)
        if data["settings_version"] != settings_version:
            try:
                settings = migrate_settings(data)
            except Exception as err:
                print("# Ошибка при миграции!!", err, "\n# Файл настроек будет перезаписан")
            with settings_path.open("w+") as s:
                yaml.dump(settings, s, default_flow_style=False)
        else:
            settings = data
    else:
        with settings_path.open("w+") as s:
            yaml.dump(settings, s, default_flow_style=False)
    return settings


def save_settings(settings_path: Path = Path("settings.yaml")):
    with settings_path.open("w+") as s:
        yaml.dump(settings, s, default_flow_style=False)


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
    return eval(func.format({"x": value}))


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
            f"{sbc.get_brightness(d)[0]}/100%",
            "Яркость обновлена",
        )
    return d, old_b, cam_b, m_b


"""
    Interface
"""


def get_interface():
    ...


"""
    Main things
"""


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

    def check():
        # обманка
        ...

    def submit(*_):
        # settings["hide_after_start"] =
        ...
        settings["hide_after_start"] = hiding_when_start_chbtn_var.get()
        settings["notifications"] = notifications_chbtn_var.get()
        settings["snapshot_delay"] = spinbox_shot_delay_var.get()
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
    hiding_when_start_chbtn_var = tk.BooleanVar()
    hiding_when_start_chbtn_var.set(settings["hide_after_start"])
    notifications_chbtn_var = tk.BooleanVar()
    notifications_chbtn_var.set(settings["notifications"])
    spinbox_shot_delay_var = tk.IntVar()
    spinbox_shot_delay_var.set(settings["snapshot_delay"])
    ...

    del check

    def check():
        changes = 0
        changes += int(hiding_when_start_chbtn_var.get() != settings["hide_after_start"])
        changes += int(notifications_chbtn_var.get() != settings["notifications"])
        changes += int(spinbox_shot_delay_var.get() != settings["snapshot_delay"])
        if changes == 0:
            submit_button.config(state="disabled")
            main_window.update()
        else:
            submit_button.config(state="active")
            main_window.update()
        ...

    ...
    hiding_when_start_chbtn = tk.Checkbutton(
        left_side_frame,
        text="Запускать свёрнутым",
        padx=10,
        anchor="w",
        command=check,
        variable=hiding_when_start_chbtn_var
    )
    hiding_when_start_chbtn.pack(fill=tk.X)

    notifications_chbtn = tk.Checkbutton(
        left_side_frame,
        text="Уведомления",
        padx=10,
        anchor="w",
        command=check,
        variable=notifications_chbtn_var
    )
    notifications_chbtn.pack(fill=tk.X)

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
    tk.Label(
        top_frame,
        text="Waba v.Dev_B (debug)   |   by @kapertdog with 💕",
        foreground="gray"
    ).pack(side=tk.BOTTOM)
    ...

    def upd_bright(icon = None, *_):
        answ = update_brightness(icon)
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
    left_side_frame.pack(side=tk.LEFT, fill=tk.BOTH)
    right_side_frame.pack(side=tk.LEFT, fill=tk.BOTH)
    top_frame.pack(fill=tk.X)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
    ...
    # main_window.geometry("400x250")
    main_window.geometry("310x125")
    main_window.resizable(width=False, height=False)
    ...

    def show_window():
        main_window.after(0, main_window.deiconify)

    def hide_window():
        main_window.withdraw()

    def quit_all(icon: pystray.Icon = None, *_):
        if icon is not None:
            icon.stop()
        main_window.deiconify()
        main_window.quit()
        # exit(0)
        ...

    ...
    tray_menu = pystray.Menu(
        pystray.MenuItem("Открыть настройки", show_window, default=True),
        pystray.MenuItem("Обновить яркость", upd_bright),
        pystray.MenuItem("Закрыть", quit_all),
    )
    sys_icon = pystray.Icon("WABA", PIL.Image.open("settings_brightness_light.png"), title, tray_menu)
    sys_icon.run_detached()
    ...
    main_window.protocol('WM_DELETE_WINDOW', hide_window)
    if settings["hide_after_start"]:
        main_window.after(0, hide_window())

    main_window.iconbitmap("logo.ico")
    main_window.mainloop()


"""
    Starter
"""

if __name__ == "__main__":
    if len(sbc.get_brightness()) == 0:
        debug_window = tk.Tk()
        debug_window.iconbitmap("logo.ico")
        debug_window.withdraw()
        msb.showerror("Waba: Нет мониторов", "Нет данных о мониторах, прерываю запуск.\n"
                                             "\n"
                                             "Проверьте кабели, обновите драйвера и попробуйте снова"
                      )
        debug_window.quit()
        exit(0)
    load_settings()
    main()
