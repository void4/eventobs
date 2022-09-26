import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz

import numpy as np

from PIL import Image

lon, lat = "03h15m46s", "-33d48m58s"

obj = SkyCoord(lon, lat)

t = Time("2022-09-26 23:14")

x = 0
y = 0

WHITE = [255,255,255,255]
BLACK = [0,0,0,0]

arr = []

for lat in range(89, -90, -1):
	print(lat)
	arr.append([])
	for lon in range(0,360, 1):
		rlon = lon-180
		loc = EarthLocation(lat=lat*u.deg, lon=rlon*u.deg)#ignoring height
		altaz = obj.transform_to(AltAz(obstime=t, location=loc))
		alt = altaz.alt.to_value()
		if int(alt) == 0:
			color = (0,0,0,255)
		elif alt > 0:
			color = (0,int(2.8*alt),0,128)
		else:
			color = (int(2.8*-alt),0,0,128)
		#color = WHITE if alt > 35 else BLACK
		arr[-1].append(color)

background = Image.open("Equirectangular_projection_SW.jpg").convert("RGBA")

print(background.size)

#img = Image.new("RGB", (len(arr[0]), len(arr)))
img = Image.fromarray(np.asarray(arr, dtype=np.uint8))
img = img.resize(background.size)
result = Image.alpha_composite(background, img)
result.save("result.png")
result.show()
