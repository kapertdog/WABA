# -*- coding: utf-8 -*-
"""
    Загрузчик обновлений.
    Взаимодействует с основным кодом, подготавливает файлы для установщика.
"""
import os
from pathlib import Path
import requests
import zipfile
import yaml


user = "kapertdog"
project = "WABA"


github_repository_url = f"https://api.github.com/repos/{user}/{project}"
github_releases_url = f"{github_repository_url}/releases"
github_commits_url = f"{github_repository_url}/commits"
github_master_download_url = f"https://github.com/{user}/{project}/archive/refs/heads/master.zip"


def setup(user_name, project_name):
    global github_releases_url, github_commits_url
    github_releases_url = f"https://api.github.com/repos/{user_name}/{project_name}/releases"
    github_commits_url = f"https://api.github.com/repos/{user_name}/{project_name}/commits"


setup(user, project)


def get_github_repository_json():
    return requests.get(github_repository_url).json()


def get_github_releases_json():
    return requests.get(github_releases_url).json()


def get_github_commits_json():
    return requests.get(github_commits_url).json()


def get_last_commit_message(data: list):
    return data[0]["commit"]["message"]


def check_for_release_updates(tag: str, data: list) -> bool:
    return data[0]["tag_name"] != tag


def check_for_venv_updates(sha: str, data: list) -> bool:
    return data[0]["sha"] != sha


def get_last_release_tag(data: list):
    return data[0]["tag_name"]


def get_last_commit_sha(data: list):
    return data[0]["sha"]


def get_last_release_update_link(data: list, asset: int = 0):
    return data[0]["assets"][asset]["browser_download_url"]


def get_last_release_file_name(data: list, asset: int = 0):
    return data[0]["assets"][asset]["name"]


def get_size_of_last_release(data: list, asset: int = 0):
    return data[0]["assets"][asset]["size"]


def get_size_of_repo(data: list):
    return data["size"]


def clear_temporary_installer():
    installer_path = Path(os.getenv("APPDATA", ""), "waba", "installer.exe")
    if installer_path.exists():
        os.remove(installer_path)


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

do_reload = True


