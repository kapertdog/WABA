# -*- coding: utf-8 -*-
"""
    Менеджер языковых пакетов
"""
import json
import os
import googletrans
from pathlib import Path

# TODO:
#  Выбор языка,
#  Поддержка смены языка в реальном времени,
#  Проверка целостности перевода,
#  Импорт переводов из файла,
#  Стиль и удобная генерация значений для разработки,
#  Возможность интернет-перевода если перевод отсутствует

""" Заглавные переменные """
current_lang = {}
default_lang = {}
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


def _load(file_path: Path):
    with file_path.open("r", encoding="UTF-8") as file:
        return json.load(file)


def load(lang_name: str, printing: bool = True):
    if printing:
        print(f"- Loading {lang_name} lang -")
    global current_lang, default_lang
    cashed_langs_path = Path(os.getenv("APPDATA", ""), "waba", "cashed", "languages", lang_name)

    if default_lang == {}:
        for file_name in os.listdir(Path("languages", "defaults")):
            default_lang[file_name] = _load(Path("languages", "defaults", file_name))
        if printing:
            print(f" default lang loaded")
    current_lang.clear()

    if cashed_langs_path.exists():
        path = cashed_langs_path
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
    return _check(default_lang["main.json"]["data"], current_lang["main.json"]["data"])


def info(file: str, lang: str = None):
    fl = dict()
    if not lang and Path(file).exists():
        fl = _load(Path(lang, file))
    elif Path("languages", "data", lang, file).exists():
        fl = _load(Path("languages", "data", lang, file))
    ...


def import_lang(directory: Path):
    ...


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
    new_lang_pack = dict()
    for file in os.listdir(def_path):
        with Path(def_path, file).open("r+", encoding="UTF-8") as r_file:
            new_lang_pack[file] = json.load(r_file)

    if not out_path.exists():
        os.makedirs(out_path)

    for file in new_lang_pack:
        new_lang_pack[file]["info"]["%head%"] = "ru"
        new_lang_pack[file]["info"]["%name%"] = googletrans.LANGUAGES[lang_to]
        new_lang_pack[file]["data"] = _translate(new_lang_pack[file]["data"], "ru", lang_to)
        with Path(out_path, file).open("w+", encoding="UTF-8") as w_file:
            json.dump(new_lang_pack[file], w_file, sort_keys=True, indent=2)


""" Обработка запросов """


def get(file, section=None, sub_section=None, element=None):
    if not section:
        if file in current_lang:
            return current_lang[file]
        elif file in default_lang:
            return default_lang[file]
    else:
        try:
            return current_lang[file]["data"][section][sub_section][element]
        except KeyError:
            return default_lang[file]["data"][section][sub_section][element]


""" Инструменты для разработки """

""" Точка входа """
if __name__ == "__main__":
    ...
    # cli_edit()
    # os.chdir(Path().absolute().parent)
    # make_translate("uk")
    # load("auto-en")
    # print(get("main.json", "brightness_update", "update_brightness", "brightness_updated"))
    # print(get("about.json"))
    # print(check_differences())
