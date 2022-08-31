# -*- coding: utf-8 -*-
"""
    Загрузчик обновлений.
    Взаимодействует с основным кодом, подготавливает файлы для установщика.
"""
import os
import shutil
from pathlib import Path
import requests
import zipfile
import yaml


user = "kapertdog"
project = "WABA"


github_repository_url = f"https://api.github.com/repos/{user}/{project}"
github_releases_url = f"{github_repository_url}/releases"
github_commits_url = f"{github_repository_url}/commits"
github_repository_download_url = \
    f"https://github.com/{user}/{project}/archive/refs/heads/"
github_master_download_url = \
    f"https://github.com/{user}/{project}/archive/refs/heads/master.zip"


def setup(user_name, project_name):
    global github_repository_url, github_releases_url, github_commits_url, \
        github_repository_download_url, github_master_download_url
    github_repository_url = f"https://api.github.com/repos/{user_name}/{project_name}"
    github_releases_url = f"{github_repository_url}/releases"
    github_commits_url = f"{github_repository_url}/commits"
    github_repository_download_url = \
        f"https://github.com/{user_name}/{project_name}/archive/refs/heads/"
    github_master_download_url = \
        f"https://github.com/{user_name}/{project_name}/archive/refs/heads/master.zip"


setup(user, project)

""" API """


def get_github_repository_json():
    return requests.get(github_repository_url).json()


def get_github_releases_json():
    return requests.get(github_releases_url).json()


def get_github_commits_json():
    return requests.get(github_commits_url).json()


def get_commit_message(data: list, commit: int = 0):
    return data[commit]["commit"]["message"]


def check_for_release_updates(tag: str, data: list) -> bool:
    return data[0]["tag_name"] != tag


def check_for_venv_updates(sha: str, data: list) -> bool:
    return data[0]["sha"] != sha


def get_release_tag(data: list, release: int = 0):
    return data[release]["tag_name"]


def get_commit_sha(data: list, commit: int = 0):
    return data[commit]["sha"]


def get_release_update_link(data: list, asset: int = 0, release: int = 0):
    return data[release]["assets"][asset]["browser_download_url"]


def get_release_file_name(data: list, asset: int = 0, release: int = 0):
    return data[release]["assets"][asset]["name"]


def get_release_file_name_end_with(data: list, end_with: str, release: int = 0):
    asset = 0
    file = get_release_file_name(data, asset, release)
    while file[-4:] != end_with:
        asset += 1
        file = get_release_file_name(data, asset, release)
    return file, asset


def get_size_of_release(data: list, asset: int = 0, release: int = 0):
    return data[release]["assets"][asset]["size"]


def get_size_of_repo(data: list):
    return data["size"]


""" Функциональность """


def make_config_file(config_file_path: Path, app_dir: Path,
                     version: str, edition: str, save_old_files: bool,
                     do_make_version_file: bool, start_command: str):
    with open(Path(config_file_path, "config.yaml"), "w+") as config:
        config_data = {
            "app_dir": app_dir,
            "version": version,
            "edition": edition,
            "do_make_version_file": do_make_version_file,
            "save_old_files": save_old_files,
            "start_command": start_command,
        }
        yaml.dump(config_data, config, default_flow_style=False)
        ...


def clear_temporary_installer():
    installer_path = Path(os.getenv("APPDATA", ""), "waba", "installer.exe")
    if installer_path.exists():
        os.remove(installer_path)


def _download_file(url, path=Path()):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True, allow_redirects=True) as r:
        r.raise_for_status()
        with open(Path(path, local_filename), 'wb') as f:
            # print(len(r.))
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return Path(path, local_filename)


def _unzip_file(file_path, output_path: str = ""):
    with zipfile.ZipFile(file_path, "r") as file:
        file.extractall(output_path)


