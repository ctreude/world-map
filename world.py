import urllib3
import json
import matplotlib.pyplot as plt
import pandas as pd

class Coordinate:
	longitude = 0
	latitude = 0
	land = False

	def __init__(self, longitude, latitude):
		self.longitude = longitude
		self.latitude = latitude
		url = 'https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=' + str(latitude) + '&lon=' + str(longitude)
		http = urllib3.PoolManager()
		request = http.request('GET', url)
		js = json.loads(request.data.decode('utf8'))
		request.release_conn()
		try:
			display_name = js["display_name"]
			self.land = True
		except:
			self.land = False

	def to_dictionary(self):
		return {"longitude":self.longitude,"latitude":self.latitude,"land":self.land}
	
	def on_land(self):
		return self.land

def coordinates_along_latitude():
	coordinates = []
	for i in range(73):
		print(i)
		for j in range(73):
			coordinates.append(Coordinate((i-36)*5, (j-36)*2.5))
	return coordinates

def plot(ocean_data, land_data):
	assert len(ocean_data) + len(land_data) > 0
	if len(ocean_data) > 0 and len(land_data) > 0:
		ocean_df = pd.DataFrame(ocean_data) 
		ax = ocean_df.plot(x="longitude", y="latitude", kind="scatter", color="lightblue")
		land_df = pd.DataFrame(land_data)
		land_df.plot(ax=ax, x="longitude", y="latitude", kind="scatter", color="black")
	elif len(ocean_data) == 0:
		land_df = pd.DataFrame(land_data)
		land_df.plot(x="longitude", y="latitude", kind="scatter", color="black")
	else:
		ocean_df = pd.DataFrame(ocean_data)
		ocean_df.plot(x="longitude", y="latitude", kind="scatter", color="lightblue")

	plt.xlabel('longitude') 
	plt.ylabel('latitude') 

	plt.xlim(-180,180)
	plt.ylim(-90,90)

	plt.show() 
	plt.savefig("out.png")

ocean_data = []
land_data = [] 
all_data = []

coordinates = coordinates_along_latitude()

for coordinate in coordinates:
	all_data.append(coordinate.to_dictionary())
	if coordinate.on_land():
		land_data.append(coordinate.to_dictionary())
	else:
		ocean_data.append(coordinate.to_dictionary())

print(pd.DataFrame(all_data))

plot(ocean_data, land_data)