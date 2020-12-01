#!/usr/bin/env python3

"""
This software was sourced from Just-Some-Bots/MusicBot
https://github.com/Just-Some-Bots

The MIT License

Copyright (c) 2015-2019 Just-Some-Bots (https://github.com/Just-Some-Bots)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from __future__ import print_function

import os
import sys
import time
import logging
import tempfile
import traceback
import subprocess

from shutil import disk_usage, rmtree
from base64 import b64decode

try:
    import pathlib
    import importlib.util
except ImportError:
    pass


class GIT(object):
    @classmethod
    def works(cls):
        try:
            return bool(subprocess.check_output("git --version", shell=True))
        except Exception:
            return False


class PIP(object):
    @classmethod
    def run(cls, command, check_output=False):
        if not cls.works():
            raise RuntimeError("Could not import pip.")

        try:
            return PIP.run_python_m(*command.split(), check_output=check_output)
        except subprocess.CalledProcessError as e:
            return e.returncode
        except Exception:
            traceback.print_exc()
            print("Error using -m method")

    @classmethod
    def run_python_m(cls, *args, **kwargs):
        check_output = kwargs.pop("check_output", False)
        check = subprocess.check_output if check_output else subprocess.check_call
        return check([sys.executable, "-m", "pip"] + list(args))

    @classmethod
    def run_pip_main(cls, *args, **kwargs):
        import pip

        args = list(args)
        check_output = kwargs.pop("check_output", False)

        if check_output:
            from io import StringIO

            out = StringIO()
            sys.stdout = out

            try:
                pip.main(args)
            except Exception:
                traceback.print_exc()
            finally:
                sys.stdout = sys.__stdout__

                out.seek(0)
                pipdata = out.read()
                out.close()

                print(pipdata)
                return pipdata
        else:
            return pip.main(args)

    @classmethod
    def run_install(cls, cmd, quiet=False, check_output=False):
        return cls.run("install %s%s" % ("-q " if quiet else "", cmd), check_output)

    @classmethod
    def run_show(cls, cmd, check_output=False):
        return cls.run("show %s" % cmd, check_output)

    @classmethod
    def works(cls):
        try:
            import pip

            return True
        except ImportError:
            return False

    # noinspection PyTypeChecker
    @classmethod
    def get_module_version(cls, mod):
        try:
            out = cls.run_show(mod, check_output=True)

            if isinstance(out, bytes):
                out = out.decode()

            datas = out.replace("\r\n", "\n").split("\n")
            expectedversion = datas[3]

            if expectedversion.startswith("Version: "):
                return expectedversion.split()[1]
            else:
                return [x.split()[1] for x in datas if x.startswith("Version: ")][0]
        except Exception:
            pass

    @classmethod
    def get_requirements(cls, file="requirements.txt"):
        from pip.req import parse_requirements

        return list(parse_requirements(file))


# Setup initial loggers

log = logging.getLogger("launcher")
log.setLevel(logging.DEBUG)

sh = logging.StreamHandler(stream=sys.stdout)
sh.setFormatter(logging.Formatter(fmt="[%(levelname)s] %(name)s: %(message)s"))

log.addHandler(sh)


def bugger_off(msg="Press enter to continue . . .", code=1):
    input(msg)
    sys.exit(code)


# TODO: all of this
def sanity_checks(optional=True):
    log.info("Starting sanity checks")
    # Required

    # Make sure we're on Python 3.5+
    req_ensure_py3()

    # Fix windows encoding
    req_ensure_encoding()

    # Make sure we're in a writeable env
    req_ensure_env()

    # Make our folders if needed
    req_ensure_folders()

    # For rewrite only
    req_check_deps()

    log.info("Required checks passed.")

    # Optional
    if not optional:
        return

    # Check disk usage
    opt_check_disk_space()

    log.info("Optional checks passed.")


def req_ensure_py3():
    log.info("Checking for Python 3.6+")

    if sys.version_info < (3, 6):
        log.warning(
            "Python 3.6+ is required. This version is %s", sys.version.split()[0]
        )
        log.warning("Attempting to locate Python 3.6...")

        pycom = None

        if sys.platform.startswith("win"):
            log.info('Trying "py -3.6"')
            try:
                subprocess.check_output('py -3.6 -c "exit()"', shell=True)
                pycom = "py -3.6"
            except Exception:

                log.info('Trying "python3"')
                try:
                    subprocess.check_output('python3 -c "exit()"', shell=True)
                    pycom = "python3"
                except Exception:
                    pass

            if pycom:
                log.info("Python 3 found.  Launching bot...")
                pyexec(pycom, "run.py")

                # I hope ^ works
                os.system("start cmd /k %s run.py" % pycom)
                sys.exit(0)

        else:
            log.info('Trying "python3.6"')
            try:
                pycom = (
                    subprocess.check_output('python3.6 -c "exit()"'.split())
                    .strip()
                    .decode()
                )
            except Exception:
                pass

            if pycom:
                log.info(
                    "\nPython 3 found.  Re-launching bot using: %s run.py\n", pycom
                )
                pyexec(pycom, "run.py")

        log.critical(
            "Could not find Python 3.6 or higher.  Please run the bot using Python 3.6"
        )
        bugger_off()


def req_check_deps():
    try:
        import discord

        if discord.version_info.major < 1:
            log.critical(
                "This version of mc-status-bot requires a newer version of discord.py (1.0+). Your version is {0}. Try running updater.py.".format(
                    discord.__version__
                )
            )
            bugger_off()
    except ImportError:
        # if we can't import discord.py, an error will be thrown later down the line anyway
        pass


def req_ensure_encoding():
    log.info("Checking console encoding")

    if (
        sys.platform.startswith("win")
        or sys.stdout.encoding.replace("-", "").lower() != "utf8"
    ):
        log.info("Setting console encoding to UTF-8")

        import io

        sys.stdout = io.TextIOWrapper(
            sys.stdout.detach(), encoding="utf8", line_buffering=True
        )
        # only slightly evil
        sys.__stdout__ = sh.stream = sys.stdout

        if os.environ.get("PYCHARM_HOSTED", None) not in (None, "0"):
            log.info("Enabling colors in pycharm pseudoconsole")
            sys.stdout.isatty = lambda: True


def req_ensure_env():
    log.info("Ensuring we're in the right environment")

    if os.environ.get("APP_ENV") != "docker" and not os.path.isdir(
        b64decode("LmdpdA==").decode("utf-8")
    ):
        log.critical(
            b64decode(
                "Qm90IHdhc24ndCBpbnN0YWxsZWQgdXNpbmcgR2l0LiBSZWluc3RhbGwgdXNpbmcgaHR0cHM6Ly9naXRodWIuY29tL0Z5c3Npb24vbWMtc3RhdHVzLWJvdCNpbnN0YWxsYXRpb24="
            ).decode("utf-8")
        )
        bugger_off()

    try:
        assert os.path.isfile("config.yml"), "config.yml file not found, run the updater to initiate setup"
        assert os.path.isfile(
            "bot.py"
        ), "Could not find bot.py"

        assert importlib.util.find_spec("bot"), "bot module is not importable"
    except AssertionError as e:
        log.critical("Failed environment check, %s", e)
        bugger_off()

    try:
        os.mkdir("statusbot-test-folder")
    except Exception:
        log.critical("Current working directory does not seem to be writable")
        log.critical("Please move the bot to a folder that is writable")
        bugger_off()
    finally:
        rmtree("statusbot-test-folder", True)

    if sys.platform.startswith("win"):
        log.info("Adding local bins/ folder to path")
        os.environ["PATH"] += ";" + os.path.abspath("bin/")
        sys.path.append(os.path.abspath("bin/"))  # might as well


def req_ensure_folders():
    pathlib.Path("logs").mkdir(exist_ok=True)
    pathlib.Path("data").mkdir(exist_ok=True)


def opt_check_disk_space(warnlimit_mb=200):
    if disk_usage(".").free < warnlimit_mb * 1024 * 2:
        log.warning(
            "Less than %sMB of free space remains on this device" % warnlimit_mb
        )


#################################################


def pyexec(pycom, *args, pycom2=None):
    pycom2 = pycom2 or pycom
    os.execlp(pycom, pycom2, *args)


def main():
    # TODO: *actual* argparsing

    if "--no-checks" not in sys.argv:
        sanity_checks()

    import asyncio

    if sys.platform == "win32":
        loop = asyncio.ProactorEventLoop()  # needed for subprocesses
        asyncio.set_event_loop(loop)

    tried_requirementstxt = False
    tryagain = True

    loops = 0
    max_wait_time = 60

    while tryagain:
        # Maybe I need to try to import stuff first, then actually import stuff
        # It'd save me a lot of pain with all that awful exception type checking

        bot = None
        try:
            from bot import ServerStatus

            bot = ServerStatus()

            sh.terminator = ""
            sh.terminator = "\n"

            bot.run()

        except SyntaxError:
            log.exception("Syntax error (this is a bug, not your fault)")
            break

        except ImportError:
            # TODO: if error module is in pip or dpy requirements...

            if not tried_requirementstxt:
                tried_requirementstxt = True

                log.exception("Error starting bot")
                log.info("Attempting to install dependencies...")

                err = PIP.run_install("--upgrade -r requirements.txt")

                if (
                    err
                ):  # TODO: add the specific error check back as not to always tell users to sudo it
                    print()
                    log.critical(
                        "You may need to %s to install dependencies."
                        % ["use sudo", "run as admin"][sys.platform.startswith("win")]
                    )
                    break
                else:
                    print()
                    log.info("Ok lets hope it worked")
                    print()
            else:
                log.exception("Unknown ImportError, exiting.")
                break

        except Exception as e:
            import discord
            if isinstance(e, discord.LoginFailure):
                log.exception("There was an error logging into Discord. Please ensure that your token is correct.")
                break

            else:
                log.exception("Error starting bot")

        finally:
            if not bot or not bot.init_ok:
                if any(sys.exc_info()):
                    # How to log this without redundant messages...
                    traceback.print_exc()
                break

            asyncio.set_event_loop(asyncio.new_event_loop())
            loops += 1

        if not bot or not bot.restart_signal:
            break

        sleeptime = min(loops * 2, max_wait_time)
        if sleeptime:
            log.info("Restarting in {} seconds...".format(loops * 2))
            time.sleep(sleeptime)

    print()
    log.info("All done.")


if __name__ == "__main__":
    main()
