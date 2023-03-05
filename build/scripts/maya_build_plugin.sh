#!/bin/bash

# can't use python ./python_script.py since the __file__ variable will return a path with
# /path/./python_script.py so we cd into the script dir first.
cd ./build/scripts/
python maya_build_plugin.py
