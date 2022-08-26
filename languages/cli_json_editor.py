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
    v1_selected = {
        "v1_path": None,
        "main-section": None,
        "sub-section": None
    }
    os.system('title SIMPLE lang.json EDITOR')
    while True:
        os.system("cls")
        if not v1_selected["v1_path"]:
            print("  Выберите или создайте *.json файл")
            dir_list = ["|<--|", *os.listdir(), "|+|", "|delete|"]
            for i in range(len(dir_list)):
                print(f"[{i}] {dir_list[i]}")
            v1_path = Path(dir_list[int(input("> "))])
            if v1_path.exists():
                if v1_path.is_dir():
                    os.chdir(v1_path)
                elif v1_path.is_file():
                    v1_selected["v1_path"] = v1_path
            elif str(v1_path) == "|<--|":
                os.chdir(Path.cwd().parent)
            elif str(v1_path) == "|+|":
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
                        v1_selected["v1_path"] = Path(file_name)
            elif str(v1_path) == "|delete|":
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
            with open(v1_selected["v1_path"], "r+", encoding="UTF-8") as file:
                v1_file_data = json.load(file)
            separator(f"Файл [{v1_selected['v1_path'].name}]")
            print(f"  Язык: {v1_file_data['info']['%name%']}\n"
                  f"  Язык-родитель: {v1_file_data['info']['%head%']}")
            if not v1_selected["main-section"]:
                separator()
                print("  Выберите или создайте раздел:")
                list_of_sections = ["|<--|", *v1_file_data["data"], "|+|"]
                for i in range(len(list_of_sections)):
                    print(f"[{i}] {list_of_sections[i]}")
                section = list_of_sections[int(input("> "))]
                if section == "|+|":
                    print("  Введите название для раздела")
                    section_name = input("... ")
                    if section_name != "":
                        v1_file_data["data"][section_name] = dict()
                        v1_selected["main-section"] = section_name
                elif section == "|<--|":
                    v1_selected["v1_path"] = None
                else:
                    v1_selected["main-section"] = section
            else:
                separator(f"Раздел [{v1_selected['main-section']}]")
                if not v1_selected["sub-section"]:
                    print("  Выберите под-раздел или создайте новый")
                    list_of_sub_sections = ["|<--|", *v1_file_data["data"][v1_selected["main-section"]], "|+|"]
                    for i in range(len(list_of_sub_sections)):
                        print(f"[{i}] {list_of_sub_sections[i]}")
                    sub_selection = list_of_sub_sections[int(input("> "))]
                    match sub_selection:
                        case "|+|":
                            print("  Введите название для нового подраздела")
                            sub_section_name = input("... ")
                            if sub_section_name != "":
                                v1_file_data["data"][v1_selected["main-section"]][sub_section_name] = dict()
                                v1_selected["sub-section"] = sub_section_name
                        case "|<--|":
                            v1_selected["main-section"] = None
                        case _:
                            v1_selected["sub-section"] = sub_selection
                else:
                    separator(f"Под-раздел [{v1_selected['sub-section']}]")
                    print("  Выберите что-бы изменить или добавьте новое значение")
                    list_of_elements = ["|<--|",
                                        *v1_file_data["data"]
                                        [v1_selected["main-section"]]
                                        [v1_selected["sub-section"]],
                                        "|+|"]
                    sms = v1_selected["main-section"]
                    sss = v1_selected["sub-section"]
                    for i in range(len(list_of_elements)):
                        if list_of_elements[i] in v1_file_data["data"][sms][sss]:
                            fd = ': "' + v1_file_data["data"][sms][sss][list_of_elements[i]] + '"'
                        else:
                            fd = ""
                        print(f'[{i}] '
                              f'{list_of_elements[i]}{fd}')
                    element = list_of_elements[int(input("> "))]
                    match element:
                        case "|<--|":
                            v1_selected["sub-section"] = None
                        case "|+|":
                            print("  Введите ключ для нового элемента:")
                            key = input("... ")
                            if key != "":
                                print(f"  Введите значение для элемента {key}:")
                                value = input("... ")
                                value = "\n".join(value.split(r"\n"))
                                sms = v1_selected["main-section"]
                                sss = v1_selected["sub-section"]
                                v1_file_data["data"][sms][sss][key] = value
                        case _:
                            print(f"  Введите новое значение для {element}")
                            value = input("... ")
                            value = "\n".join(value.split(r"\n"))
                            sms = v1_selected["main-section"]
                            sss = v1_selected["sub-section"]
                            v1_file_data["data"][sms][sss][element] = value
            if v1_selected["v1_path"]:
                if v1_selected["v1_path"].exists():
                    with open(v1_selected["v1_path"], "w+", encoding="UTF-8") as file:
                        json.dump(v1_file_data, file, sort_keys=True, indent=2)
                else:
                    os.system("cls")
                    separator()
                    print(f'  Ой! Кажется "{v1_selected["v1_path"]}" больше не существует.')
                    separator()
                    input("OK > ")
                    v1_selected["v1_path"] = None


