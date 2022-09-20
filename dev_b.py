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
from languages import manager as lang
import pystray
import yaml
import time

short_app_name = "Waba"  # Подставляется везде в интерфейсе
full_app_name = "Windows Automatic\nBrightness Adjustment"  # Вставляется в About

titled_name = short_app_name + ": "

title = short_app_name + " (v.Dev_B)"
version = "0.3.2.0"
github_tag = "dev_b_pre-10"
edition = "venv"  # Всего 3 издания: "venv", "folder" и "exe"
branch = "master"  # Пока планирую 2 ветки: "master" и "only-tray"

# camera = iio.get_reader("<video0>")
# screenshot = camera.get_data(0)

# print("Размер скрина:", screenshot.shape)
# print("Среднее яркости:", int(screenshot.mean()))
# input()

"""
    Defaults
"""
# Default settings values
settings_version = 8  # Надо не забыть обновить
settings_path = Path(os.getenv("APPDATA", ""), short_app_name.lower(), "settings.yaml")
waba_user_files_path = Path(os.getenv("APPDATA", ""), short_app_name.lower())
settings = {
    "_venv_dir": os.getcwd(),  # Нужно, но только для апдейтов
    "settings_version": settings_version,
    "theme": "dark",
    "language": None,
    "autostart": False,
    "checking_for_updates": edition != "venv",
    # features
    "features": {
        # Обновляются только после перезапуска!!
        "autoupdate": True,
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
    "devices": {},
    "displays": {},
    # snapshot
    "cycle_timer": None,
    "timer_tick_delay": 1,
    "snapshot_delay": 1,
    "amount_of_shots": 1,
    "load_settings_every_update": False,
    # math
    "pre-save_values": False,  # Пока не работает
    "sort_keyframes": True,
    "merge_nearest_keyframes": True,
    "keyframes_limit": 15
}

cashed_dict_of_devices = dict()
checked_cams = dict()

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


def f_settings(keyword: str, element: str = "main") -> str:
    match element:
        case "tkinter":
            if settings["features"][keyword]:
                return "normal"
            else:
                return "disabled"
        case _:
            return settings["features"][keyword]
    # return features_values_of_switches[keyword][settings["features"][keyword]][element]


def migrate_settings(data):
    migrate_sect = lang.Section("main.json", "migrate")

    def check(old, new):
        ret = dict()
        for name in new:
            if name in old:
                # Если элемент есть в старой версии
                if type(new[name]) == dict and name not in ("devices", "displays"):
                    # Но это словарь
                    ret[name] = check(old[name], new[name])
                else:
                    ret[name] = old[name]
            else:
                # Если элемент вообще отсутствует
                print(f"# {migrate_sect.get('missing_element').format(name)}")
                ret[name] = new[name]
        return ret

    global settings
    print(f"-=- {migrate_sect.get('migration_required')} -=-")
    data = check(data, settings)

    match data["settings_version"]:
        case 7:
            data = reset_settings(data, "displays_calibration", "sensors_calibration")
            # msb.showwarning(migrate_sect.get("title"),
            #                 migrate_sect.get("reset", "warn_top_text")
            #                 + "\n\n"
            #                 + migrate_sect.get("reset", "calibration"))
            # data["devices"] = {}

    data["settings_version"] = settings_version
    print(f"-=-  {migrate_sect.get('successful')}  -=-")
    return data


def reset_settings(data, *args):
    migrate_sect = lang.Section("main.json", "migrate")
    warn_bottom_text_list = []
    for i in args:
        match i:
            case "all":
                data = settings
            case "displays_calibration":
                data["displays"] = {}
            case "sensors_calibration":
                data["devices"] = {}
        warn_bottom_text_list.append(migrate_sect.get("reset", i))
    msb.showwarning(titled_name + migrate_sect.get("title"),
                    migrate_sect.get("reset", "warn_top_text") + "\n\n" + "\n".join(warn_bottom_text_list))
    return data


def save_settings(path: Path = settings_path):
    with path.open("w+") as s:
        yaml.dump(settings, s, default_flow_style=False)


def load_settings(path: Path = settings_path, do_migrate=True, do_update=True):
    # Path(os.getenv("APPDATA"), "Microsoft", "Window", "Start Menu", "Programs", "Startup")
    global settings
    if path.exists():
        with path.open("r+") as s:
            data = yaml.safe_load(s)
        if data["settings_version"] != settings_version and do_migrate:
            if data["language"]:
                lang.load(data["language"], printing=False)
            try:
                settings = migrate_settings(data)
            except Exception as err:
                migrate_sect = lang.Section("main.json", "migrate")
                print("# " + migrate_sect.get("fatal_error"), err,
                      "\n# " + migrate_sect.get("fatal_error_message"))
                msb.showerror(titled_name + migrate_sect.get("title"), f"{err}\n" +
                              migrate_sect.get("fatal_error_message"))
            save_settings(path)
        else:
            settings = data
    elif do_update:
        if not path.parent.exists():
            path.parent.mkdir()
        save_settings(path)
    if do_update and not Path(settings["_venv_dir"]).exists():
        settings["_venv_dir"] = str(Path.cwd())
        save_settings(path)
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
    Pre-matched values
"""
# Как-нибудь стоит сделать возможность хранить эти значения не только в оперативке

displays_values = dict()
devices_values = dict()


def sort_keyframes(keyframes: tuple | list) -> tuple:
    return tuple(sorted(keyframes, key=lambda x: x[0]))


def generate_values(keyframes: tuple = tuple(), start_with: tuple = (0, 0), end_with: tuple = (255, 255)):
    c_result = dict()
    if settings["sort_keyframes"]:
        keyframes = sort_keyframes(keyframes)
    keyframes_list = [start_with, *keyframes, end_with]
    # print(keyframes_list)
    for i in range(len(keyframes_list) - 1):
        from_x = keyframes_list[i][0]
        from_y = keyframes_list[i][1]
        to_x = keyframes_list[i+1][0]
        to_y = keyframes_list[i+1][1]
        steps = max(abs(from_x - to_x), abs(from_y - to_y))
        # print(i, from_x, from_y, to_x, to_y, steps)
        if steps != 0:
            x_step = (- 1 * (from_x - to_x)) / steps
            y_step = (- 1 * (from_y - to_y)) / steps

            cashed_x = float(from_x)
            cashed_y = float(from_y)
            for n in range(steps):
                if not str(int(cashed_x)) in c_result:
                    c_result[str(int(cashed_x))] = list()
                c_result[str(int(cashed_x))].append(int(cashed_y))
                cashed_x += x_step
                cashed_y += y_step
    c_result[str(end_with[0])] = end_with[1]
    g_result = list()
    for n in c_result:
        if type(c_result[n]) is list:
            g_result.insert(int(n), int(mean(c_result[n])))
            # g_result[n] = mean(c_result[n])
        else:
            g_result.insert(int(n), int(c_result[n]))
    return g_result


def generate_display_values(display: str):
    if display in settings["displays"]:
        keyframes = tuple(settings["displays"][display]["keyframes"])
    else:
        keyframes = ()
    global displays_values
    displays_values[display] = generate_values(keyframes, (0, 0), (255, 100))


def generate_device_values(device: str):
    if device in settings["devices"]:
        keyframes = tuple(settings["devices"][device]["keyframes"])
    else:
        keyframes = ()
    global devices_values
    devices_values[device] = generate_values(keyframes, (0, 0), (255, 255))


# noinspection PyUnresolvedReferences
def add_device_keyframe(device: str, keyframe: (int, int)):
    global settings
    settings["devices"][device]["keyframes"].append(keyframe)
    save_settings()
    generate_device_values(device)
    ...


# noinspection PyUnresolvedReferences
def add_display_keyframe(display: str, keyframe: (int, int)):
    global settings
    if display not in settings["displays"]:
        settings["displays"][display] = {
            "keyframes": []
        }
    settings["displays"][display]["keyframes"].append(list(keyframe))
    save_settings()
    generate_display_values(display)
    ...


def reset_calibration(icon: pystray.Icon = None):
    cbk_sect = lang.Section("main.json", "brightness_update", "clear_displays_keyframes")
    print(cbk_sect.get("resetting_keyframes"))
    cashed_displays_dict = dict()
    for i in settings["displays"]:
        cashed_displays_dict[i] = settings["displays"][i]
    for display in cashed_displays_dict:
        print(f'  "{display}", '
              f'{cbk_sect.get("elements").format(len(cashed_displays_dict[display]["keyframes"]))} ...')
        settings["displays"].pop(display)
        generate_display_values(display)
    print(cbk_sect.get("saving_settings") + "\n")
    save_settings()
    if icon and settings["notifications"]:
        icon.notify(
            cbk_sect.get("default_values_restored"),
            cbk_sect.get("reset"))


def match_displays_brightness_at_state(icon: pystray.Icon = None):
    mdb_sect = lang.Section("main.json", "brightness_update", "match_brightness")
    print(f"-=- {time.ctime()} -=-")
    print(mdb_sect.get("correlation_of_brightness_values"))
    for device in settings["devices"]:
        print(mdb_sect.get("device"), device)
        device_b = get_brightness(device, settings["snapshot_delay"], settings["amount_of_shots"])
        if device not in devices_values:
            generate_device_values(device)
        device_m_b = devices_values[device][device_b]
        print(f"{device_b}/255 ~ {device_m_b}/255")
        for display in settings["devices"][device]["displays"]:
            print(f"  {mdb_sect.get('display')} {display}")
            display_b = sbc.get_brightness(display)[0]
            print(f"    {mdb_sect.get('brightness_now')} {display_b}")
            add_display_keyframe(display, (device_m_b, display_b))
            print(f"    ~ {mdb_sect.get('values_are_prepared')}")
    if icon and settings["notifications"]:
        icon.notify(mdb_sect.get('calibrated'), mdb_sect.get('match_completed'))
    print()


"""
    Functions
"""


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
        sect = lang.Section("main.json", "brightness_update", "errors")
        msb.showerror(
            titled_name + sect.get("incorrect_settings_title"),
            sect.get("incorrect_settings").format(err))
        raise ValueError(err)


def calc_custom(value: int, func: str):
    if settings["features"]["safe_math_mode"]:
        return int(eval(func.format(value), {"value": value, "x": value, "open_web_page": open_web_page}))
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


def update_brightness(icon: pystray.Icon = None, *_):
    sect = lang.Section("main.json", "brightness_update", "update_brightness")
    print(f"-=- {time.ctime()} -=-")
    if settings["load_settings_every_update"]:
        load_settings()
    for device in settings["devices"]:
        print(sect.get("device") + device)
        disp = settings["devices"][device]["displays"]
        reply = dict()
        cam_b = get_brightness(device, settings["snapshot_delay"], settings["amount_of_shots"])
        if device not in devices_values:
            generate_device_values(device)
            print("~", sect.get("values_for_sensor_is_calculated"))
            # print(devices_values[device])
        m_cam_b = devices_values[device][cam_b]
        print(sect.get("brightness_from_sensor"), f"{cam_b}/255 -> {m_cam_b}")
        for display in disp:
            print("*", sect.get("display"))
            if display not in displays_values:
                generate_display_values(display)
                print("  ~", sect.get("values_for_display_is_calculated"))
                print("  ~ Просчитаны значения для этого дисплея")
                # print(displays_values[display])
            old_b = sbc.get_brightness(display)[0]
            print(f"  *", sect.get("brightness_before"), old_b)
            m_b = displays_values[display][m_cam_b]
            # method = settings["devices"][device]["method"]
            # if method and method != "":
            #     m_b = calc_custom(cam_b, method)
            # else:
            #     m_b = calc_value_v1(cam_b)
            print(f"  *", sect.get("brightness_after"), m_b)
            print()
            sbc.set_brightness(m_b, display)
            reply[display] = {
                "old_b": old_b,
                "m_b": m_b
            }
        # reply_text = f"Камера {device}:\n" \
        #              f"  {cam_b}/255 -> {m_cam_b}"
        # reply_text = f"{device}: {cam_b}/255 ~ {m_cam_b}"
        reply_text = ""
        for display_name in reply:
            reply_text += f"{display_name.split(' ')[0]}:" \
                          f" {reply[display_name]['old_b']}% -> {reply[display_name]['m_b']}%\n"
        if icon is not None and settings["notifications"]:
            icon.notify(
                reply_text,
                sect.get("brightness_updated"),
            )
    # return d, old_b, cam_b, m_b


thread_alive = True


def timer_thread(_):
    last_time = 0
    while thread_alive:
        if settings["cycle_timer"]:
            if int(time.monotonic()) - last_time > settings["cycle_timer"]:
                try:
                    update_brightness()
                except Exception as err:
                    msb.showerror(titled_name + lang.get("main.json", "default_error", "title"),
                                  f"{err}")
                last_time = int(time.monotonic())
        time.sleep(settings["timer_tick_delay"])


downloader_busy = False


def download_thread(icon: pystray.Icon, e, v, do_at_end=None):
    sect = lang.Section("main.json", "download_thread")
    import updater.manager
    global downloader_busy
    downloader_busy = True
    if icon and settings["notifications"]:
        icon.notify(sect.get("you_can_use_app"),
                    sect.get("update_is_downloading"))

    try:
        updater.manager.download_update(e, v)
    except Exception as err:
        msb.showerror(titled_name + sect.get("error_title"), f"{err}")
        downloader_busy = False
        return False

    if icon and settings["notifications"]:
        icon.notify(sect.get("go_to_extra"),
                    sect.get("downloaded"))
    if do_at_end:
        do_at_end()
    downloader_busy = False
    return True


def check_device_exist(device: str = "<video0>"):
    try:
        test_reader = iio.get_reader(device)
        test_reader.close()
        del test_reader
        return True
    except IndexError:
        return False


def get_free_displays(dis: list, devices: dict) -> list:
    free_displays = dis.copy()
    for display in dis:
        for device in devices:
            if display in devices[device]["displays"]:
                free_displays.remove(display)
    return free_displays


"""
    Interface
"""


def get_interface():
    ...


"""
    Main things
"""


def open_web_page(url: str = r"https://youtu.be/dQw4w9WgXcQ"):
    __import__("webbrowser").open_new_tab(url)


def open_web(url: str = r"https://youtu.be/hMCAF8tZ7ZE"):
    import webbrowser
    webbrowser.open_new_tab(url)


def github_page():
    # with open("about.txt", "r+", encoding="UTF-8") as f:
    #     about_txt = f.read()
    # msb.showinfo(
    #     "Waba: about",
    #     about_txt
    # )
    open_web_page(r"https://github.com/kapertdog/WABA")


def about(show: bool = True):
    about_txt = lang.get("main.json", "pages", "about")
    if show:
        msb.showinfo(
            titled_name + about_txt.get("title"),
            about_txt.get("about").format(full_app_name),
        )
    return about_txt
    # __import__("webbrowser").open_new_tab(r"https://github.com/kapertdog/WABA")


def main():
    main_sect = lang.Section("main.json", "main")
    global settings
    main_window = tk.Tk()
    main_window.title(titled_name + main_sect.get("title"))
    ...  # Подготовка переменных

    def submit(*_):
        # settings["hide_after_start"] =
        ...
        if settings["autostart"] != autostart_chbtn_var.get():
            settings["autostart"] = autostart(autostart_chbtn_var.get())
        settings["devices"] = {}
        for element in cashed_dict_of_devices:
            # noinspection PyUnresolvedReferences
            settings["devices"][element] = cashed_dict_of_devices[element].copy()
        settings["checking_for_updates"] = checking_for_updates_chbtn_var.get()
        settings["hiding_to_tray"] = hiding_to_tray_chbtn_var.get()
        settings["hide_after_start"] = hiding_when_start_chbtn_var.get()
        settings["notifications"] = notifications_chbtn_var.get()
        settings["cycle_timer"] = timer_values_of_names[update_rate_lst_var.get()]
        settings["snapshot_delay"] = spinbox_shot_delay_var.get()
        save_settings()
        check()

    hiding_to_tray_chbtn_var = tk.BooleanVar()
    hiding_when_start_chbtn_var = tk.BooleanVar()
    notifications_chbtn_var = tk.BooleanVar()
    autostart_chbtn_var = tk.BooleanVar()
    checking_for_updates_chbtn_var = tk.BooleanVar()
    update_rate_lst_var = tk.StringVar()
    spinbox_shot_delay_var = tk.IntVar()

    turned_cam_chbtn_var = tk.BooleanVar()
    displays_selected_device_var = tk.StringVar()
    displays_is_its_zero_page = tk.BooleanVar()
    displays_is_device_exist_var = tk.BooleanVar()

    def update():
        hiding_to_tray_chbtn_var.set(settings["hiding_to_tray"])
        hiding_when_start_chbtn_var.set(settings["hide_after_start"])
        notifications_chbtn_var.set(settings["notifications"])
        autostart_chbtn_var.set(settings["autostart"])
        checking_for_updates_chbtn_var.set(settings["checking_for_updates"])
        update_rate_lst_var.set(timer_names_of_values[settings["cycle_timer"]])
        spinbox_shot_delay_var.set(settings["snapshot_delay"])

        displays_selected_device_var.set("<video0>")
    update()

    def displays_update_lists(free_displays_list, selected_displays_list):
        if len(left_list_box.get(0, tk.END)) > 0:
            left_list_box.delete(0, tk.END)
        if len(right_list_box.get(0, tk.END)) > 0:
            right_list_box.delete(0, tk.END)
        for i in free_displays_list:
            left_list_box.insert(tk.END, i)
        for i in selected_displays_list:
            right_list_box.insert(tk.END, i)

    def displays_page_update(do_check_cam=True):
        if displays_selected_device_var.get() in checked_cams:
            displays_is_device_exist_var.set(checked_cams[displays_selected_device_var.get()])
        elif do_check_cam:
            displays_is_device_exist_var.set(check_device_exist(displays_selected_device_var.get()))
            checked_cams[displays_selected_device_var.get()] = displays_is_device_exist_var.get()
        else:
            displays_is_device_exist_var.set(True)
            checked_cams[displays_selected_device_var.get()] = displays_is_device_exist_var.get()
        displays_is_its_zero_page.set(displays_selected_device_var.get()[-2] == "0")
        if displays_is_its_zero_page.get():
            previous_cam_button.config(state="disabled")
        else:
            previous_cam_button.config(state="normal")
        if displays_is_device_exist_var.get():
            next_cam_button.config(state="normal")
            turned_cam_chbtn.config(state="normal")
        else:
            next_cam_button.config(state="disabled")
            turned_cam_chbtn.config(state="disabled")
        turned_cam_chbtn_var.set(displays_selected_device_var.get() in cashed_dict_of_devices)
        turned_cam_chbtn.config(text=f"Камера {displays_selected_device_var.get()}")
        update_lists()
        check()

    def update_lists():
        if turned_cam_chbtn_var.get():
            # noinspection PyUnresolvedReferences
            displays_update_lists(get_free_displays(sbc.list_monitors(), cashed_dict_of_devices),
                                  cashed_dict_of_devices[displays_selected_device_var.get()]["displays"])
        else:
            displays_update_lists(get_free_displays(sbc.list_monitors(), cashed_dict_of_devices), [])
        right_list_box.update()
        left_list_box.update()

    def check():
        changes = 0
        try:
            changes += int(hiding_to_tray_chbtn_var.get() != settings["hiding_to_tray"])
            changes += int(hiding_when_start_chbtn_var.get() != settings["hide_after_start"])
            changes += int(notifications_chbtn_var.get() != settings["notifications"])
            changes += int(autostart_chbtn_var.get() != settings["autostart"])
            changes += int(checking_for_updates_chbtn_var.get() != settings["checking_for_updates"])
            changes += int(timer_values_of_names[update_rate_lst_var.get()] != settings["cycle_timer"])
            changes += int(spinbox_shot_delay_var.get() != settings["snapshot_delay"])
            changes += int(not settings["devices"] == cashed_dict_of_devices)
        except Exception as err:
            msb.showerror(titled_name + main_sect.get("settings_checking_error"),
                          f"{err}")
        if changes == 0:
            submit_button.config(state="disabled")
            main_window.update()
        else:
            submit_button.config(state="active")
            main_window.update()
        check_two()
    ...

    def install_update(icon):
        match edition:
            case "venv" | "folder":
                os.chdir(Path(waba_user_files_path, "update"))
                if os.access(settings["_venv_dir"], os.W_OK & os.R_OK):
                    os.system("start installer.exe")
                else:
                    os.system(f'''powershell -Command "Start-Process 'installer.exe' -Verb runAs"''')
            case "exe":
                os.chdir(Path(waba_user_files_path, "update"))
                os.system("start install-waba.exe")
        quit_all(icon)

    ...  # Распределение главных фреймов
    tab_control = ttk.Notebook(main_window)  # По-сути верхний фрейм
    bottom_frame = tk.Frame(main_window, padx=10, pady=10, background="#ABB2B9")
    ...  # Страница главных настроек
    main_page = ttk.Frame(tab_control)
    mp_sect = lang.Section("main.json", "pages", "main")
    ...  # Левый и правый фреймы
    left_side_frame = tk.Frame(main_page)
    right_side_frame = tk.Frame(main_page)
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
        text=mp_sect.get("hiding_to_tray"),
        padx=10,
        anchor="w",
        command=check,
        state=f_settings("tray", "tkinter"),
        variable=hiding_to_tray_chbtn_var
    )
    hiding_to_tray_chbtn.pack(fill=tk.X)

    hiding_when_start_chbtn = tk.Checkbutton(
        left_side_frame,
        text=mp_sect.get("hiding_when_start"),
        padx=10,
        anchor="w",
        command=check,
        state=f_settings("tray", "tkinter"),
        variable=hiding_when_start_chbtn_var
    )
    hiding_when_start_chbtn.pack(fill=tk.X)

    notifications_chbtn = tk.Checkbutton(
        left_side_frame,
        text=mp_sect.get("notifications"),
        padx=10,
        anchor="w",
        command=check,
        state=f_settings("notifications", "tkinter"),
        variable=notifications_chbtn_var
    )
    notifications_chbtn.pack(fill=tk.X)

    autostart_chbtn = tk.Checkbutton(
        left_side_frame,
        text=mp_sect.get("starting_with_system"),
        padx=10,
        anchor="w",
        command=check,
        state=f_settings("autostart", "tkinter"),
        variable=autostart_chbtn_var
    )
    autostart_chbtn.pack(fill=tk.X)

    checking_for_updates_chbtn = tk.Checkbutton(
        left_side_frame,
        text=mp_sect.get("look_for_updates"),
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
        text=mp_sect.get("brightness_update_rate"),
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
    update_rate_lst.pack(fill=tk.X, padx=4)

    lbl_shot_delay = tk.Label(
        right_side_frame,
        text="Задержка кадра: ",
        padx=10,
        anchor="w"
    )
    lbl_shot_delay.pack(fill=tk.X)

    spinbox_shot_delay = ttk.Spinbox(
        right_side_frame,
        from_=0,
        to=100,
        command=check,
        textvariable=spinbox_shot_delay_var
    )
    spinbox_shot_delay.pack(fill=tk.X, padx=4)

    ...
    ...
    tk.Label(
        main_page,
        text=f"v.Dev_B ({version})   |   made with 💕",
        foreground="gray"
    ).pack(side=tk.BOTTOM)
    ...
    ...  # Упаковка главных фреймов
    left_side_frame.pack(side=tk.LEFT, fill=tk.BOTH)
    right_side_frame.pack(side=tk.LEFT, fill=tk.BOTH)
    ...  # Добавляем страничку
    tab_control.add(main_page, text=mp_sect.get("title"))

    ...  # Страница соотношения камер и мониторов
    displays_page = ttk.Frame(tab_control)
    dp_sect = lang.Section("main.json", "pages", "displays")
    ...  # И вновь прописываю стороны
    displays_top_line_frame = tk.Frame(displays_page, bg="#D8D8D8")
    displays_lists_frame = tk.Frame(displays_page)
    displays_lists_left_frame = tk.Frame(displays_lists_frame)
    displays_lists_right_frame = tk.Frame(displays_lists_frame)
    displays_lists_center_frame = tk.Frame(displays_lists_frame)
    displays_downside_frame = tk.Frame(displays_page)
    ...  # Прописываем элементы
    # Literal["raised", "sunken", "flat", "ridge", "solid", "groove"]

    def previous_cam_func():
        if displays_selected_device_var.get()[:-2] != "0":
            displays_selected_device_var.set(
                f"<video{int(displays_selected_device_var.get()[-2]) - 1}>")
            displays_page_update()
    previous_cam_button = tk.Button(
        displays_top_line_frame,
        text="<",
        relief="flat",
        command=previous_cam_func,
        state="disabled"
    )

    def next_cam_func():
        displays_selected_device_var.set(
            f"<video{int(displays_selected_device_var.get()[-2]) + 1}>")
        displays_page_update()
    previous_cam_button.pack(side=tk.LEFT, padx=5, pady=5)
    next_cam_button = tk.Button(
        displays_top_line_frame,
        text=">",
        relief="flat",
        command=next_cam_func
    )
    next_cam_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def turned_cam_func():
        global cashed_dict_of_devices
        if turned_cam_chbtn_var.get():
            cashed_dict_of_devices[displays_selected_device_var.get()] = \
                {
                    "displays": [],
                    "keyframes": [],
                }
        else:
            copy_of_dict = dict()
            for item in cashed_dict_of_devices:
                copy_of_dict[item] = cashed_dict_of_devices[item].copy()
            cashed_dict_of_devices = {}
            for item in copy_of_dict:
                if item != displays_selected_device_var.get():
                    cashed_dict_of_devices[item] = copy_of_dict[item].copy()
        update_lists()
        check()
    turned_cam_chbtn = tk.Checkbutton(
        displays_top_line_frame,
        text=f"{dp_sect.get('current_sensor')} <video0>",
        command=turned_cam_func,
        variable=turned_cam_chbtn_var,
    )
    turned_cam_chbtn.pack(anchor="center", side=tk.TOP, padx=5, pady=5)
    ...
    left_list_box_title = tk.Label(
        displays_lists_left_frame,
        text=dp_sect.get("free")
    )
    left_list_box_title.pack(fill=tk.X, anchor="center")
    left_list_box_scrllbar = ttk.Scrollbar(
        displays_lists_left_frame,
    )
    left_list_box_scrllbar.pack(fill=tk.Y, side=tk.RIGHT)
    left_list_box = tk.Listbox(
        displays_lists_left_frame,
        height=6,
        width=18,
        yscrollcommand=left_list_box_scrllbar.set,
        selectmode=tk.EXTENDED,
    )
    left_list_box.pack(fill=tk.X, side=tk.LEFT)

    left_list_box_scrllbar.config(command=left_list_box.yview)

    displays_lists_left_frame.pack(side=tk.LEFT)
    ...
    right_list_box_title = tk.Label(
        displays_lists_right_frame,
        text=dp_sect.get("selected")
    )
    right_list_box_title.pack()
    right_list_box_scrllbar = ttk.Scrollbar(
        displays_lists_right_frame,
    )
    right_list_box_scrllbar.pack(fill=tk.Y, side=tk.RIGHT)
    right_list_box = tk.Listbox(
        displays_lists_right_frame,
        height=6,
        width=18,
        yscrollcommand=right_list_box_scrllbar.set,
        selectmode=tk.EXTENDED,
    )
    right_list_box.pack(fill=tk.X, side=tk.LEFT)

    right_list_box_scrllbar.config(command=right_list_box.yview)

    displays_lists_right_frame.pack(side=tk.RIGHT)

    def grab_all():
        # noinspection PyUnresolvedReferences
        cashed_dict_of_devices[displays_selected_device_var.get()]["displays"] = \
                [*cashed_dict_of_devices[
                    displays_selected_device_var.get()]["displays"].copy(),
                 *get_free_displays(sbc.list_monitors(), cashed_dict_of_devices)]
        update_lists()
        check()
    grab_all_btn = tk.Button(
        displays_lists_center_frame,
        text=">>",
        width=2,
        relief="flat",
        command=grab_all
    )
    grab_all_btn.pack(anchor="center", padx=5)

    def grab_selected():
        for i in list(left_list_box.curselection()):
            cashed_dict_of_devices[displays_selected_device_var.get()]["displays"] = \
                    [*cashed_dict_of_devices[
                        displays_selected_device_var.get()]["displays"].copy(),
                     left_list_box.get(i)]
        update_lists()
        check()
    grab_selected_btn = tk.Button(
        displays_lists_center_frame,
        text="->",
        width=2,
        command=grab_selected
    )
    grab_selected_btn.pack(anchor="center", padx=5)

    def store_selected():
        copy_of_list = [*cashed_dict_of_devices[
            displays_selected_device_var.get()]["displays"].copy()]
        for i in list(right_list_box.curselection()):
            copy_of_list.remove(right_list_box.get(i))
        cashed_dict_of_devices[displays_selected_device_var.get()]["displays"] = \
            [*copy_of_list.copy()]
        update_lists()
        check()
    store_selected_btn = tk.Button(
        displays_lists_center_frame,
        text="<-",
        width=2,
        command=store_selected
    )
    store_selected_btn.pack(anchor="center", padx=5)

    def store_all():
        # noinspection PyUnresolvedReferences
        cashed_dict_of_devices[displays_selected_device_var.get()]["displays"] = list()
        update_lists()
        check()
    store_all_btn = tk.Button(
        displays_lists_center_frame,
        text="<<",
        width=2,
        relief="flat",
        command=store_all
    )
    store_all_btn.pack(anchor="center", padx=5)

    displays_lists_center_frame.pack(fill=tk.Y, anchor="center", pady=5)

    method_entry_lbl = tk.Label(
        displays_downside_frame,
        text=dp_sect.get("function"),
        state="disabled",
    )
    method_entry_lbl.pack(side=tk.LEFT)
    method_entry = ttk.Entry(
        displays_downside_frame,
        state="disabled",
    )
    method_entry.pack(fill=tk.X, side=tk.LEFT)
    get_photo_btn = tk.Button(
        displays_downside_frame,
        text=dp_sect.get("take_a_photo"),
        state="disabled",
    )
    get_photo_btn.pack(side=tk.RIGHT)
    ...  # Пакуем глобальных шизоидов
    displays_top_line_frame.pack(fill=tk.X, side=tk.TOP)
    displays_lists_frame.pack()
    displays_downside_frame.pack(fill=tk.BOTH, side=tk.BOTTOM, padx=5, pady=5)
    ...  # Добавляем
    tab_control.add(displays_page, text=dp_sect.get("title"))

    ...  # Страница калибровки
    calibration_page = ttk.Frame(tab_control)
    cp_sect = lang.Section("main.json", "pages", "calibration")
    ...  # Прописываем элементы
    ...  # Добавляем
    tab_control.add(calibration_page, text=cp_sect.get("title"), state="disabled")

    ...  # Страница дополнительных настроек
    settings_page = ttk.Frame(tab_control)
    sp_sect = lang.Section("main.json", "pages", "extra")
    ...  # Прописываем элементы

    def down_upd():
        if not downloader_busy:
            v = 0
            if edition == "venv":
                v = branch

            def d_a_end():
                download_update_button.config(state="normal")
                install_update_button.config(state="normal")
            d_thread = threading.Thread(target=download_thread,
                                        args=(sys_icon, edition, v, d_a_end))
            d_thread.start()
            download_update_button.config(state="disabled")
            install_update_button.config(state="disabled")
        else:
            msb.showerror(titled_name + lang.get("main.json", "download_thread", "title"),
                          lang.get("main.json", "download_thread", "already_downloading"))
    download_update_button = tk.Button(
        settings_page,
        text="Скачать",
        command=down_upd
    )
    download_update_button.pack()

    def inst_upd():
        install_update(sys_icon)
    install_update_button = tk.Button(
        settings_page,
        text="Установить",
        command=inst_upd,
        state="disabled"
    )
    install_update_button.pack()
    ...  # Добавляем
    tab_control.add(settings_page, text=sp_sect.get("title"), state="disabled")

    ...  # Страница About
    about_page = ttk.Frame(tab_control)
    ap_sect = lang.Section("main.json", "pages", "about")
    ...  # Вновь делю на левую и правую части
    about_left_side_frame = tk.Frame(about_page)
    about_right_side_frame = tk.Frame(about_page)
    ...  # Прописываем элементы
    waba_logo_image = tk.PhotoImage(file="resources/logo2.png")
    waba_logo_lbl = tk.Label(
        about_left_side_frame,
        image=waba_logo_image,
    )
    waba_logo_lbl.pack()

    sub_waba_lbl = tk.Label(
        about_left_side_frame,
        text=ap_sect.get("links")
    )
    sub_waba_lbl.pack()

    web_buttons_frame = tk.Frame(about_left_side_frame)

    # tk.Label(about_left_side_frame, text="WABA").pack(fill=tk.X)
    github_logo_image = tk.PhotoImage(file="resources/github_logo.png")
    about_github_button = tk.Button(
        web_buttons_frame,
        image=github_logo_image,
        command=github_page
    )
    about_github_button.pack(side=tk.LEFT, padx=1)

    def linktree_page():
        open_web_page(r"https://linktr.ee/kapertdog")
    linktree_logo_image = tk.PhotoImage(file="resources/linktree_logo.png")
    about_linktree_button = tk.Button(
        web_buttons_frame,
        image=linktree_logo_image,
        command=linktree_page
    )
    about_linktree_button.pack(side=tk.LEFT, padx=1)

    def youtube_page():
        open_web_page(r"https://www.youtube.com/c/kprtdg")
    youtube_logo_image = tk.PhotoImage(file="resources/youtube_logo.png")
    about_youtube_button = tk.Button(
        web_buttons_frame,
        image=youtube_logo_image,
        command=youtube_page
    )
    about_youtube_button.pack(side=tk.LEFT, padx=1)

    ...
    about_lbl = tk.Label(
        about_right_side_frame,
        text=about(False),
        anchor="center"
    )
    about_lbl.pack()
    ...  # Пакуем шизоидов
    about_left_side_frame.pack(side=tk.LEFT, fill=tk.Y)
    about_right_side_frame.pack(fill=tk.BOTH)
    web_buttons_frame.pack()
    ...  # Добавляем
    tab_control.add(about_page, text=ap_sect("title"))

    ...  # Теперь Нижний фрейм

    def upd_bright(icon=None, *_):
        if not icon:
            icon = sys_icon
        # subprocess.run(update_brightness, input=icon)
        try:
            update_brightness(icon)
        except Exception as err:
            msb.showerror(titled_name +
                          lang.get("main.json", "default_error", "title"), f"{err}")
            return

    check_button = tk.Button(
        bottom_frame,
        command=upd_bright,
        text=mp_sect.get("update"),
        anchor="center",
        relief=tk.GROOVE,
    )
    check_button.pack(side=tk.LEFT)

    submit_button = tk.Button(
        bottom_frame,
        command=submit,
        text=mp_sect.get("apply"),
        state="disabled",
        relief=tk.GROOVE,
    )
    submit_button.pack(side=tk.RIGHT)
    ...
    displays_page_elements_list = [
        left_list_box_title,
        right_list_box_title, grab_all_btn, grab_selected_btn,
        store_all_btn, store_selected_btn,
    ]

    def check_two():
        if turned_cam_chbtn_var.get():
            for i in displays_page_elements_list:
                i.config(state="normal")
        else:
            for i in displays_page_elements_list:
                i.config(state="disabled")
        ...
    ...  # Упаковываем все странички
    tab_control.pack(expand=1, fill='both', padx=5, pady=5)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

    ...  # А теперь трей и всякое что нужно сделать после

    def show_window():
        main_window.after(0, main_window.deiconify)
        check()

    def quit_all(icon: pystray.Icon = None, *_, window: tk.Tk = main_window):
        def q():
            if icon is not None:
                icon.stop()
            if f_settings("threading", "thread"):
                global thread_alive
                thread_alive = False
                thread.join()

        # import loading_screen
        # loading_screen.processing(q, "Waba: Завершение работы", "Выходим...")
        # print("-- after processing")
        window.withdraw()
        q()
        window.deiconify()
        print("-- try to quit")
        window.quit()
        print("-- after try to quit")

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

    tray_sect = lang.Section("main.json", "tray")

    def keep_state_in_mind(icon):
        if msb.askyesno(titled_name + tray_sect.get("ask_do_calibration_title"),
                        tray_sect.get("ask_do_calibration")):
            match_displays_brightness_at_state(icon)

    def reset_keyvalues(icon):
        if msb.askyesno(titled_name + tray_sect.get("ask_reset_calibration_title"),
                        tray_sect.get("ask_reset_calibration")):
            reset_calibration(icon)
    ...
    if f_settings("tray", "main"):
        tray_menu = pystray.Menu(
            pystray.MenuItem(tray_sect.get("open_settings"), show_window, default=True),
            pystray.MenuItem(tray_sect.get("update_brightness"), upd_bright, default=False),
            pystray.MenuItem(tray_sect.get("calibration", "name"), pystray.Menu(
                pystray.MenuItem(tray_sect.get("calibration", "keep_in_mind"),
                                 keep_state_in_mind, default=False),
                pystray.MenuItem(tray_sect.get("calibration", "reset"), reset_keyvalues, default=False),
            ), ),
            pystray.MenuItem(tray_sect.get("update_every"), pystray.Menu(
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
                             enabled=f_settings("threading", "tray")
            ),
            pystray.MenuItem(tray_sect.get("autostart"), autostart_checkbox, lambda item: settings["autostart"],
                             enabled=f_settings("autostart", "tray")),
            pystray.MenuItem("GitHub", github_page),
            pystray.MenuItem(tray_sect.get("exit"), quit_all),
        )
        sys_icon = pystray.Icon("Waba", PIL.Image.open("resources/settings_brightness.png"),
                                title, tray_menu)
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
                    tray_sect.get("hid_in_tray"),
                    tray_sect.get("hid_in_tray_title")
                )
                settings["im_hiding_message"] = False
                save_settings()
        else:
            if msb.askyesno(titled_name + tray_sect.get("ask_to_exit_title"),
                            tray_sect.get("ask_to_exit")):
                quit_all(sys_icon, window=main_window)
    ...
    main_window.protocol('WM_DELETE_WINDOW', hide_window)
    # noinspection PyUnboundLocalVariable
    if settings["hide_after_start"] and f_settings("tray"):
        main_window.after(0, hide_window(True))
    ...  # Корректировка размеров окна
    # main_window.geometry("400x250")
    main_window.geometry("320x280")
    main_window.resizable(width=False, height=False)
    ...  # Финальная подготовка и запуск основного цикла!!
    displays_page_update(do_check_cam=False)
    main_window.iconbitmap(Path("resources", "logo2.ico"))
    main_window.after(0, check)
    main_window.mainloop()
    main_window.destroy()
    if sys_icon is not None:
        sys_icon.stop()
    print("-- main quit")


"""
    Starter
"""

do_start = True


def check_for_updates(tag_or_sha, c_edition, user_files_path, save_old_files, do_ask_user):
    import updater.manager
    if updater.manager.check_for_updates_with_ui(
            tag_or_sha=tag_or_sha,
            save_old_files=save_old_files,
            edition=c_edition,
            user_files_path=user_files_path, do_ask_user=do_ask_user):
        settings["_venv_dir"] = os.getcwd()
        save_settings()
        access = os.access(Path(Path.cwd(), "requirements.txt"), os.W_OK & os.R_OK)
        os.chdir(waba_user_files_path)
        if access:
            os.system("installer.exe")
        else:
            os.system(f'''powershell -Command "Start-Process 'installer.exe' -Verb runAs"''')
        global do_start
        do_start = False
        return True
    return False


if __name__ == "__main__":
    lang.load_default()
    load_settings()
    load_version_file()
    if not settings["language"]:
        settings["language"] = lang.chose_lang()
        save_settings()
    lang.load(settings["language"])
    sett_lang_sect = lang.Section("main.json", "starter", "errors")
    if settings["checking_for_updates"] and f_settings("autoupdate", "main"):
        check_for_updates(github_tag, edition, waba_user_files_path, True, True)
    try:
        if do_start:
            displays = sbc.list_monitors()
            if len(displays) == 0:
                debug_window = tk.Tk()
                debug_window.iconbitmap(Path("resources", "logo2.ico"))
                debug_window.withdraw()
                msb.showerror(
                    titled_name + sett_lang_sect.get("no_monitors_title"),
                    sett_lang_sect.get("no_monitors")
                )
                debug_window.destroy()
                raise LookupError
            settings["display"] = displays[0]

            if check_device_exist():
                if settings["devices"] == {}:
                    settings["devices"]["<video0>"] = {
                        "displays": [displays[0]],
                        "keyframes": [],
                    }
            else:
                debug_window = tk.Tk()
                debug_window.iconbitmap(Path("resources", "logo2.ico"))
                debug_window.withdraw()
                msb.showerror(
                    titled_name + sett_lang_sect.get("no_devices_title"),
                    sett_lang_sect.get("no_devices")
                )
                debug_window.destroy()
                raise LookupError
            del displays

            for cs in settings["devices"]:
                # noinspection PyUnresolvedReferences
                cashed_dict_of_devices[cs] = settings["devices"][cs].copy()

            main()
    except LookupError:
        pass
