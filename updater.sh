#!/bin/bash

# This software was sourced from Just-Some-Bots/MusicBot
# https://github.com/Just-Some-Bots

# The MIT License

# Copyright (c) 2015-2019 Just-Some-Bots (https://github.com/Just-Some-Bots)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Ensure we're in the MusicBot directory
cd "$(dirname "$BASH_SOURCE")"

# Set variables for python versions. Could probably be done cleaner, but this works.
declare -A python=( ["0"]=`python -c 'import sys; version=sys.version_info[:3]; print("{0}".format(version[0]))' || { echo "no py"; }` ["1"]=`python -c 'import sys; version=sys.version_info[:3]; print("{0}".format(version[1]))' || { echo "no py"; }` ["2"]=`python -c 'import sys; version=sys.version_info[:3]; print("{0}".format(version[2]))' || { echo "no py"; }` )
declare -A python3=( ["0"]=`python3 -c 'import sys; version=sys.version_info[:3]; print("{0}".format(version[1]))' || { echo "no py3"; }` ["1"]=`python3 -c 'import sys; version=sys.version_info[:3]; print("{0}".format(version[2]))' || { echo "no py3"; }` )
PYTHON35_VERSION=`python3.5 -c 'import sys; version=sys.version_info[:3]; print("{0}".format(version[2]))' || { echo "no py35"; }`
PYTHON36_VERSION=`python3.6 -c 'import sys; version=sys.version_info[:3]; print("{0}".format(version[1]))' || { echo "no py36"; }`
PYTHON37_VERSION=`python3.7 -c 'import sys; version=sys.version_info[:3]; print("{0}".format(version[1]))' || { echo "no py37"; }`


if [ "${python[0]}" -eq "3" ]; then # Python = 3
    if [ "${python[1]}" -ge "6" ]; then # Python >= 3.6
        python updater.py
        exit
    fi
fi


if [ "${python3[0]}" -ge "6" ]; then # Python3 >= 3.6
    python3 updater.py
    exit
fi

if [ "$PYTHON35_VERSION" -ge "3" ]; then # Python3.5 > 3.5.3
    python3.5 updater.py
    exit
fi

if [ "$PYTHON36_VERSION" -eq "6" ]; then # Python3.6 = 3.6
    python3.6 updater.py
    exit
fi

if [ "$PYTHON37_VERSION" -eq "7" ]; then # Python3.7 = 3.7
    python3.7 updater.py
    exit
fi

echo "You are running an unsupported Python version."
echo "Please use a version of Python at or above 3.6.0."
