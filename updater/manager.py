# -*- coding: utf-8 -*-
"""
    Загрузчик обновлений.
    Взаимодействует с основным кодом, подготавливает файлы для установщика.
"""
import requests
import zipfile


user = "kapertdog"
project = "waba"


github_releases_url = f"https://api.github.com/repos/{user}/{project}/releases"
github_commits_url = f"https://api.github.com/repos/{user}/{project}/commits"


def setup(user_name, project_name):
    global github_releases_url, github_commits_url
    github_releases_url = f"https://api.github.com/repos/{user_name}/{project_name}/releases"
    github_commits_url = f"https://api.github.com/repos/{user_name}/{project_name}/commits"


def get_github_releases_json():
    return requests.get(github_releases_url).json()


def check_for_release_updates(tag: str, data: list) -> bool:
    return data[0]["tag_name"] != tag


def check_for_venv_updates(sha: str, data: list) -> bool:
    return data[0]["sha"] != sha


def get_last_release_update_link(data: list):
    return data[0]["assets"][0]["browser_download_url"]


def get_last_release_file_name(data: list):
    return data[0]["assets"][0]["name"]


def get_size_of_last_release(data: list):
    return data[0]["assets"][0]["size"]


def download_file(url):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True, allow_redirects=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            # print(len(r.))
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename


def unzip_file(file_path, output_path: str = ""):
    with zipfile.ZipFile(file_path, "r") as file:
        file.extractall(output_path)


"""
    Интерфейс
"""


def check_for_updates_with_ui(tag_or_sha, user_files_path: str, edition: str = "folder"):

    import tkinter as tk
    from tkinter import messagebox as msb
    from tkinter import ttk
    releases = get_github_releases_json()
    match edition:
        case "folder":
            # noinspection PyBroadException
            try:
                if not check_for_release_updates(tag_or_sha, releases):
                    return False
                else:
                    if not msb.askyesno("Updater: Обновление", "Найдена новая версия приложения!\n"
                                                               "Хотите обновить?"):
                        return False
            except Exception:
                return False
        case _:
            msb.showerror("Updater: В разработке", "Авто-обновление всё ещё разрабатывается~")
            return False
    window = tk.Tk()
    window.geometry('300x120')
    window.title("Updater: Обновление")

    pb_var = tk.IntVar()
    pb = ttk.Progressbar(
        window,
        variable=pb_var,
        maximum=get_size_of_last_release(releases) // (8192 * 8),
        orient="horizontal",
        mode="determinate",
        length=280,
    )
    pb.pack(padx=10, pady=20)

    lbl = tk.Label(
        window,
        text="-=- Подготовка -=-",
    )
    lbl.pack(padx=10, pady=20)

    file_name = get_last_release_file_name(releases)

    def update_status(status: str):
        lbl.config(text=f"-=- {status} -=-")

    def download():
        url = get_last_release_update_link(releases)
        local_filename = url.split('/')[-1]
        update_status(f"Скачивание {local_filename}...")
        with requests.get(url, stream=True, allow_redirects=True) as r:
            r.raise_for_status()
            with open(f"updater/{local_filename}", 'wb') as f:
                # print(len(r.))
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    pb["value"] += 1
                    window.update()

    def update():
        try:
            import os
            old_files = os.listdir("updater")
            pb.start()
            download()
            update_status("Разархивация...")
            pb.stop()
            pb.config(mode="indeterminate")
            pb.start()
            window.update()
            unzip_file(f"updater/{file_name}", "updater")
            os.remove(f"updater/{file_name}")
            update_status("Подготовка к установке...")
            import shutil
            folder_name = [item for item in os.listdir("updater") if item not in frozenset(old_files)][0]
            shutil.copytree(f"updater/{folder_name}", f"{user_files_path}/waba_update_data")
            shutil.copyfile(f"updater/installer.exe", f"{user_files_path}/installer.exe")
            shutil.rmtree(f"updater/{folder_name}")

            window.destroy()
            ...
        except Exception as err:
            msb.showerror("Updater: сбой", f"Что-то пошло не так, обновление отменено.\n"
                                           f"{err}")
            window.destroy()
            exit(0)

    window.after(1000, update)

    window.mainloop()
    return True
