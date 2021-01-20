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
    default_text = f" [{default}]" if default else " []"
    default_text = default_text if optional else ""

    while True:
        result = input(f"{question}{default_text}: ")
        if not result and optional:
            return default

        if not optional and not result:
            continue

        else:
            break
    return result


class ConfigOption:
    def __init__(self, name, help, *, default=None, optional=True):
        self.name = name
        self.help = help

        if default and not optional:
            raise ValueError("this option is optional yet a default has been set")

        self.default = default
        self.optional = optional

    def prompt(self):
        result = get_info(self.help, default=self.default, optional=self.optional)
        return result


class BotToken(ConfigOption):
    def __init__(self):
        super().__init__("bot-token", "Enter the token for the bot", optional=False)

    def prompt(self):
        description = self.help + (
            ".\nYou can get the bot's token from the bot application. "
            "To learn how to create a bot application, visit https://discordpy.readthedocs.io/en/latest/discord.html"
        )
        result = get_info(description, default=self.default, optional=self.optional)
        return result


class Prefix(ConfigOption):
    def __init__(self):
        super().__init__("prefix", "Enter the prefix for the bot", default=";")


class ServerType(ConfigOption):
    def __init__(self):
        super().__init__(
            "server-type",
            "Enter the type of Minecraft server (Java or Bedrock)",
            default="java",
        )

    def prompt(self):
        while True:
            result = get_info(self.help, default=self.default, optional=self.optional)

            result = result.lower()

            if result in ["java", "bedrock"]:
                break

            print("Please enter either Java or Bedrock.")

        return result


class ServerIP(ConfigOption):
    def __init__(self):
        super().__init__(
            "server-ip",
            "Enter the Minecraft server ip to display status for",
            optional=False,
        )


class RefreshRate(ConfigOption):
    def __init__(self):
        super().__init__(
            "refresh-rate",
            "Enter the amount of seconds to wait in between status refreshes",
            default=60,
        )

    def prompt(self):
        while True:
            result = get_info(self.help, default=self.default, optional=self.optional)

            try:
                result = int(result)

            except ValueError:
                continue

            if result >= 30:
                break

            print("Seconds must be 30 or higher. This is due to Discord's ratelimit on changing statuses.")

        return result


class MaintenceModeDetection(ConfigOption):
    def __init__(self):
        super().__init__(
            "maintenance-mode-detection",
            "Enter the text to look for in the MOTD",
            default=None,
        )

    def prompt(self):
        enable = y_n(
            "Would you like to enable maintenance mode detection? "
            "This will allow you to specify a substring to search for in the Minecraft server's MOTD. "
            "If the substring is found, the bot's status is set to maintenance mode "
            "(DND presence with a maintenance mode message)."
        )

        if not enable:
            return None

        result = get_info(self.help, optional=False)
        return result


OPTIONS = (BotToken(), Prefix(), ServerType(), ServerIP(), RefreshRate(), MaintenceModeDetection())


def get_option(key):
    for option in OPTIONS:
        if option.name == key:
            return option
    return None


def ensure_config_keys(config):
    import yaml

    all_keys = [o.name for o in OPTIONS]

    missing_opts = set(all_keys) - set(config.keys())

    if missing_opts:
        joined = ", ".join(missing_opts)
        print(f"There are missing options in your config file: {joined}")
        set_to_default = y_n(
            "Automatically set these options to default? You can come back and change these later."
        )

        if set_to_default:
            for opt in missing_opts:
                option = get_option(opt)
                config[opt] = option.default

        else:
            for opt in missing_opts:
                option = get_option(opt)
                result = option.prompt()
                config[opt] = result

        with open("config.yml", "w") as f:
            yaml.dump(config, f)

        print("Successfully updated config")

    else:
        print("Config is up-to-date")


def run_config_adjustments(all_keys, formatted):
    import yaml

    with open("config.yml", "r") as f:
        current_config = yaml.safe_load(f)

    ensure_config_keys(current_config)

    change = y_n("Change info in config file?")

    view_more = "View more about each option here: https://github.com/Fyssion/mc-status-bot#setup-details"

    if not change:
        return

    while True:
        while True:
            to_change = get_info(
                f"Options: {formatted}\n{view_more}\nEnter option to change",
                optional=False,
            )
            to_change = to_change.lower()

            if to_change in all_keys:
                break

        option = get_option(to_change)
        change_to = option.prompt()
        current_config[to_change] = change_to

        again = y_n("Change another option?")
        if not again:
            break

    with open("config.yml", "w") as f:
        yaml.dump(current_config, f)

    print("Successfully updated your config")


def run_setup():
    loops = 0

    while loops < 2:
        try:
            import yaml

            break

        except ImportError:
            print("Oh no! PyYAML is not installed. Trying to fix...")
            loops += 1
            update_deps()

            if loops >= 2:
                raise OSError("Could not install PyYAML. Try installing it manually.")

    all_keys = [o.name for o in OPTIONS]
    formatted = ", ".join(all_keys)

    config_exists = os.path.isfile("config.yml")

    if config_exists:
        run_config_adjustments(all_keys, formatted)

    else:
        print("Config file not found, initiating setup...")

        config = {}

        for option in OPTIONS:
            result = option.prompt()
            config[option.name] = result

        with open("config.yml", "w") as f:
            yaml.dump(config, f)

        print("Successfully created and setup config")


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
            print("Done. You may now run the bot.")
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
