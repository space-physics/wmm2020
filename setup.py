#!/usr/bin/env python3
import sys
import site
import setuptools

# PEP517 workaround
site.ENABLE_USER_SITE = True

extensions = [
        setuptools.Extension(
                'wmm2020.wmm_cext',  # Note: Next wmm_cext.pyd inside of package wmm2020
                # define_macros=[('MAJOR_VERSION', '1')],
                # extra_compile_args=['-std=c99'],
                sources=['src/wmm2020/src/wmm_cext.c', 'src/wmm2020/src/wmm_point_sub.c',
                         'src/wmm2020/src/GeomagnetismLibrary.c'],
                include_dirs=['src/wmm2020/src/']),
    ]

try:
    setuptools.setup(ext_modules=extensions)
except (Exception, SystemError, SystemExit) as err:
    # Catch SystemExit to try installing again without C Extension
    print('Failed to build the C Extension!', file=sys.stderr)  # This will only print with "pip install -v ."
    setuptools.setup()
