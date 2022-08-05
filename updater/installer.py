# -*- coding: utf-8 -*-
"""
    Независимый установщик!
    Кинуть к настройкам, принимает инструкции из них.
    Заменяет старые файлы новыми.
    Должен быть сразу exe и поставляться вместе с основной программой~
"""
import progress.spinner
pb = progress.spinner.Spinner()
pb.message = "Initialization..."
pb.start()
import shutil
pb.update()
import yaml
pb.update()
import os
pb.update()
from pathlib import Path
pb.update()
import filecmp
pb.update()


def get_app_directory():
#    settings_path = Path(os.getenv("APPDATA", ""), "waba", "settings.yaml")
#    with settings_path.open("r") as s:
#        return yaml.safe_load(s)["_venv_dir"]
    with open("settings.yaml") as s:
        return yaml.safe_load(s)["_venv_dir"]


from progress.bar import IncrementalBar


def update(from_dir: Path, to_dir: Path):
    from_list = os.listdir(from_dir)
    to_list = os.listdir(to_dir)
    upb = IncrementalBar(from_dir.name, max=len(from_list))

    def copy(file_name):
        shutil.copy2(
            Path(from_dir, file_name),
            Path(to_dir, file_name)
        )
        ...

    def delcopy(file_name):
        os.remove(Path(to_dir, file_name))
        copy(file_name)

    for file in from_list:
        if Path(from_dir, file).is_dir():
            if not Path(to_dir, file).exists():
                Path(to_dir, file).mkdir()
            update(Path(from_dir, file), Path(to_dir, file))
        elif file not in to_list:
            copy(file)
        elif not filecmp.cmp(Path(from_dir, file), Path(to_dir, file), shallow=True):
            delcopy(file)
        upb.next()
    upb.finish()


pb.update()

app_dir = get_app_directory()
# shutil.rmtree(app_dir)

pb.message = "Installing..."
pb.update()

# shutil.copytree("waba_update_data", app_dir)
print("From:", Path(Path.cwd(), "waba_update_data"))
print("To:", Path(app_dir))
update(Path(Path.cwd(), "waba_update_data"), Path(app_dir))

pb.message = "Deleting temporary files..."
pb.update()

shutil.rmtree("waba_update_data")

pb.message = "Done!"
pb.update()

pb.finish()
input("Press ENTER to continue...")
# os.remove("installer.exe")

print("Restarting app...")

os.chdir(app_dir)
os.system(f'"{app_dir}/WABA v.Dev_B.exe"')
exit()