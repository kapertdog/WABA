from statistics import mean
from math import fabs
import screen_brightness_control as sbc
import numpy as np
import tkinter as tk
import cv2
import os
import time
import yaml
import notification


settings_version = 0
settings = {
    "settings_version": settings_version,
    "mode": "CMD",
    "logging": False,
    "do_notify": False,
    "min_step_for_notify": 2,
    "printing": True,
    "timeout_s": 60,
    "camera_id": 0,
    "scan_repeats": 1,
    "read_repeats": 0,
    "do_use_custom_func": False,
    "brightness_transform_func": "{0} ** 2 // 100",
}


def load_settings():
    global settings
    if not os.path.exists("settings.yaml"):
        with open("settings.yaml", "w+") as s:
            yaml.dump(settings, s, default_flow_style=False)
    else:
        with open("settings.yaml", "r+") as s:
            settings = yaml.safe_load(s)

    return settings


def get_brightness(device_id: int = 0, scan_repeats: int = 1, read_repeats: int = 0) -> int:

    brightness = list()
    # print(f"# Захват изображения с камеры #{device_id}...")
    cap = cv2.VideoCapture(device_id)
    for _ in range(scan_repeats):
        for _ in range(read_repeats):
            cap.read()
        ret, frame = cap.read()
        # print("  Обесцвечивание...")
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # print("# Подсчёт среднего числа...")
        color_summ = int()
        width, height = np.size(gray, 0), np.size(gray, 1)
        # print(f"  Размер изображения: {width}x{height}")
        for x in range(width):
            for y in range(height):
                color_summ += gray[x, y]
        brightness.append(color_summ // (width * height))
    cap.release()

    # print("# Вывод...")
    return mean(brightness)


def get_FPS():
    ...


# def stackoverflow_check():
#     cap = cv2.VideoCapture(0)
#
#     while True:
#         ret, frame = cap.read()
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         # cv2.imshow('Video', frame)
#         cv2.imshow('frame', gray)
#         # print(type(gray))
#         # print(gray[0, 0])
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
#     cap.release()
#     cv2.destroyAllWindows()


def update_brightness(printing=True):
    brightness = get_brightness(
        settings["camera_id"],
        settings["scan_repeats"],
        settings["read_repeats"]
    )
    screen_brightness = brightness * 100 // 255
    if settings["do_use_custom_func"]:
        modified_screen_brightness = eval(settings["brightness_transform_func"].format(screen_brightness))
    else:
        modified_screen_brightness = screen_brightness ** 2 // 100

    if printing:
        os.system("cls")
        print(f" -=- {time.asctime()} -=- ")
        print(f">> Яркость: {brightness} | {screen_brightness}%")
        print(f">> С пересчётом: {modified_screen_brightness}%")

    sbc.set_brightness(modified_screen_brightness)
    return brightness, screen_brightness, modified_screen_brightness


def main():

    load_settings()
    if settings_version != settings["settings_version"]:
        input("! Несовместимая версия настроек !\nНажмите Enter для сброса...")
        os.remove("settings.yaml")
        exit()

    match settings["mode"].lower():

        case "debug":
            print(" =!= DEBUG MODE =!= ")
            while True:
                try:
                    print(eval(input("# ")))
                except Exception as error:
                    print(error)

        case "cmd":
            while True:
                os.system("cls")
                print("# Обновляю...")
                load_settings()
                osb = sbc.get_brightness()[0]
                b, sb, msb = update_brightness(settings["printing"])
                # TODO: Более плавное определение повторений
                if settings["do_notify"] and fabs(osb - msb) >= settings["min_step_for_notify"]:
                    notification.notify(
                        title="Яркость обновлена",
                        msg=f"{b}/255 | {osb}% -> {msb}%",
                        icon_path="logo.ico",
                        duration=5
                    )

                time.sleep(settings["timeout_s"])
                os.system("cls")

        case "tkinter":
            window = tk.Tk()
            window.title("Ин дев")
            print("В разработке крч")
            lbl_main = tk.Label(window, text="Amogus")
            lbl_main.grid(column=0, row=0)
            window.mainloop()
            ...

        case _:
            input("! Несуществующий режим загрузки ! \nНажмите Enter для сброса...")
            os.remove("settings.yaml")


if __name__ == "__main__":
    main()
