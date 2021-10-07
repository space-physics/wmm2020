"""
A generic, clean way to build C/C++/Fortran code "build on run"

Michael Hirsch, Ph.D.
https://www.scivision.dev
"""
import shutil
from pathlib import Path
import importlib.resources
import subprocess
import sys
import os
import ctypes as ct

from .this_path import SDIR


__all__ = ['build', 'get_libpath', 'SDIR', 'libwmm',
           'wmmsub']


def build():
    """
    attempt to build using CMake
    """
    exe = shutil.which("ctest")
    if not exe:
        raise FileNotFoundError("CMake not available")

    with importlib.resources.path(__package__, "setup.cmake") as file:
        subprocess.check_call([exe, "-S", str(file), "-VV"])


def get_libpath(bin_dir: Path, stem: str) -> Path:
    if sys.platform in ("win32", "cygwin"):
        dllfn = bin_dir / ("lib" + stem + ".dll")
    elif sys.platform == "linux":
        dllfn = bin_dir / ("lib" + stem + ".so")
    elif sys.platform == "darwin":
        dllfn = bin_dir / ("lib" + stem + ".dylib")

    return dllfn


# Build and load the dll
libwmm = None


def load_wmm():
    """Run the build commands and load the library. The user may want to import this module without building."""
    global libwmm

    if libwmm is None:
        BDIR = SDIR / "build"

        # NOTE: must be str() for Windows, even with py37
        dllfn = get_libpath(BDIR, "wmm20")
        if not dllfn.is_file():
            build()
            dllfn = get_libpath(BDIR, "wmm20")
            if not dllfn.is_file():
                raise ModuleNotFoundError(f"could not find {dllfn}")

        libwmm = ct.cdll.LoadLibrary(str(dllfn))


def wmmsub(geolatitude, geolongitude, HeightAboveEllipsoid, yeardecimal, wmm_filename=None):
    # Load the library. This may also build the library the first time.
    load_wmm()

    # Check WMM filename argument
    if wmm_filename is None:
        wmm_filename = SDIR.joinpath('WMM.COF')

    x = ct.c_double()
    y = ct.c_double()
    z = ct.c_double()
    T = ct.c_double()
    D = ct.c_double()
    mI = ct.c_double()

    old_dir = os.getcwd()
    os.chdir(os.path.dirname(wmm_filename))
    ret = libwmm.wmmsub(
        ct.c_double(geolatitude),
        ct.c_double(geolongitude),
        ct.c_double(HeightAboveEllipsoid),
        ct.c_double(yeardecimal),
        ct.byref(x),
        ct.byref(y),
        ct.byref(z),
        ct.byref(T),
        ct.byref(D),
        ct.byref(mI),
    )
    os.chdir(old_dir)

    # Check for error
    if ret != 0:
        raise FileNotFoundError("WMM.COF not found.")  # FileNotFound seems to be the only condition for error

    return x.value, y.value, z.value, T.value, D.value, mI.value
