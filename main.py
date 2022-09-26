import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pylab as pl

from matplotlib.colors import ListedColormap

lonstr, latstr = "03h15m46s", "-33d48m58s"

obj = SkyCoord(lonstr, latstr)

tstr = "2022-09-26 23:14"
t = Time(tstr)

x = 0
y = 0

WHITE = [255,255,255,255]
BLACK = [0,0,0,0]

arr = []

latrange = range(90, -91, -5)
lonrange = range(0, 361, 5)

for lat in latrange:
	print(lat)
	arr.append([])
	for lon in lonrange:
		loc = EarthLocation(lat=lat*u.deg, lon=(lon-180)*u.deg)#ignoring height
		altaz = obj.transform_to(AltAz(obstime=t, location=loc))
		alt = altaz.alt.to_value()
		arr[-1].append(alt)

pimg = plt.imread("Equirectangular_projection_BW.jpg")
fig, ax = plt.subplots()
ax.imshow(pimg, extent=[0,360,-90,90])

cs = plt.contour(lonrange, latrange, arr, alpha=1.0, levels=18, cmap="RdYlGn", nchunk=18, antialiased=True)
plt.clabel(cs, inline=True, fontsize=10)

plt.title(f"{lonstr} {latstr} @ {tstr}")
fig.set_size_inches(18.5, 10.5)
plt.tight_layout()
plt.savefig("plot.png")
plt.show()
