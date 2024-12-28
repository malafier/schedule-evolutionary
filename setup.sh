#!/usr/bin/sh

# Clear previously generated C code and  shared objects, and create new
# Needs to be in a venv!
python3 setup.py clean --all
rm -rf build evolutionary/*.so evolutionary/*.c
python3 setup.py build_ext --inplace