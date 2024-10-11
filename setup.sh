#!/bin/sh

# Clear previously generated libraries and create new
# Needs to be in venv!!!
python3 setup.py clean --all
rm -rf build evolutionary/*.so evolutionary/*.c
python3 setup.py build_ext --inplace