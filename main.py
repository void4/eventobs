import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, get_sun
import matplotlib.pyplot as plt

lonstr, latstr = "03h15m46s", "-33d48m58s"

obj = SkyCoord(lonstr, latstr)

tstr = "2022-09-26 23:14"
t = Time(tstr)

suncoords = get_sun(t)

arr = []

sunarr = []

latrange = range(90, -91, -5)
lonrange = range(0, 361, 5)

rlonrange = range(-180, 181, 5)

for lat in latrange:
	print(lat)
	arr.append([])
	sunarr.append([])
	for lon in lonrange:
		loc = EarthLocation(lat=lat*u.deg, lon=(lon-180)*u.deg)#ignoring height
		altaz = obj.transform_to(AltAz(obstime=t, location=loc))
		alt = altaz.alt.to_value()
		arr[-1].append(alt)

		sunaltaz = suncoords.transform_to(AltAz(obstime=t, location=loc))
		sunalt = sunaltaz.alt.to_value()
		if sunalt < -18:
			sunval = 0
		elif sunalt < -12:
			sunval = 1
		elif sunalt < -6:
			sunval = 2
		else:
			sunval = 5
		sunarr[-1].append(sunval)

pimg = plt.imread("Equirectangular_projection_SW.jpg")
fig, ax = plt.subplots()
ax.imshow(pimg, extent=[-180,180,-90,90])

cs = plt.contourf(rlonrange, latrange, sunarr, alpha=0.4, levels=40, cmap="copper", antialiased=True)

# The calculated altitudes are at the corner of the corresponding pixel, so slightly inaccurate/shifted
# should interpolate
cs = plt.contour(rlonrange, latrange, arr, alpha=1.0, levels=18, cmap="RdYlGn", nchunk=18, antialiased=True)
plt.clabel(cs, inline=True, fontsize=10)

plt.title(f"Altitude of {lonstr} {latstr} (J2000) @ {tstr} UTC")
fig.set_size_inches(18.5, 10.5)
plt.xticks(range(-180, 181, 15))
plt.yticks(range(90, -91, -15))
plt.tight_layout()
plt.savefig("plot.png")
plt.show()
