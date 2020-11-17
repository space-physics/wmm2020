from __future__ import annotations
import numpy as np
from pathlib import Path
import xarray
import ctypes as ct
import os

from .build import build, get_libpath

SDIR = Path(__file__).parent
BDIR = SDIR / "build"

# NOTE: must be str() for Windows, even with py37
dllfn = get_libpath(BDIR, "wmm20")
if not dllfn.is_file():
    build()
    dllfn = get_libpath(BDIR, "wmm20")
    if not dllfn.is_file():
        raise ModuleNotFoundError(f"could not find {dllfn}")

libwmm = ct.cdll.LoadLibrary(str(dllfn))


def wmm(glats: np.ndarray, glons: np.ndarray, alt_km: float, yeardec: float) -> xarray.Dataset:
    """
    wmm computes the value of the world magnetic model at grid points specified by glats and
    glons, for a single altitude value. glats and glons should be in degrees.

    glats and glons should be generated from something like np.meshgrid, so they should be
    2-D arrays.
    """

    glats = np.atleast_2d(glats).astype(np.float64)  # to coerce all else to float64
    glons = np.atleast_2d(glons).astype(np.float64)

    # the only way to check, if two 1-D arrays are passed in is to examine the values.
    # expect that lon[:,i] for all i are the same value
    # expect that lat[i,:] for all i are the same value
    assert np.allclose(np.diff(glons, axis=0), 0)
    assert np.allclose(np.diff(glats, axis=1), 0)

    assert glats.shape == glons.shape

    mag = xarray.Dataset(coords={"glat": glats[:, 0], "glon": glons[0, :]})
    north = np.empty(glats.size)
    east = np.empty(glats.size)
    down = np.empty(glats.size)
    total = np.empty(glats.size)
    decl = np.empty(glats.size)
    incl = np.empty(glats.size)

    for i, (glat, glon) in enumerate(zip(glats.ravel(), glons.ravel())):

        x = ct.c_double()
        y = ct.c_double()
        z = ct.c_double()
        T = ct.c_double()
        D = ct.c_double()
        mI = ct.c_double()

        # this hack is needed because of coding practice of WMM

        old_dir = os.getcwd()
        os.chdir(SDIR)
        ret = libwmm.wmmsub(
            ct.c_double(glat),
            ct.c_double(glon),
            ct.c_double(alt_km),
            ct.c_double(yeardec),
            ct.byref(x),
            ct.byref(y),
            ct.byref(z),
            ct.byref(T),
            ct.byref(D),
            ct.byref(mI),
        )
        os.chdir(old_dir)

        assert ret == 0

        north[i] = x.value
        east[i] = y.value
        down[i] = z.value
        total[i] = T.value
        decl[i] = D.value
        incl[i] = mI.value

    mag["north"] = (("glat", "glon"), north.reshape(glats.shape))
    mag["east"] = (("glat", "glon"), east.reshape(glats.shape))
    mag["down"] = (("glat", "glon"), down.reshape(glats.shape))
    mag["total"] = (("glat", "glon"), total.reshape(glats.shape))
    mag["incl"] = (("glat", "glon"), incl.reshape(glats.shape))
    mag["decl"] = (("glat", "glon"), decl.reshape(glats.shape))

    mag.attrs["time"] = yeardec

    return mag


def transect(glats: np.ndarray, glons: np.ndarray, alt_km: np.ndarray, yeardec: np.ndarray) -> dict:
    """
    compute a transect through the WMM

    All inputs should be either single values, indicating held constant or numpy.ndarray
    of the same size.
    """

    # get all the inputs in a dictionary and convert to numpy arrays
    inputs = {k: np.asarray(v) for k, v in vars().items()}

    # get the shape of each input element that is not one element
    szs = {k: v.shape for k, v in inputs.items() if v.size > 1}

    # check if each in sz ar the same shape, if they all have the same size, this
    # will be true.
    # this will raise a TypeError if the number of dimensions are different
    # this will raise an AssertionError if the dimensions are the same, but the shapes are different
    assert np.allclose(np.diff(np.asarray([v for v in szs.values()]), axis=0), 0)

    # since they are the same, pick the first and save
    if len(szs) > 0:
        sz = list(szs.values())[0]
    else:
        # if all inputs are single value, we end up here
        sz = ()

    # reformat the inputs to have all the same shape
    ref_input = {k: v if v.size > 1 else np.ones(sz) * v for k, v in inputs.items()}

    # create output arrays
    north = np.empty(sz)
    east = np.empty(sz)
    down = np.empty(sz)
    total = np.empty(sz)
    decl = np.empty(sz)
    incl = np.empty(sz)

    for i, (_lat, _lon, _alt, _year) in enumerate(zip(*[v.ravel() for v in ref_input.values()])):

        x = ct.c_double()
        y = ct.c_double()
        z = ct.c_double()
        T = ct.c_double()
        D = ct.c_double()
        mI = ct.c_double()

        # this hack is needed because of coding practice of WMM

        old_dir = os.getcwd()
        os.chdir(SDIR)
        ret = libwmm.wmmsub(
            ct.c_double(_lat),
            ct.c_double(_lon),
            ct.c_double(_alt),
            ct.c_double(_year),
            ct.byref(x),
            ct.byref(y),
            ct.byref(z),
            ct.byref(T),
            ct.byref(D),
            ct.byref(mI),
        )
        os.chdir(old_dir)

        assert ret == 0

        north[i] = x.value
        east[i] = y.value
        down[i] = z.value
        total[i] = T.value
        decl[i] = D.value
        incl[i] = mI.value

    rd = {
        "north": north[()],
        "east": east[()],
        "down": down[()],
        "total": total[()],
        "decl": decl[()],
        "incl": incl[()],
    }

    return rd


def wmm_point(glat: float, glon: float, alt_km: float, yeardec: float) -> dict[str, float]:
    """
    wmm_unique computes the value of the world magnetic model at a specific unique points specified by glat,
    glon, and a altitude value. glat and glon should be in degrees.

    It is meant to be faster than `wmm` and `transect` to retrieve one single value.
    """

    if isinstance(glat, int):
        glat = float(glat)
    if isinstance(glon, int):
        glon = float(glon)
    if isinstance(alt_km, int):
        alt_km = float(alt_km)

    assert isinstance(glat, float)
    assert isinstance(glon, float)

    mag = {"glat": glat, "glon": glon}

    x = ct.c_double()
    y = ct.c_double()
    z = ct.c_double()
    T = ct.c_double()
    D = ct.c_double()
    mI = ct.c_double()

    # this hack is needed because of coding practice of WMM

    old_dir = os.getcwd()
    os.chdir(SDIR)
    ret = libwmm.wmmsub(
        ct.c_double(glat),
        ct.c_double(glon),
        ct.c_double(alt_km),
        ct.c_double(yeardec),
        ct.byref(x),
        ct.byref(y),
        ct.byref(z),
        ct.byref(T),
        ct.byref(D),
        ct.byref(mI),
    )
    os.chdir(old_dir)

    assert ret == 0

    mag["north"] = x.value
    mag["east"] = y.value
    mag["down"] = z.value
    mag["total"] = T.value
    mag["incl"] = mI.value
    mag["decl"] = D.value

    mag["time"] = yeardec

    return mag
