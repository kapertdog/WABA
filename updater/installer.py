# -*- coding: utf-8 -*-
"""
    Независимый установщик!
    Кинуть к настройкам, принимает инструкции из них.
    Заменяет старые файлы новыми.
    Должен быть сразу exe и поставляться вместе с основной программой~
"""
import progress.spinner
pb = progress.spinner.Spinner()
pb.message("Initialization...")
pb.start()
import shutil
import yaml
import os


def get_app_directory():
    with open("settings.yaml", "r") as s:
        return yaml.safe_load(s)["_venv_dir"]


pb.message("Installing...")
shutil.move("waba_update_data", get_app_directory())
pb.message("Done!")
pb.finish()
os.remove("installer.exe")
