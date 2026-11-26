# Bismillah
"""hook-ozdenui.py - ozdenui v0.1 (OzdenUI: basic.js for Python)
The hook of the package for PyInstaller: the page of the window (web/: basic.js, the components, the fonts) goes into
the app. WHY: they are data files, not modules, so PyInstaller does not see them; without them the window stayed empty
and the program waited for its page ("the page is not ready yet").

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0
"""

from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files("ozdenui")