def check_for_updates_with_ui(tag_or_sha, user_files_path: str, edition: str = "debug"):

    import tkinter as tk
    from tkinter import messagebox as msb
    from tkinter import ttk
    files_urls = list()
    match edition:
        case "folder":
            # noinspection PyBroadException
            try:
                releases = get_github_releases_json()
                if not check_for_release_updates(tag_or_sha, releases):
                    return False
                else:
                    file_name = get_last_release_file_name(releases)
                    main_file_url = get_last_release_update_link(releases)
                    size_of_file = get_size_of_last_release(releases)
                    new_tag_or_sha = get_last_release_tag(releases)
                    start_command = f''' "WABA v.Dev_B.exe" '''
                    do_make_version_file = False
                    do_pip_update_requirements = False
                    if not msb.askyesno("Updater: Обновление", "Найдена новая версия приложения!\n"
                                                               "Хотите обновить? "
                                                               f"( ~{size_of_file // 1024 // 1024} MB )\n"
                                                               "\n"
                                                               f"{tag_or_sha} -> {new_tag_or_sha}\n"):
                        return False
            except Exception as err:
                msb.showerror("Waba: сбой", f"Не удалось проверить наличие обновлений\n\n"
                                            f"{err}")
                return False
        case "venv":
            # noinspection PyBroadException
            try:
                commits = get_github_commits_json()
                repository = get_github_repository_json()
                if not check_for_venv_updates(tag_or_sha, commits):
                    return False
                else:
                    file_name = f"master.zip"
                    commit_message = get_last_commit_message(commits)
                    main_file_url = github_master_download_url
                    size_of_file = get_size_of_repo(repository) * 1024
                    new_tag_or_sha = get_last_commit_sha(commits)
                    start_command = "start_vB.cmd"
                    do_make_version_file = True
                    do_pip_update_requirements = True
                    if not msb.askyesno("Updater: Обновление", "Найдена новая версия приложения!\n"
                                                               "Хотите обновить? "
                                                               f"( ~{size_of_file // 1024 // 1024} MB )\n"
                                                               "\n"
                                                               f"{tag_or_sha[:7]} -> {new_tag_or_sha[:7]}\n"
                                                               f"Что нового:\n{commit_message}"):
                        return False
            except Exception as err:
                msb.showerror("Waba: сбой", f"Не удалось проверить наличие обновления\n\n"
                                            f"{err}")
                return False
        case _:
            msb.showerror("Updater: В разработке", "Функция проверки обновлений\n"
                                                   "активирована файлом настроек,\n"
                                                   "но пока не реализована\n"
                                                   f'для "{edition}" издания.')
            return False
    window = tk.Tk()
    window.geometry('300x120')
    window.title("Updater: Обновление")

    pb_var = tk.IntVar()
    pb = ttk.Progressbar(
        window,
        variable=pb_var,
        maximum=size_of_file // 8192 // 7,
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

    def update_status(status: str):
        lbl.config(text=f"-=- {status} -=-")

    def download(url_address):
        local_filename = url_address.split('/')[-1]
        update_status(f"Скачивание {local_filename}...")
        with requests.get(url_address, stream=True, allow_redirects=True) as r:
            r.raise_for_status()
            with open(f"updater/{local_filename}", 'wb') as f:
                # print(len(r.))
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    pb["value"] += 1
                    window.update()
            return local_filename

    def update():
        try:
            import os
            old_files = os.listdir("updater")
            pb.start()
            # Разбираемся с основным файлом
            download(main_file_url)
            update_status("Распаковка косметики...")
            pb.stop()
            pb.config(mode="indeterminate")
            pb.start()
            window.update()
            unzip_file(f"updater/{file_name}", "updater")
            os.remove(f"updater/{file_name}")
            folder_name = [item for item in os.listdir("updater") if item not in frozenset(old_files)][0]

            # Теперь с дополнительными
            pb.stop()
            pb.config(maximum=0)
            pb["value"] = 0
            pb.start()
            update_status("Доп файлы...")
            if not os.path.exists("updater/waba_additional_files"):
                os.mkdir("updater/waba_additional_files")
            add_files_list = list()
            for add_file_url in files_urls:
                add_file_name = download(add_file_url)
                update_status(f"Распаковка {add_file_name}...")
                unzip_file(f"updater/{add_file_name}", "updater/waba_additional_files")
                add_files_list.extend(
                    [item for item in os.listdir("updater/waba_additional_files")
                     if item not in frozenset(old_files)
                     ]
                )
            import shutil
            if do_pip_update_requirements:
                shutil.copy2(Path("updater", folder_name, "requirements.txt"), "updater")
                if not Path("venv").exists():
                    unzip_file("updater/empty_venv.zip", "updater/waba_additional_files")
                    os.system(
                        ' "updater/install_requirements_to_new.cmd" '
                    )
                else:
                    os.system(
                        ' "updater/install_requirements_to_global.cmd" '
                    )
                os.remove("updater/requirements.txt")

            update_status("Подготовка к установке...")
            # Вытаскиваем дополнительные файлы из их папок
            for file in add_files_list:
                if os.path.isdir(f"updater/waba_additional_files/{file}"):
                    shutil.copytree(f"updater/waba_additional_files/{file}", "updater/waba_additional_files")
                    shutil.rmtree(f"updater/waba_additional_files/{file}")
            # Если в выходе уже были файлы, удаляем
            if os.path.exists(f"{user_files_path}/waba_update_data"):
                shutil.rmtree(f"{user_files_path}/waba_update_data")
            if os.path.exists(f"{user_files_path}/waba_additional_files"):
                shutil.rmtree(f"{user_files_path}/waba_additional_files")
            if os.path.exists(f"{user_files_path}/installer.exe"):
                os.remove(f"{user_files_path}/installer.exe")
            # Создаём дополнительные файлы для установщика
            with open(f"updater/waba_additional_files/config.yaml", "w+") as config:
                config_data = {
                    "do_make_version_file": do_make_version_file,
                    "version": new_tag_or_sha,
                    "edition": edition,
                    "start_command": start_command
                }
                yaml.dump(config_data, config, default_flow_style=False)
                ...
            # Переносим!!
            shutil.copytree(f"updater/{folder_name}", f"{user_files_path}/waba_update_data")
            shutil.copytree(f"updater/waba_additional_files", f"{user_files_path}/waba_additional_files")
            shutil.copyfile(f"updater/installer.exe", f"{user_files_path}/installer.exe")
            shutil.rmtree(f"updater/{folder_name}")
            shutil.rmtree(f"updater/waba_additional_files")

            window.destroy()
            ...
        except Exception as err_:
            msb.showerror("Updater: сбой", f"Что-то пошло не так, обновление отменено.\n"
                                           f"{err_}\n"
                                           f"{releases}")
            window.destroy()
            global do_reload
            do_reload = False

    window.after(1000, update)

    window.mainloop()
    global do_reload
    return do_reload
