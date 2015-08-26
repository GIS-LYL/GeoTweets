<?php
/* Get Params from post request */
$bounds = [
    'east' => $_POST['east'],
    'south' => $_POST['south'],
    'west' => $_POST['west'],
    'north' => $_POST['north']
];

/* Create a connection to database */
$connection = new MongoClient();
$collection = $connection->test->Twitter;

//var_dump( $collection->findOne() );
$query = [ 'grades' => [ '$elemMatch' => [ 'score' => [ '$gt' => 20 ] ] ] ];
$fields = [ '_id' => 0, 'address.zipcode' => 1 ];
$cursor = $collection->find( $query, $fields )->limit(5);

while ( $cursor->hasNext() )
{
    ?><p><?php var_dump( $cursor->getNext() ); ?></p><?php
}

$geoJson = '{
    "type": "FeatureCollection",
    "features": [{
        "geometry": {
            "type": "Point",
            "coordinates": [-72.26518, 18.579273]
        },
        "type": "Feature",
        "id": "55cd1bc05882980ff072054b",
        "properties": {
            "marker-color": "#7ec9b1",
            "name": "I am Flore H Edouard",
            "marker-symbol": "3",
            "time": "Thu Aug 13 22:35:45 +0000 2015",
            "importance": {
                "Science": 0,
                "Health": 0.2995732273553991,
                "Sports": 0
            },
            "text": "Sweat is body fat crying right??? (@ Boulevard Fitness) https://t.co/rbRHRxzqjG",
            "marker-size": "medium",
            "media_url": [],
            "id": "55cd1bc05882980ff072054b",
            "location": "Haiti Cherie"
        }
    }, {
        "geometry": {
            "type": "Point",
            "coordinates": [120.856705, 14.414455]
        },
        "type": "Feature",
        "id": "55cd1bc45882980ff072054c",
        "properties": {
            "marker-color": "#7ec9b1",
            "name": "jayzee guevarra",
            "marker-symbol": "3",
            "time": "Thu Aug 13 22:35:49 +0000 2015",
            "importance": {
                "Science": 0,
                "Health": 0.2995732273553991,
                "Sports": 0
            },
            "text": "Sweat is body fat crying right??? (@ Boulevard Fitness) https://t.co/rbRHRxzqjG",
            "marker-size": "medium",
            "media_url": [],
            "id": "55cd1bc05882980ff072054b",
            "location": "Haiti Cherie"
        }
    }],
    "id": "tweetsyoulike.c22ab257"
}';
//echo $geoJson;

?>
