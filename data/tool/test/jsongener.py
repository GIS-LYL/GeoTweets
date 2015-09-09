# Ramdomly generates data
import json, random, copy

data = {
    'tweets': {},
    'events': {},
    'tweetsHeat': [],
    'eventsHeat': []
}

tweetGeo = {
    "type": "FeatureCollection",
    "features": [],
    "id": "tweetsyoulike.c22ab257"
}

tfeature = {
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

eventGeo = {
    "type": "FeatureCollection",
    "features": [],
    "id": "tweetsyoulike.c22ab257"
}

efeature = {
    "geometry": {
        "type": "Point",
        "coordinates": [120.856705, 14.414455]
    },
    "type": "Feature",
    "id": "55cd1bc45882980ff072054c",
    "properties": {
        "name": "jayzee guevarra",
        "time": "Thu Aug 13 22:35:49 +0000 2015",
        "text": "Sweat is body fat crying right??? (@ Boulevard Fitness) https://t.co/rbRHRxzqjG",
        "media_url": [],
        "id": "55cd1bc05882980ff072054b",
        "location": "Haiti Cherie"
    }
}

for i in range(0, 100):
    tfea = copy.deepcopy(tfeature)
    tfea['properties']['importance'] = random.random()
    coordi = []
    coordi.append(tfeature['geometry']['coordinates'][1] + (random.random() - 0.5) * 10)
    coordi.append(tfeature['geometry']['coordinates'][0] + (random.random() - 0.5) * 10)
    tfea['geometry']['coordinates'][0] = coordi[1]
    tfea['geometry']['coordinates'][1] = coordi[0]
    tweetGeo['features'].append(tfea)
    coordi.append(tfea['properties']['importance'])
    data['tweetsHeat'].append(coordi)

    efea = copy.deepcopy(efeature)
    coordi = []
    coordi.append(efeature['geometry']['coordinates'][1] + (random.random() - 0.5) * 10)
    coordi.append(efeature['geometry']['coordinates'][0] + (random.random() - 0.5) * 10)
    efea['geometry']['coordinates'][0] = coordi[1]
    efea['geometry']['coordinates'][1] = coordi[0]
    eventGeo['features'].append(efea)
    coordi.append(1)
    data['eventsHeat'].append(coordi)

data['tweets'] = tweetGeo
data['events'] = eventGeo

f = open("geo.json", "w")
json.dump(data, f)
f.close()