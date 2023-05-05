#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pathlib
import sys
import datetime
import os.path
import argparse


def add_human(staff, name, phone, str_bday):
    """
    Запросить данные о человеке.
    """
    b_day = list(map(int, str_bday.split(".")))
    date_bday = datetime.date(b_day[2], b_day[1], b_day[0])
    staff.append(
        {
            "name": name,
            "phone": phone,
            "birthday": date_bday
        }
    )

    return staff


def display_human(staff):
    """
    Отобразить список работников.
    """
    # Проверить, что список работников не пуст.
    if staff:
        # Заголовок таблицы.
        line = "+-{}-+-{}-+-{}-+-{}-+".format(
            "-" * 4,
            "-" * 30,
            "-" * 15,
            "-" * 15
        )
        print(line)
        print(
            "| {:^4} | {:^30} | {:^15} | {:^15} |".format(
                "№",
                "Фамилия и имя",
                "Телефон",
                "День рождения"
            )
        )
        print(line)

        # Вывести данные о всех сотрудниках.
        for idx, human in enumerate(staff, 1):
            print(
                f"| {idx:>4} |"
                f' {human.get("name", ""):<30} |'
                f' {human.get("phone", 0):<15} |'
                f' {human.get("birthday")}      |'
            )
            print(line)

    else:
        print("Список пуст.")


def find_human(staff, fname):
    """
    Выбрать работников с заданным стажем.
    """
    # Сформировать список людей.
    result = []
    for h in staff:
        if fname in str(h.values()):
            result.append(h)

    # Проверка на наличие записей
    if len(result) == 0:
        return print("Запись не найдена")

    # Возвратить список выбранных работников.
    return result


def json_deserial(obj):
    """
    Деериализация объектов datetime
    """
    for h in obj:
        if isinstance(h["birthday"], str):
            # print(datetime.strptime(h['birthday'], '%Y-%m-%d'))
            bday = list(map(int, h["birthday"].split("-")))
            h["birthday"] = datetime.date(bday[0], bday[1], bday[2])


def load_humans(file_name):
    """
    Загрузить всех работников из файла JSON.
    """

    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def json_serial(obj):
    """Сериализация объектов datetime"""

    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()


def save_humans(file_name, staff):
    """
    Сохранить всех работников в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(staff, fout, ensure_ascii=False, indent=4, default=json_serial)


def main(command_line=None):
    """
    Главная функция программы.
    """
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="The data file name"
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("people")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления работника.
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new worker"
    )

    add.add_argument(
        "-n",
        "--name",
        action="store",
        required=True,
        help="The worker's name"
    )

    add.add_argument(
        "-p",
        "--phone",
        type=int,
        action="store",
        help="The worker's post"
    )

    add.add_argument(
        "-bd",
        "--bday",
        action="store",
        required=True,
        help="The year of hiring"
    )

    # Создать субпарсер для отображения всех людей.
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all people"
    )

    # Создать субпарсер для поиска людей по фамилии.
    find = subparsers.add_parser(
        "find",
        parents=[file_parser],
        help="Find the people"
    )

    find.add_argument(
        "-sn",
        "--surname",
        action="store",
        required=True,
        help="Required surname"
    )

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    path = pathlib.Path.home() / args.filename

    # Загрузить всех работников из файла, если файл существует.
    is_dirty = False
    if path.exists():
        people = load_humans(path)
    else:
        people = []

    match args.command:
        # Добавить челоека.
        case "add":
            people = add_human(
                people,
                args.name,
                args.phone,
                args.bday
            )
            is_dirty = True
        # Отобразить всех людей.
        case "display":
            display_human(people)
        # Выбрать требуемых людей
        case "find":
            selected = find_human(people, args.surname)
            display_human(selected)

    # Сохранить данные в файл, если список работников был изменен.
    if is_dirty:
        save_humans(path, people)


if __name__ == "__main__":
    main()
