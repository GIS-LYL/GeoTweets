import json, random, copy

geojson = {
    "type": "FeatureCollection",
    "features": [],
    "id": "tweetsyoulike.c22ab257"
}

feature = {
    "geometry": {
        "type": "Point",
        "coordinates": [120.856705, 14.414455]
    },
    "type": "Feature",
    "id": "55cd1bc45882980ff072054c",
    "properties": {
        "name": "jayzee guevarra",
        "time": "Thu Aug 13 22:35:49 +0000 2015",
        "importance": 0.2995732273553991,
        "text": "Sweat is body fat crying right??? (@ Boulevard Fitness) https://t.co/rbRHRxzqjG",
        "media_url": [],
        "id": "55cd1bc05882980ff072054b",
        "location": "Haiti Cherie"
    }
}

for i in range(0, 100):
	fea = copy.deepcopy(feature)
	fea['properties']['importance'] = random.random()
	fea['geometry']['coordinates'][0] = feature['geometry']['coordinates'][0] + (random.random() - 0.5) * 10
	fea['geometry']['coordinates'][1] = feature['geometry']['coordinates'][1] + (random.random() - 0.5) * 10
	geojson['features'].append(fea)

f = open("geo.json", "w")
json.dump(geojson, f)
f.close()