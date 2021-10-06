#!/usr/bin/env python3
import site
from setuptools import setup, Extension

# PEP517 workaround
site.ENABLE_USER_SITE = True


# C Extension
extensions = [
        Extension('wmm2020.wmm_ext',
                  # define_macros=[('MAJOR_VERSION', '1')],
                  # extra_compile_args=['-std=c99'],
                  sources=['src/wmm2020/src/wmm_ext.c', 'src/wmm2020/src/wmm_point_sub.c',
                           'src/wmm2020/src/GeomagnetismLibrary.c'],
                  include_dirs=['src/wmm2020/src/']),
    ]

setup(ext_modules=extensions)
