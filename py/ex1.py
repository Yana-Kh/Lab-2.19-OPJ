#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib
import collections

# Пример 1.Подсчет файлов
if __name__ == "__main__":
    print(collections.Counter(p.suffix for p in pathlib.Path.cwd().iterdir()))