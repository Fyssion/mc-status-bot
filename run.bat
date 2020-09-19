@ECHO off

REM This software was sourced from Just-Some-Bots/MusicBot
REM https://github.com/Just-Some-Bots

REM The MIT License

REM Copyright c 2015-2019 Just-Some-Bots - https://github.com/Just-Some-Bots

REM Permission is hereby granted, free of charge, to any person obtaining a copy
REM of this software and associated documentation files - the "Software" - , to deal
REM in the Software without restriction, including without limitation the rights
REM to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
REM copies of the Software, and to permit persons to whom the Software is
REM furnished to do so, subject to the following conditions:

REM The above copyright notice and this permission notice shall be included in
REM all copies or substantial portions of the Software.

REM THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
REM IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
REM FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
REM AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
REM LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
REM OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
REM THE SOFTWARE.

CHCP 65001 > NUL
CD /d "%~dp0"

SETLOCAL ENABLEEXTENSIONS
SET KEY_NAME="HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
SET VALUE_NAME=HideFileExt

FOR /F "usebackq tokens=1-3" %%A IN (`REG QUERY %KEY_NAME% /v %VALUE_NAME% 2^>nul`) DO (
    SET ValueName=%%A
    SET ValueType=%%B
    SET ValueValue=%%C
)

IF x%ValueValue:0x0=%==x%ValueValue% (
    ECHO Unhiding file extensions...
    START CMD /c REG ADD HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced /v HideFileExt /t REG_DWORD /d 0 /f
)
ENDLOCAL


IF EXIST %SYSTEMROOT%\py.exe (
    CMD /k %SYSTEMROOT%\py.exe -3 run.py
    EXIT
)

python --version > NUL 2>&1
IF %ERRORLEVEL% NEQ 0 GOTO nopython

CMD /k python run.py
GOTO end

:nopython
ECHO ERROR: Python has either not been installed or not added to your PATH.

:end
PAUSE
