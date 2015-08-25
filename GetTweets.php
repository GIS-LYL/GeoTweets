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
$collection = $connection->test->restaurants;

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
  "features": [
    {
      "type": "Feature",
      "properties": {
        "id": "marker-icghioki2",
        "time": "2015-08-10",
        "name": "Lenard",
        "text": "fuck the world",
        "location": "CA",
        "media_url":"",
        "importance":{
            "Cuture":"0",
            "Sports":"0",
            "Economy":"0.1"
        },
        "marker-size": "medium",
        "marker-color": "#7ec9b1",
        "marker-symbol": "3"
      },
      "geometry": {
        "coordinates": [
          -118.249282,
          33.983794
        ],
        "type": "Point"
      },
      "id": "096f93dfc47a3bbb093384b1b03c6211"
    },
    {
      "type": "Feature",
      "properties": {
        "id": "marker-icghioki2",
        "time": "2015-08-10",
        "name": "Lenard",
        "text": "fuck the world",
        "location": "CA",
        "media_url":"",
        "importance":{
            "Cuture":"0",
            "Sports":"0",
            "Economy":"0.1"
        },
        "marker-size": "medium",
        "marker-color": "#7ec9b1",
        "marker-symbol": "3"
      },
      "geometry": {
        "coordinates": [
          -118.368759,
          33.945638
        ],
        "type": "Point"
      },
      "id": "415624e6791d0488c0526439d8443b77"
    },
    {
     "type": "Feature",
      "properties": {
        "id": "marker-icghioki2",
        "time": "2015-08-10",
        "name": "Lenard",
        "text": "fuck the world",
        "location": "CA",
        "media_url":"",
        "importance":{
            "Cuture":"0",
            "Sports":"0",
            "Economy":"0.1"
        },
        "marker-size": "medium",
        "marker-color": "#7ec9b1",
        "marker-symbol": "3"
      },
      "geometry": {
        "coordinates": [
          -118.31726,
          34.037297
        ],
        "type": "Point"
      },
      "id": "f781393661de78d8b7f36025535298c6"
    }
  ],
  "id": "tweetsyoulike.c22ab257"
}';
//echo $geoJson;

?>
