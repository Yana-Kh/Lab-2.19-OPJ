import argparse
from colorama import init, Fore, Style
from pathlib import Path

init() # Инициализация библиотеки colorama

def tree(directory, head='', tail='', level=0, colors=None):
    path = Path(directory)



    if path.is_dir():
        print(colors[level] + head + path.name + Style.RESET_ALL)

        entries = sorted(path.iterdir())

        for i, entry in enumerate(entries):
            if level == 2:
                level = -1
            if i < len(entries) - 1:
                tree(entry, f"{tail} ├──", f"{tail} │  ", level=level+1, colors=colors)
            else:
                tree(entry, f"{tail} └──", f"{tail}   ", level=level+1, colors=colors)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Display a tree of directories and files')
    parser.add_argument('directory', metavar='DIRECTORY', nargs='?', default='.', help='the directory to display')
    parser.add_argument('-c', '--colors', metavar='COLOR', nargs='+', choices=['blue', 'green', 'red'], default=['blue', 'green', 'red'], help='the colors to use for each level of the tree')

    args = parser.parse_args()

    tree(args.directory, '', '', level=0)