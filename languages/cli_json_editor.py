import json
import os
from pathlib import Path


def separator(title: str = None):
    if title:
        if len(title) % 2 != 0:
            title += " "
        l_s = len(title)
        print(f"-{'=' * (15 - l_s // 2)} {title} {'=' * (15 - l_s // 2)}-")
    else:
        print(f"-{'=' * 32}-")


def cli_edit():
    selected = {
        "path": None,
        "main-section": None,
        "sub-section": None
    }
    os.system('title SIMPLE lang.json EDITOR')
    while True:
        os.system("cls")
        if not selected["path"]:
            print("  Выберите или создайте *.json файл")
            dir_list = ["|<--|", *os.listdir(), "|+|", "|delete|"]
            for i in range(len(dir_list)):
                print(f"[{i}] {dir_list[i]}")
            path = Path(dir_list[int(input("> "))])
            if path.exists():
                if path.is_dir():
                    os.chdir(path)
                elif path.is_file():
                    selected["path"] = path
            elif str(path) == "|<--|":
                os.chdir(Path.cwd().parent)
            elif str(path) == "|+|":
                print('Введите "Название_файла.json, Название_языка, Идентификатор_Заглавного_Языка",\n'
                      'прямо как в примере, через ", " (запятую и пробел)')
                new_file = input("... ").split(", ")
                match new_file:
                    case file_name, lang, head:
                        with open(file_name, "w+", encoding="UTF-8") as file:
                            json.dump({
                                "info": {
                                    "%name%": lang,
                                    "%head%": head,
                                },
                                "data": {

                                }
                            }, file, sort_keys=True, indent=2)
                        selected["path"] = Path(file_name)
            elif str(path) == "|delete|":
                os.system("cls")
                print("Какой файл хотите УДАЛИТЬ?")
                dir_list = ["|cancel|", *os.listdir()]
                for i in range(len(dir_list)):
                    print(f"[{i}] {dir_list[i]}")
                current_file = dir_list[int(input("> "))]
                if current_file != "|cancel|":
                    os.system("cls")
                    print("!!! -===========- !!!\n"
                          f'  Уверены, что хотите НАВСЕГДА удалить "{current_file}"?\n'
                          '!!! -===========- !!!')
                    print("[0] НЕТ\n"
                          "[1] ДА")
                    if int(input("> ")) == 1:
                        os.remove(current_file)
        else:
            with open(selected["path"], "r+", encoding="UTF-8") as file:
                file_data = json.load(file)
            separator(f"Файл [{selected['path'].name}]")
            print(f"  Язык: {file_data['info']['%name%']}\n"
                  f"  Язык-родитель: {file_data['info']['%head%']}")
            if not selected["main-section"]:
                separator()
                print("  Выберите или создайте раздел:")
                list_of_sections = ["|<--|", *file_data["data"], "|+|"]
                for i in range(len(list_of_sections)):
                    print(f"[{i}] {list_of_sections[i]}")
                section = list_of_sections[int(input("> "))]
                if section == "|+|":
                    print("  Введите название для раздела")
                    section_name = input("... ")
                    if section_name != "":
                        file_data["data"][section_name] = dict()
                        selected["main-section"] = section_name
                elif section == "|<--|":
                    selected["path"] = None
                else:
                    selected["main-section"] = section
            else:
                separator(f"Раздел [{selected['main-section']}]")
                if not selected["sub-section"]:
                    print("  Выберите под-раздел или создайте новый")
                    list_of_sub_sections = ["|<--|", *file_data["data"][selected["main-section"]], "|+|"]
                    for i in range(len(list_of_sub_sections)):
                        print(f"[{i}] {list_of_sub_sections[i]}")
                    sub_selection = list_of_sub_sections[int(input("> "))]
                    match sub_selection:
                        case "|+|":
                            print("  Введите название для нового подраздела")
                            sub_section_name = input("... ")
                            if sub_section_name != "":
                                file_data["data"][selected["main-section"]][sub_section_name] = dict()
                                selected["sub-section"] = sub_section_name
                        case "|<--|":
                            selected["main-section"] = None
                        case _:
                            selected["sub-section"] = sub_selection
                else:
                    separator(f"Под-раздел [{selected['sub-section']}]")
                    print("  Выберите что-бы изменить или добавьте новое значение")
                    list_of_elements = ["|<--|",
                                        *file_data["data"][selected["main-section"]][selected["sub-section"]],
                                        "|+|"]
                    sms = selected["main-section"]
                    sss = selected["sub-section"]
                    for i in range(len(list_of_elements)):
                        if list_of_elements[i] in file_data["data"][sms][sss]:
                            fd = ': "' + file_data["data"][sms][sss][list_of_elements[i]] + '"'
                        else:
                            fd = ""
                        print(f'[{i}] '
                              f'{list_of_elements[i]}{fd}')
                    element = list_of_elements[int(input("> "))]
                    match element:
                        case "|<--|":
                            selected["sub-section"] = None
                        case "|+|":
                            print("  Введите ключ для нового элемента:")
                            key = input("... ")
                            if key != "":
                                print(f"  Введите значение для элемента {key}:")
                                value = input("... ")
                                value = "\n".join(value.split(r"\n"))
                                sms = selected["main-section"]
                                sss = selected["sub-section"]
                                file_data["data"][sms][sss][key] = value
                        case _:
                            print(f"  Введите новое значение для {element}")
                            value = input("... ")
                            value = "\n".join(value.split(r"\n"))
                            sms = selected["main-section"]
                            sss = selected["sub-section"]
                            file_data["data"][sms][sss][element] = value
            if selected["path"]:
                if selected["path"].exists():
                    with open(selected["path"], "w+", encoding="UTF-8") as file:
                        json.dump(file_data, file, sort_keys=True, indent=2)
                else:
                    os.system("cls")
                    separator()
                    print(f'  Ой! Кажется "{selected["path"]}" больше не существует.')
                    separator()
                    input("OK > ")
                    selected["path"] = None


if __name__ == "__main__":
    cli_edit()
