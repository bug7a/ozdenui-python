@rem Bismillah
@echo off
goto :start

run_windows.bat - ozdenui v0.1 (OzdenUI: basic.js for Python)
Tests OzdenUI on this Windows computer: a new environment, the tests, then every example in its real window.
Usage: double click it, or checks\run_windows.bat. The result is written to checks\windows-result.txt.
(The lines between goto and its label are never read by cmd: a comment of any characters.)

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0

:start
cd /d "%~dp0\.."
py -m venv .venv || goto failed
.venv\Scripts\python -m pip install --upgrade pip || goto failed
.venv\Scripts\python -m pip install -e . pytest pillow || goto failed
(
    .venv\Scripts\python -m pytest tests
    .venv\Scripts\python checks\run_all.py
) > checks\windows-result.txt 2>&1
type checks\windows-result.txt
echo.
echo The result is in checks\windows-result.txt
pause
exit /b 0
:failed
echo Could not make the environment. Is Python installed? https://www.python.org/downloads/
pause
exit /b 1
