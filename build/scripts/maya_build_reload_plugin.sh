#!/bin/bash

# Project info
NAME_PROJECT="mlunar"
PATH_PROJECT="/Users/luky/My Drive/Development/3d/Maya/LunarDev"
# Build info
VERSION_MAYA=2023
BUILD_VARIANT="Release"
COMPILER="Unix Makefiles"
# Get platform info
unamestr=$(uname)
if [[ "$unamestr" == "Darwin" ]]; then
	PLATFORM="macos"
	PLUGIN_EXTENSION=".bundle"
elif [[ "$unamestr" == "Linux" ]]; then
	PLATFORM="linux"
	PLUGIN_EXTENSION=".so"
fi
# Build paths
PATH_BUILD="$PATH_PROJECT/build"
PATH_BUILD_SCRIPTS = "$PATH_BUILD/scripts"
PATH_BUILD_MAYA="$PATH_BUILD/maya"
PATH_BUILD_MAYA_VERSION="$PATH_BUILD_MAYA/$VERSION_MAYA"
# Plugin info
PLUGIN="$NAME_PROJECT$PLUGIN_EXTENSION"
PLUGIN_BUILT="/src/maya/$PLUGIN"
PATH_PLUGIN_TARGET="$PATH_PROJECT/lunar/maya/resources/plug-ins/$PLATFORM/$VERSION_MAYA"

# Pre build - clean up
python "$PATH_PROJECT/build/scripts/maya_quit.py"

rm -rf "$PATH_BUILD_MAYA"
mkdir -p "${PATH_BUILD_MAYA_VERSION}"
cd "${PATH_BUILD_MAYA_VERSION}"

# Cmake build
cmake -DMAYA_VERSION="$VERSION_MAYA" -G "$COMPILER" ../../../
open -a maya
cmake --build . --config $BUILD_VARIANT --target all

# Post build
# python "$PATH_PROJECT/build/scripts/maya_unload_plugin.py"
# Run python script to unload script
# rm "$PATH_PLUGIN_TARGET/$PLUGIN"
cp -f "./$PLUGIN_BUILT" "$PATH_PLUGIN_TARGET"
# sleep 1
# Run load plugin
# python "$PATH_PROJECT/build/scripts/maya_load_plugin.py"
# open -a maya
