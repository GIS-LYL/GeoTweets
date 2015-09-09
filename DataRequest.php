<?php
/*$_POST['south'] = '24.396308';
$_POST['north'] = '49.384358';
$_POST['east'] = '-66.885444';
$_POST['west'] = '-124.848974';
$_POST['startTime'] = '2015-01-01';
$_POST['endTime'] = '2016-01-01';
$_POST['domain'] = 'Science';/**/
/* Get Params from post request */
$latbounds = ['$gt' => floatval($_POST['south']), '$lt' => floatval($_POST['north'])];
$lonbounds = [];
$east = floatval($_POST['east']); $west = floatval($_POST['west']);
if ($west < $east)
    $lonbounds = ['$gt' => $west, '$lt' => $east];
else
    $lonbounds = ['$in' => ['$gt' => $west, '$lt' => $east]];
$domain = $_POST['domain'];
$period = [
    '$gt' => new MongoDate(strtotime($_POST['startTime'])),
    '$lt' => new MongoDate(strtotime($_POST['endTime']))
];
//echo json_encode($latbounds).json_encode($lonbounds);
//echo json_encode($domain);
//echo json_encode($period);
$limit = 10000;

//$curr = new DateTime();
$data = [
    'tweets' => [
        'type' => 'FeatureCollection',
        'features' => [],
        'id' => '384759234752904937267'//$now->getTimestamp()
    ],
    'events' => [
        'type' => 'FeatureCollection',
        'features' => [],
        'id' => '384759234752904937267'//$now->getTimestamp()
    ],
    'tweetsHeat' => [],
    'eventsHeat' => []
];
/* Create a connection to database */
$connection = new MongoClient();
$collection = $connection->test->twitters;
$impt_collection = $connection->test->importances;

//var_dump( $collection->findOne() );
//$query = [ 'grades' => [ '$elemMatch' => [ 'score' => [ '$gt' => 20 ] ] ] ];
$query = [
    //'created_at' => $period,
    'coordinates.latitude' => $latbounds,
    'coordinates.longitude' => $lonbounds
];
//$fields = [ '_id' => 0, 'address.zipcode' => 1 ];
$fields = ['words' => 0];
$cursor = $collection->find($query, $fields)->limit($limit);

foreach ($cursor as $doc) {
    $cur = $impt_collection->find(['id' => $doc['_id'], 'domain' => $domain]);
    if (!$cur->hasNext())
        continue;
    $tfeature = [
        'geometry' => [
            'type' => 'Point',
            'coordinates' => [$doc['coordinates']['longitude'], $doc['coordinates']['latitude']]
        ],
        'type' => 'Feature',
        'id' => $doc['id'],
        'properties' => [
            'name' => $doc['user']['name'],
            'time' => $doc['created_at'],
            'importance' => $cur->getNext()['importance'],
            'text' => $doc['text'],
            "media_urls" => $doc['media_urls'],
            'id' => $doc['id'],
            'location' => $doc['user']['location']
        ]
    ];
    array_push($data['tweets']['features'], $tfeature);
    array_push($data['tweetsHeat'], [$doc['coordinates']['latitude'], $doc['coordinates']['longitude'],  $cur->current()['importance']]);
}

/* Query on events */
$query = [
    'domain' => $domain,
    //'start_time' => $period,
    'latitude' => $latbounds,
    'longitude' => $lonbounds
];
$collection = $connection->test->events;
$cursor = $collection->find($query)->limit($limit);
foreach ($cursor as $event) {
    $efeature = [
        'geometry' => [
            'type' => 'Point',
            'coordinates' => [$event['longitude'], $event['latitude']]
        ],
        'type' => 'Feature',
        'id' => null,
        'properties' => [
            'title' => $event['title'],
            'time' => $event['start_time'],
            'description' => $event['description'],
            "url" => $event['url'],
            'id' => null,
            'venue' => $event['venue_name'],
            'location' => implode(', ', [$event['venue_address'], $event['city_name'], $event['region_name']])
        ]
    ];
    array_push($data['events']['features'], $efeature);
    array_push($data['eventsHeat'], [$event['latitude'], $event['longitude'], 1]);
}

echo json_encode($data);/*
$file = fopen('data/data.json', 'w');
fwrite($file, json_encode($data));
fclose($file);
echo 'data/data.json';/**/
/*
$geoJson = '';

echo $geoJson;
*/
?>
