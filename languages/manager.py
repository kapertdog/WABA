# -*- coding: utf-8 -*-
"""
    Менеджер языковых пакетов
"""
import json
import os
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import googletrans
from pathlib import Path

# TODO:
#  Поддержка смены языка в реальном времени,
#  Проверка целостности перевода,
#  Импорт переводов из файла,

""" Заглавные переменные """
current_lang = {}
default_lang = {}
cashed_langs_path = Path(os.getenv("APPDATA", ""), "waba", "cashed", "languages")
""" Задание общей стилистики """
example = {
    # Заголовок
    "info": {
        "%name%": "default",
        "%head%": "",
    },
    # Основные данные
    "data": {
        # Разделы
        "main-section": {
            # Может иметь значения # Пока невозможно
            "element": "value",
            # Под-разделы
            "sub-section": {
                # Элементы и значения
                "element": "value"
            }
        },
        "additional-section": {

        }
    }
}

""" Работа с файлами """


def loaded():
    """
    :return: True if any lang is loaded
    """
    return bool(default_lang) or bool(current_lang)


def _load(file_path: Path):
    with file_path.open("r", encoding="UTF-8") as file:
        if file_path.name[-5:] == ".json":
            return json.load(file)
        else:
            return file.read()


def load(lang_name: str, printing: bool = True):
    if printing:
        print(f"- Loading {lang_name} lang -")
    global current_lang, default_lang
    lang_path = Path(cashed_langs_path, lang_name)

    if default_lang == {}:
        for file_name in os.listdir(Path("languages", "defaults")):
            default_lang[file_name] = _load(Path("languages", "defaults", file_name))
        if printing:
            print(f" default lang loaded")
    current_lang.clear()

    if lang_path.exists():
        path = lang_path
    else:
        path = Path("languages", "data", lang_name)

    for file_name in os.listdir(Path("languages", "defaults")):
        if Path(path, file_name).exists():
            current_lang[file_name] = _load(Path(path, file_name))
            if printing:
                print(f"[{lang_name}]: {file_name} is loaded")
        elif printing:
            print(f"! [{lang_name}]: {file_name} is missing")


def _check(head_dict, other_dict):
    diffs = 0
    for key in head_dict:
        if type(head_dict[key]) == dict:
            diffs += _check(head_dict[key], other_dict[key])
        elif key not in other_dict:
            diffs += 1
        elif head_dict[key] == other_dict[key]:
            diffs += 1
    return diffs


def check_differences():
    return _check(default_lang["main.json"]["data"],
                  current_lang["main.json"]["data"])


def info(loaded_file_name):
    return current_lang[loaded_file_name]["info"],


def file_info(file_path: Path):
    with file_path.open("r") as file:
        _file = json.load(file)


def get_langs_list():
    return (*os.listdir(cashed_langs_path),
            *os.listdir(Path("languages", "data")))


def import_lang(directory: Path):
    """

    :param directory: ".zip" (like '>en.zip</en/data' inside)
    or lang_forder (with data inside!! not folder in folder)
    """
    if not cashed_langs_path.exists():
        os.makedirs(cashed_langs_path)
    if directory.is_dir():
        target_dir = Path(cashed_langs_path, directory.name)
        if target_dir.exists():
            shutil.rmtree(target_dir)
        shutil.copytree(directory, target_dir)
    elif directory.name[-4:] == ".zip":
        import zipfile
        with zipfile.ZipFile(directory, "r") as z_file:
            z_file.extractall(cashed_langs_path)
    else:
        raise TypeError("Wrong file or path")


def _translate(data: dict, lang_from: str, lang_to: str):
    translator = googletrans.Translator()
    result = dict()
    for key in data:
        if type(data[key]) == dict:
            result[key] = _translate(data[key], lang_from, lang_to)
        else:
            result[key] = translator.translate(data[key], lang_to, lang_from).text
    return result


def make_translate(lang_to: str):
    def_path = Path("languages", "defaults")
    out_path = Path(os.getenv("APPDATA", ""), "waba", "cashed", "languages", f"auto-{lang_to}")
    if out_path.exists():
        shutil.rmtree(out_path)
    new_lang_pack = dict()
    for file in os.listdir(def_path):
        with Path(def_path, file).open("r+", encoding="UTF-8") as r_file:
            if file[-5:] == ".json":
                new_lang_pack[file] = json.load(r_file)
            else:
                new_lang_pack[file] = r_file.read()

    if not out_path.exists():
        os.makedirs(out_path)

    for file in new_lang_pack:
        if file[-5:] == ".json":
            new_lang_pack[file]["info"]["%head%"] = "ru"
            new_lang_pack[file]["info"]["%name%"] = googletrans.LANGUAGES[lang_to]
            new_lang_pack[file]["data"] = _translate(new_lang_pack[file]["data"], "ru", lang_to)
            with Path(out_path, file).open("w+", encoding="UTF-8") as w_file:
                json.dump(new_lang_pack[file], w_file, sort_keys=True, indent=2)
        else:
            new_lang_pack[file] = _translate({"data": new_lang_pack[file]}, "ru", lang_to)
            with Path(out_path, file).open("w+", encoding="UTF-8") as w_file:
                w_file.write(new_lang_pack[file]["data"])


""" Обработка запросов """