def nothing(*_):
    return ""


def decompose(data, *args):
    copy_of_args = [*args]
    if args != ():
        return decompose(data[copy_of_args.pop(0)], *copy_of_args)
    return data


def cls():
    os.system("cls")


def window_title(text: str):
    os.system("title " + text)


def choose(show: list | tuple | dict,
           top_commands: dict = (),
           bottom_commands: dict = (),
           wrong_answer_command=None,
           wrong_index_command=None,
           title: str = None,
           prompt: str = "> ",):
    """
    Ask user to select one item of list by index or key

    :param show: The sheet whose element you want to select
    :param top_commands: Dictionary of keys and commands executable when selected (on top of list)
    {"text": func | method}
    :param bottom_commands: Dictionary of keys and commands executable when selected (at bottom of list)
    {"text": func | method}
    :param wrong_answer_command: Will be executed if
    the user's provided sting is not found in the provided list
    :param wrong_index_command: Will be executed if
    the user's provided index is not found in the provided list
    :param title: Text title of list
    :param prompt: Input field prefix
    :return:
    """
    if title:
        print("  " + title)
    dir_list = (*top_commands, *sorted([*show], key=lambda e: type(e) != dict), *bottom_commands)
    for i in range(len(dir_list)):
        if dir_list[i] not in show or type(show) != dict:
            pd = ""
            fd = ""
        elif type(show[dir_list[i]]) != dict:
            pd = "- "
            fd = f":"
            for line in show[dir_list[i]].split("\n"):
                fd += "\n        " + line
        else:
            pd = ""
            fd = ""
        print(f"[{i}] {pd}{dir_list[i]}{fd}")
    answer = input(prompt)
    # Если у нас число
    try:
        if dir_list[int(answer)] in top_commands:
            return top_commands[dir_list[int(answer)]]()
        elif dir_list[int(answer)] in bottom_commands:
            return bottom_commands[dir_list[int(answer)]]()
        else:
            return dir_list[int(answer)]
    # А если строчка
    except ValueError:
        if answer not in dir_list and wrong_answer_command:
            return wrong_answer_command(answer)
        elif answer in top_commands:
            return top_commands[answer]()
        elif answer in bottom_commands:
            return bottom_commands[answer]()
    except IndexError:
        if wrong_index_command:
            wrong_index_command(int(answer))
    return answer


def show_message(message, title=None):
    cls()
    separator(title)
    print("  " + message)
    separator()
    input("OK > ")


def ask_str(message, title=None, do_cls=True):
    if do_cls:
        cls()
        separator(title)
    print("  " + message)
    separator()
    return input("... ")


def askyesno(message, title=None, do_cls=True):
    if do_cls:
        cls()
        separator(title)
    print("  " + message)
    separator()
    return input("(y/n): ").lower() in ("y", "yes", "sure", "1", "да")


path = None
selected = []
file_data = {}


def file_back():
    os.chdir(Path().absolute().parent)


def file_make_new(name=None):
    cls()
    title = "Создание файла"
    new_file = {
        "info": {},
        "data": {}
    }
    for i in range(1):
        if name:
            if len(name) >= 5:
                if name[-5:] != ".json":
                    name += ".json"
            else:
                name += ".json"
        if not name:
            filename = ask_str("Назовите новый .json файл", title)
            if filename == "":
                break
            elif len(filename) < 5:
                filename += ".json"
            elif filename[-5:] != ".json":
                filename += ".json"
        elif name == "":
            break
        elif name in os.listdir():
            global path
            path = name
            break
        elif not askyesno(f'Хотите создать файл "{name}"?', title):
            break
        else:
            filename = name
        new_file["info"]["%name%"] = ask_str("Укажите полное название языка", title)
        if new_file["info"]["%name%"] == "":
            break
        new_file["info"]["%head%"] = ask_str("Какой язык использовать для недостающих строчек?\n"
                                             "  (оставьте пустым для значения по умолчанию)")
        with Path(filename).open("w+", encoding="UTF-8") as file:
            json.dump(new_file, file, sort_keys=True, indent=2)
        return filename


