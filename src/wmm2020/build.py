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

R = Path(__file__).resolve().parent
SRCDIR = R
BINDIR = SRCDIR / "build"


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

    if not dllfn.is_file():
        dllfn = None

    return dllfn
