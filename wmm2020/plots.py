from matplotlib.pyplot import figure
import xarray


def plotwmm(mag: xarray.Dataset):

    fg = figure()
    ax = fg.subplots(1, 2, sharey=True)
    fg.suptitle("WMM2020  {}".format(mag.time))
    h = ax[0].contour(mag.glon, mag.glat, mag.decl, range(-90, 90 + 20, 20))
    ax[0].clabel(h, inline=True, fmt="%0.1f")
    ax[0].set_title("Magnetic Declination [degrees]")

    h = ax[1].contour(mag.glon, mag.glat, mag.incl, range(-90, 90 + 20, 20))
    ax[1].clabel(h, inline=True, fmt="%0.1f")
    ax[1].set_title("Magnetic Inclination [degrees]")

    ax[0].set_ylabel("Geographic latitude (deg)")
    for a in ax:
        a.set_xlabel("Geographic longitude (deg)")
