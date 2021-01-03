# WMM2020

![Actions Status](https://github.com/space-physics/wmm2020/workflows/ci/badge.svg)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/space-physics/wmm2020.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/space-physics/wmm2020/context:python)
[![Python versions (PyPI)](https://img.shields.io/pypi/pyversions/wmm2020.svg)](https://pypi.python.org/pypi/wmm2020)
[![Downloads](http://pepy.tech/badge/wmm2020)](http://pepy.tech/project/wmm2020)


WMM2020 World Magnetic Model...in simple, object-oriented Python.
[WMM2015](https://github.com/space-physics/wmm2015) is also available.
Tested on Linux, Mac and Windows.
Most C compilers work.
At this time Visual Studio is not supported since MSVC doesn't export function symbols without additional headers,
which is typically done with something like SWIG.

![image](./src/wmm2020/tests/incldecl.png)

## Install

for the latest release from PyPi:

```sh
python -m pip install wmm2020
```

Optionally, to get the cutting-edge development version:

```sh
git clone https://github.com/space-physics/wmm2020

python -m pip install -e wmm2020
```

This Python wrapper of WMM2020 uses our build-on-run technique.
The first time you use WMM2020, you will see messages from the Meson build system and your C compiler.


## Usage

an example script

```sh
python RunWMM2020.py
```

or as a Python module:

```python
import wmm2020

mag = wmm2020.wmm(glat, glon, alt_km, yeardec)
```

## Reference

* WMM2020 [inclination map](https://www.ngdc.noaa.gov/geomag/WMM/data/WMM2020/WMM2020_I_MERC.pdf)
* WMM2020 [declination map](https://www.ngdc.noaa.gov/geomag/WMM/data/WMM2020/WMM2020_D_MERC.pdf)
