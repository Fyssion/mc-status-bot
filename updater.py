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

import os
import subprocess
import sys
import yaml


def y_n(q):
    while True:
        ri = input("{} (y/n): ".format(q))
        if ri.lower() in ["yes", "y"]:
            return True
        elif ri.lower() in ["no", "n"]:
            return False


def update_deps():
    print("Attempting to update dependencies...")

    try:
        subprocess.check_call(
            '"{}" -m pip install --no-warn-script-location --user -U -r requirements.txt'.format(
                sys.executable
            ),
            shell=True,
        )
    except subprocess.CalledProcessError:
        raise OSError(
            "Could not update dependencies. You will need to run '\"{0}\" -m pip install -U -r requirements.txt' yourself.".format(
                sys.executable
            )
        )


def get_info(question, *, default=None, optional=True):
    default_text = f" [{default}]" if default else "[]"
    default_text = default if optional else ""

    while True:
        result = input(f"{question}{default_text}: ")
        if not result and optional:
            return default

        if not optional and not result:
            continue

        else:
            break
    return result


def run_setup():
    # option: (description, optional/default)
    options = {
        "bot-token": ("Enter the token for the bot", False),
        "prefix": ("Enter the prefix for the bot", ";"),
        "server-ip": ("Enter the minecraft server ip to display status for", False),
        "maintenance-mode-detection": (
            "If you want maintenance mode detection, enter the text to look for in the MOTD or press enter to disable it",
            None,
        ),
    }
    formatted = ", ".join(options.keys())

    config_exists = os.path.isfile("config.yml")

    if config_exists:
        with open("config.yml", "r") as f:
            current_config = yaml.safe_load(f)

        missing_opts = set(options.keys()) - set(current_config.keys())

        if missing_opts:
            joined = ", ".join(missing_opts)
            print(f"There are missing options in your config file: {joined}")
            set_to_default = y_n("Automatically set these options to default?")

            if set_to_default:
                for opt in missing_opts:
                    desc, default = options[opt]
                    current_config[opt] = default

            else:
                for opt in missing_opts:
                    desc, default = options[opt]
                    optional = False if default is False else True
                    result = get_info(desc, default=default, optional=optional)

                    current_config[opt] = result

            with open("config.yml", "w") as f:
                yaml.dump(current_config, f)

        change = y_n("Change info in config file?")

        if change:
            while True:
                while True:
                    to_change = get_info(
                        f"Options: {formatted}\nEnter option to change", optional=False
                    )
                    to_change = to_change.lower()

                    if to_change in options:
                        break

                change_to = get_info(f"Enter new value for {to_change}", optional=False)

                current_config[to_change] = change_to

                again = y_n("Change another option?")

                if not again:
                    break

            with open("config.yml", "w") as f:
                yaml.dump(current_config, f)

            print("Changed options.")

        return

    print("Config file not found, initiating setup...")

    config = {}

    for option, (desc, default) in options.items():
        optional = False if default is False else True
        result = get_info(desc, default=default, optional=optional)

        config[option] = result

    with open("config.yml", "w") as f:
        yaml.dump(config, f)

    print("Setup complete.")


def main():
    print("Starting...")

    # Make sure that we're in a Git repository
    if not os.path.isdir(".git"):
        raise EnvironmentError("This isn't a Git repository.")

    # Make sure that we can actually use Git on the command line
    # because some people install Git Bash without allowing access to Windows CMD
    try:
        subprocess.check_call("git --version", shell=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        raise EnvironmentError(
            "Couldn't use Git on the CLI. You will need to run 'git pull' yourself."
        )

    print("Passed Git checks...")

    # Check that the current working directory is clean
    sp = subprocess.check_output(
        "git status --porcelain", shell=True, universal_newlines=True
    )
    if sp:
        ohno = y_n(
            "You have modified files that are tracked by Git (e.g the bot's source files).\n"
            "Should we try resetting the repo? You will lose local modifications."
        )
        if ohno:
            try:
                subprocess.check_call("git reset --hard", shell=True)
            except subprocess.CalledProcessError:
                raise OSError("Could not reset the directory to a clean state.")
        else:
            wowee = y_n(
                "OK, skipping bot update. Do you still want to update dependencies?"
            )
            if wowee:
                update_deps()

            run_setup()
            return

    print("Checking if we need to update the bot...")

    try:
        subprocess.check_call("git pull", shell=True)
    except subprocess.CalledProcessError:
        raise OSError(
            "Could not update the bot. You will need to run 'git pull' yourself."
        )

    update_deps()
    run_setup()

    print("Done. You may now run the bot.")


if __name__ == "__main__":
    main()