def download_update(edition, version, releases: list = None):
    cash_path = Path(os.getenv("APPDATA", ""), "waba", "cashed", "update")
    data_path = Path(os.getenv("APPDATA", ""), "waba", "update")
    update_data_path = Path(data_path, "waba_update_data")
    additional_data_path = Path(data_path, "waba_additional_files")
    if cash_path.exists():
        shutil.rmtree(cash_path)
    os.makedirs(cash_path)
    if data_path.exists():
        shutil.rmtree(data_path)
    os.makedirs(data_path)
    if update_data_path.exists():
        shutil.rmtree(update_data_path)
    os.makedirs(update_data_path)
    if additional_data_path.exists():
        shutil.rmtree(additional_data_path)
    os.makedirs(additional_data_path)

    match edition:
        case "folder":
            if not releases:
                releases = get_github_releases_json()
            file_name, asset = get_release_file_name_end_with(releases, ".zip", version)

            downloaded_file_path = _download_file(
                get_release_update_link(releases, asset, version),
                cash_path)

            _unzip_file(downloaded_file_path, cash_path)
            os.remove(downloaded_file_path)
            make_config_file(additional_data_path, os.getcwd(), version, edition,
                             True, False, f''' "WABA v.Dev_B.exe" ''')
            shutil.copyfile(Path("updater", "installer.exe"),
                            Path(data_path, "installer.exe"))
        case "exe":
            if not releases:
                releases = get_github_releases_json()
            file_name, asset = get_release_file_name_end_with(releases, ".exe", version)

            _download_file(get_release_update_link(releases, asset, version), cash_path)
        case "venv":
            downloaded_file_path = _download_file(
                github_repository_download_url + version + ".zip")
            _unzip_file(downloaded_file_path, cash_path)
            os.remove(downloaded_file_path)
            make_config_file(additional_data_path, os.getcwd(),
                             get_commit_sha(get_github_commits_json(), 0), edition,
                             True, True, "start start_vB.cmd")

            shutil.copy2(Path(cash_path, os.listdir(cash_path)[0], "requirements.txt"),
                         data_path.parent)
            if not Path("venv").exists():
                # unzip_file("updater/empty_venv.zip", "updater/waba_additional_files")
                address = r".\updater\install_requirements_to_new.cmd"
            else:
                address = r".\updater\install_requirements_to_global.cmd"
            if os.access(os.getcwd(), os.W_OK & os.R_OK):
                os.system(address)
            else:
                os.system(
                    f'''powershell -Command "Start-Process '{address}' -Verb runAs"'''
                )
            os.remove(Path(data_path.parent, "requirements.txt"))

            shutil.copyfile(Path("updater", "installer.exe"), Path(cash_path, "installer.exe"))
    for item in os.listdir(cash_path):
        file = Path(cash_path, item)
        if file.is_dir():
            for sub_file in os.listdir(file):
                shutil.move(Path(file, sub_file), update_data_path)
            # shutil.copytree(file, update_data_path)
        elif file.is_file():
            shutil.move(file, data_path)
    shutil.rmtree(cash_path)


""" Интерфейс """

do_reload = True


