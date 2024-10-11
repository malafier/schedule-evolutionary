#!/bin/sh

# Clear previously generated libraries and create new
python3 setup.py clean --all
rm -rf build evolutionary/*.so evolutionary/*.c
python setup.py build_ext --inplace