def file_delete(file=None):
    cls()
    if not file:
        file = choose(sorted(os.listdir(), key=lambda f: os.path.isfile(f)),
                      {"|cancel|": nothing}, {}, nothing, nothing,
                      "Что хотите удалить?")
    if bool(file):
        cls()
        if askyesno(f'Действительно хотите удалить "{file}"? (НАВСЕГДА)', "Удаление файла"):
            if os.path.isdir(file):
                os.rmdir(file)
            elif os.path.isfile(file):
                os.remove(file)


def element_make_new_section(section=None):
    for i in range(1):
        if not section:
            cls()
            element_show_info()
            section = ask_str("Введите название для раздела", do_cls=False)
            if not section:
                break
        decompose(file_data["data"], *selected)[section] = dict()
        selected.append(section)


def element_make_new_element(element=None):
    for i in range(1):
        if not element:
            cls()
            element_show_info()
            element = ask_str("Введите название для значения", do_cls=False)
            if not element:
                break
        cls()
        element_show_info()
        new_element_data = ask_str(f'Введите новое значение для "{element}"', do_cls=False)
        if new_element_data:
            decompose(file_data["data"], *selected)[element] = \
                "\n".join(new_element_data.split(r"\n"))


def element_make_new(name, text=None):
    cls()
    element_show_info()
    if not text:
        if name:
            text = 'Создать "{}" как элемент, или как раздел?'
        else:
            text = 'Создать элемент или раздел?'
    print("  " + text.format(name))
    separator()
    answ = input("(element/section): ").lower()
    if answ in ("element", "e", "элемент", "э", "value", "v"):
        element_make_new_element(name)
    elif answ in ("section", "s", "раздел", "р", "значение", "з"):
        element_make_new_section(name)
    elif answ in ("yes", "y", "sure", "да", "д", "1"):
        element_make_new(name, "Элемент или Раздел?")


def element_back():
    global path, selected
    if bool(selected):
        selected.pop(len(selected) - 1)
    else:
        path = None


def element_delete(element=None):
    cls()
    element_show_info()
    global path, selected
    if not element:
        element = choose(decompose(file_data["data"], *selected),
                         {"|cancel|": nothing}, {}, nothing, nothing,
                         "Что хотите удалить?")
    if element:
        cls()
        element_show_info()
        if askyesno(f'Действительно хотите удалить "{element}"? (НАВСЕГДА)', do_cls=False):
            decompose(file_data["data"], *selected).pop(element)


def element_show_info():
    separator(f"Файл [{path}]")
    print("  " + f"Язык: {file_data['info']['%name%']}")
    print("  " + f"Родитель: {file_data['info']['%head%']}")
    separator("/".join(selected))


file_top_choose_commands = {
    "|<--|": file_back
}
file_bottom_choose_commands = {
    "|del|": file_delete,
    "| + |": file_make_new
}
element_top_choose_commands = {
    "|<--|": element_back
}
element_bottom_choose_commands = {
    "|del|": element_delete,
    "|+value|": element_make_new_element,
    "|+section|": element_make_new_section
}


def cli_edit_v2():
    global path, selected, file_data

    window_title("SIMPLE lang.json EDITOR v.2")
    while True:
        cls()
        if not path:
            answ = choose(sorted(os.listdir(), key=lambda fm: os.path.isfile(fm)),
                          file_top_choose_commands, file_bottom_choose_commands, file_make_new, nothing,
                          "Выберите файл для редактирования или создайте новый")
            if answ:
                if os.path.isdir(answ):
                    os.chdir(answ)
                elif os.path.isfile(answ) and answ[-5:] == ".json":
                    path = answ
        else:
            with open(path, "r", encoding="UTF-8") as file:
                file_data = json.load(file)
            element_show_info()
            answ = choose(decompose(file_data["data"], *selected),
                          element_top_choose_commands,
                          element_bottom_choose_commands,
                          element_make_new,
                          nothing,
                          "Выберите элемент для редактирования или раздел для просмотра")
            if answ:
                element = decompose(file_data["data"], *selected, answ)
                if type(element) == dict:
                    selected.append(answ)
                elif type(element) == str:
                    cls()
                    element_show_info()
                    new_element_data = ask_str(f'Введите новое значение для {answ}', do_cls=False)
                    if new_element_data:
                        decompose(file_data["data"], *selected)[answ] = \
                            "\n".join(new_element_data.split(r"\n"))
            if path:
                if Path(path).exists():
                    with open(path, "w+", encoding="UTF-8") as w_file:
                        json.dump(file_data, w_file, sort_keys=True, indent=2)
                else:
                    show_message("Файл недоступен", path)
                    path = None
                    selected.clear()


if __name__ == "__main__":
    if choose((), {"V.1": cli_edit, "V.2": cli_edit_v2}, {}, title="Выберите версию приложения") == "":
        cli_edit()
