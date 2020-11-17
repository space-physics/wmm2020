from pytest import approx
import xarray

import wmm2020 as wmm


def test_wmm2020():
    mag = wmm.wmm(65, 85, alt_km=0, yeardec=2012.52868852459)

    assert isinstance(mag, xarray.Dataset)

    assert mag.north.item() == approx(9216.095937998032)
    assert mag.east.item() == approx(2585.6313552791953)
    assert mag.down.item() == approx(59578.81210945489)
    assert mag.total.item() == approx(60342.82696574229)

    assert mag.incl.item() == approx(80.87285397874935)
    assert mag.decl.item() == approx(15.67178464900435)


def test_wmm2020_point():
    mag = wmm.wmm_point(65, 85, alt_km=0, yeardec=2012.52868852459)
    assert isinstance(mag, dict)

    assert mag["north"] == approx(9216.095937998032)
    assert mag["east"] == approx(2585.6313552791953)
    assert mag["down"] == approx(59578.81210945489)
    assert mag["total"] == approx(60342.82696574229)

    assert mag["incl"] == approx(80.87285397874935)
    assert mag["decl"] == approx(15.67178464900435)