def check_for_updates_with_ui(tag_or_sha, user_files_path: str,
                              edition: str = "debug", save_old_files: bool = True,
                              do_ask_user: bool = True):

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
                    asset = 0
                    file_name = get_release_file_name(releases, asset)
                    while file_name[-4:] != ".zip":
                        asset += 1
                        file_name = get_release_file_name(releases, asset)

                    main_file_url = get_release_update_link(releases, asset)
                    size_of_file = get_size_of_release(releases)
                    new_tag_or_sha = get_release_tag(releases)
                    start_command = f''' "WABA v.Dev_B.exe" '''
                    do_make_version_file = False
                    do_pip_update_requirements = False
                    if (not msb.askyesno(
                            "Updater: Обновление",
                            "Найдена новая версия приложения!\n"
                            "Хотите обновить? "
                            f"( ~{size_of_file // 1024 // 1024} MB )\n"
                            "\n"
                            f"{tag_or_sha} -> {new_tag_or_sha}\n"))\
                            or (not do_ask_user):
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
                    commit_message = get_commit_message(commits)
                    main_file_url = github_master_download_url
                    size_of_file = get_size_of_repo(repository) * 1024
                    new_tag_or_sha = get_commit_sha(commits)
                    start_command = "start_vB.cmd"
                    do_make_version_file = True
                    do_pip_update_requirements = True
                    if not msb.askyesno("Updater: Обновление",
                                        "Найдена новая версия приложения!\n"
                                        "Хотите обновить? "
                                        f"( ~{size_of_file // 1024 // 1024} MB )\n"
                                        "\n"
                                        f"{tag_or_sha[:7]} -> {new_tag_or_sha[:7]}\n\n"
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

    def download(url_address, out_folder):
        local_filename = url_address.split('/')[-1]
        update_status(f"Скачивание {local_filename}...")
        with requests.get(url_address, stream=True, allow_redirects=True) as r:
            r.raise_for_status()
            with open(f"{out_folder}/{local_filename}", 'wb') as f:
                # print(len(r.))
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    pb["value"] += 1
                    window.update()
            return local_filename

    def update():
        try:
            import os
            import shutil
            old_files = os.listdir(user_files_path)
            pb.start()
            # Если в выходе уже были файлы, удаляем
            update_status("Чистим чистим...")
            for file in old_files:
                match file:
                    case "settings.yaml":
                        ...
                    case "cashed":
                        ...
                    case _:
                        old_file = Path(user_files_path, file)
                        if old_file.is_dir():
                            shutil.rmtree(old_file)
                        else:
                            os.remove(old_file)
            del old_files
            old_files = os.listdir(user_files_path)
            # if os.path.exists(f"{user_files_path}/waba_update_data"):
            #     shutil.rmtree(f"{user_files_path}/waba_update_data")
            # if os.path.exists(f"{user_files_path}/waba_additional_files"):
            #     shutil.rmtree(f"{user_files_path}/waba_additional_files")
            # if os.path.exists(f"{user_files_path}/installer.exe"):
            #     os.remove(f"{user_files_path}/installer.exe")
            # Разбираемся с основным файлом
            download(main_file_url, user_files_path)
            update_status("Распаковка косметики...")
            pb.stop()
            pb.config(mode="indeterminate")
            pb.start()
            window.update()
            _unzip_file(f"{user_files_path}/{file_name}", user_files_path)
            os.remove(f"{user_files_path}/{file_name}")
            folder_name = [item for item in os.listdir(user_files_path)
                           if item not in frozenset(old_files)][0]

            # Теперь с дополнительными
            pb.stop()
            pb.config(maximum=5)
            pb["value"] = 0
            pb.start()
            update_status("Доп файлы...")
            if not os.path.exists(f"{user_files_path}/waba_additional_files"):
                os.mkdir(f"{user_files_path}/waba_additional_files")
            add_files_list = list()
            for add_file_url in files_urls:
                add_file_name = download(add_file_url, f"{user_files_path}")
                update_status(f"Распаковка {add_file_name}...")
                _unzip_file(f"{user_files_path}/{add_file_name}",
                            f"{user_files_path}/waba_additional_files")
                add_files_list.extend(
                    [item for item in os.listdir(f"{user_files_path}/waba_additional_files")
                     if item not in frozenset(old_files)
                     ]
                )
            if do_pip_update_requirements:
                shutil.copy2(Path(user_files_path, folder_name, "requirements.txt"),
                             user_files_path)
                if not Path("venv").exists():
                    # unzip_file("updater/empty_venv.zip", "updater/waba_additional_files")
                    address = r".\updater\install_requirements_to_new.cmd"
                else:
                    address = r".\updater\install_requirements_to_global.cmd"
                if os.access(os.getcwd(), os.W_OK & os.R_OK):
                    os.system(address)
                else:
                    os.system(
                        f'''powershell -Command "Start-Process '{address}' -Verb runAs"'''
                    )
                os.remove(f"{user_files_path}/requirements.txt")

            update_status("Подготовка к установке...")
            # Вытаскиваем дополнительные файлы из их папок
            for file in add_files_list:
                if os.path.isdir(f"{user_files_path}/waba_additional_files/{file}"):
                    shutil.copytree(f"{user_files_path}/waba_additional_files/{file}",
                                    f"{user_files_path}/waba_additional_files")
                    shutil.rmtree(f"{user_files_path}/waba_additional_files/{file}")
            # Создаём дополнительные файлы для установщика
            with open(f"{user_files_path}/waba_additional_files/config.yaml", "w+") as config:
                config_data = {
                    "do_make_version_file": do_make_version_file,
                    "save_old_files": save_old_files,
                    "version": new_tag_or_sha,
                    "edition": edition,
                    "start_command": start_command,
                    "app_dir": os.getcwd()
                }
                yaml.dump(config_data, config, default_flow_style=False)
                ...
            # Переносим!!
            shutil.copytree(f"{user_files_path}/{folder_name}",
                            f"{user_files_path}/waba_update_data")
            shutil.copyfile(f"updater/installer.exe",
                            f"{user_files_path}/installer.exe")
            # Чистим чистим
            shutil.rmtree(f"{user_files_path}/{folder_name}")

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


if __name__ == "__main__":
    rl = get_github_releases_json()
    for i in rl[0]["assets"]:
        print(i)
    print(get_release_file_name_end_with(rl, ".zip"))
