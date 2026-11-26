# Bismillah
"""__pyinstaller/__init__.py - ozdenui v0.1 (OzdenUI: basic.js for Python)
Where PyInstaller finds the hook of the package: the entry point "pyinstaller40" of pyproject.toml names
get_hook_dirs, so pyinstaller app.py takes the page of the window into the app without a flag.

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0
"""

import os


def get_hook_dirs():
    return [os.path.dirname(__file__)]