def decompose(data, *args):
    copy_of_args = [*args]
    if args != ():
        return decompose(data[copy_of_args.pop(0)], *copy_of_args)
    return data


def get(file, *args):
    if not args:
        if file in current_lang:
            return current_lang[file]
        elif file in default_lang:
            return default_lang[file]
        else:
            return file
    else:
        try:
            return decompose(current_lang[file]["data"], *args)
        except KeyError:
            try:
                return decompose(default_lang[file]["data"], *args)
            except KeyError:
                return args[-1]


class Section:
    def __init__(self, *path):
        self.path = path

    def get(self, *path):
        return get(*self.path, *path)


""" GUI """


class GenerateLang(tk.Tk):
    def __init__(self):
        self.cancel_chose = True
        lang_sect = Section("languages.json", "generate_lang")
        super().__init__()
        if not loaded():
            load("en", False)

        self.title(lang_sect.get("title"))

        self.select_frame = ttk.Frame(self)

        self.chose_lang_lbl = ttk.Label(
            self.select_frame,
            text=lang_sect.get("chose_lang")
        )
        self.chose_lang_lbl.pack(side=tk.LEFT, padx=5, pady=5)
        self.selected_lang = tk.StringVar()
        self.langs_list = ttk.Combobox(
            self.select_frame,
            textvariable=self.selected_lang,
            values=[*googletrans.LANGUAGES]
        )
        self.langs_list.pack(fill=tk.X, padx=5, pady=5)

        self.select_frame.pack(fill=tk.X)

        self.submit_frame = ttk.Frame(self)

        self.submit_btn = ttk.Button(
            self.submit_frame,
            text=lang_sect.get("translate"),
            command=self.submit
        )
        self.submit_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        tk.Label(
            self,
            text=lang_sect.get("warn"),
            foreground="gray"
        ).pack(fill=tk.X)

        self.submit_frame.pack(side=tk.BOTTOM, fill=tk.X)

    def submit(self):
        self.cancel_chose = False
        # self.quit()
        self.destroy()

    def chose_lang(self):
        self.mainloop()
        if self.cancel_chose:
            self.selected_lang.set("")
        return self.selected_lang.get()


class LangSelectWindow(tk.Tk):
    def __init__(self):
        lang_sect = Section("languages.json", "chose_lang")
        super().__init__()
        if not loaded():
            load("en", False)

        self.title(lang_sect.get("title"))

        self.select_frame = ttk.Frame(self)

        self.chose_lang_lbl = ttk.Label(
            self.select_frame,
            text=lang_sect.get("chose_lang")
        )
        self.chose_lang_lbl.pack(side=tk.LEFT, padx=5, pady=5)

        self.selected_lang = tk.StringVar()
        self.langs_list = ttk.Combobox(
            self.select_frame,
            textvariable=self.selected_lang,
        )
        self.update_langs_list()
        self.langs_list.pack(fill=tk.X, padx=5, pady=5)
        self.langs_list.set("ru")

        self.select_frame.pack(fill=tk.X)

        self.buttons_frame = ttk.Frame(self)

        self.import_btn = ttk.Button(
            self.buttons_frame,
            text=lang_sect.get("import"),
            command=self.import_f
        )
        self.import_btn.pack(side=tk.LEFT, padx=5, pady=2)

        self.translate_btn = ttk.Button(
            self.buttons_frame,
            text=lang_sect.get("translate"),
            command=self.generate
        )
        self.translate_btn.pack(side=tk.LEFT, pady=2)

        self.buttons_frame.pack(fill=tk.X, padx=5)

        self.bottom_frame = ttk.Frame(self)

        self.submit_btn = ttk.Button(
            self.bottom_frame,
            text=lang_sect.get("submit"),
            command=self.submit
        )
        self.submit_btn.pack(side=tk.RIGHT, padx=5, pady=5)

        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

    def generate(self):
        self.destroy()
        gn_window = GenerateLang()
        answ = gn_window.chose_lang()
        if answ:
            make_translate(answ)
        r_main_window = LangSelectWindow()
        self.selected_lang.set(r_main_window.chose_lang())

    def import_f(self):
        file = fd.askopenfilename(
            title=get("languages.json", "chose_lang", "select_zip_file_title"),
            filetypes=((get("languages.json", "chose_lang", "only_zip_files"), "*.zip"),)
        )
        if file:
            import_lang(file)
            self.update_langs_list()

    def update_langs_list(self):
        langs_list = get_langs_list()
        self.langs_list.config(values=langs_list)
        self.langs_list.update()

    def chose_lang(self):
        self.mainloop()
        return self.selected_lang.get()

    def submit(self):
        self.destroy()


def chose_lang():
    return LangSelectWindow().chose_lang()


""" Точка входа """
if __name__ == "__main__":
    os.chdir(Path().absolute().parent)
    # print("Доступные языки:")
    # for i in googletrans.LANGUAGES:
    #     print(f"[{i}]: {googletrans.LANGUAGES[i]}")
    # lang = input("Перевести на: ")
    # make_translate(lang)
    # load("auto-" + lang)
    # print(get("main.json", "brightness_update", "update_brightness", "brightness_updated"))
    # print(get("about.json"))
    # print(check_differences())
    load(chose_lang())
    print(chose_lang())
