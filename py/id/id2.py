#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import pathlib
from colorama import init, Fore, Style

init() # Инициализация библиотеки colorama


def tree(directory, head='', tail='', level=0, colors=None):

    path = pathlib.Path(directory)

    if colors is None:
        colors = [Fore.LIGHTYELLOW_EX, Fore.YELLOW, Fore.MAGENTA,Fore.LIGHTBLUE_EX]
    # Определение цветов для раскраски

    if path.is_dir():
        print(f"{colors[level]}{head}{path.name}{Style.RESET_ALL}")

        entries = sorted(path.iterdir())
        for i, entry in enumerate(entries):
            if level == 3:
                level = -1
            if i < len(entries) - 1:
                tree(entry, f"{tail} ├──", f"{tail} │  ", level=level + 1, colors=colors)
            else:
                tree(entry, f"{tail} └──", f"{tail}   ", level=level + 1, colors=colors)


def main():
    parser = argparse.ArgumentParser(add_help=False)
    # Добавление аргумента для пути к каталогу, который не является обязательным
    # Если он не указан, то выводится текущий рабочий каталог
    parser.add_argument(
        "directory",
        type=pathlib.Path,
        default=pathlib.Path.cwd(),
        help="Каталог для отображения (по умолчанию: текущий каталог)")


    args = parser.parse_args()
    tree(args.directory, '', '', level=0)


if __name__ == "__main__":
    main()
