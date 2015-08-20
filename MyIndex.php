<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>GeoJson Test</title>

    <!--Mapbox-->
    <link href='https://api.tiles.mapbox.com/mapbox.js/v2.2.1/mapbox.css' rel='stylesheet' />

    <!--Bootstrap-->
    <link href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css' rel='stylesheet' />

    <!--Main Work Space-->
    <link href='css/style_blank.css' rel='stylesheet' />

    <!--Google format-->
    <link href='http://fonts.googleapis.com/css?family=Roboto' rel='stylesheet' type='text/css' />

    <!--Plugins-->
    <link href='https://api.tiles.mapbox.com/mapbox.js/plugins/leaflet-markercluster/v0.4.0/MarkerCluster.css' rel='stylesheet' />
    <link href='https://api.tiles.mapbox.com/mapbox.js/plugins/leaflet-markercluster/v0.4.0/MarkerCluster.Default.css' rel='stylesheet' />
    <link href='https://api.tiles.mapbox.com/mapbox.js/plugins/leaflet-draw/v0.2.2/leaflet.draw.css' rel='stylesheet' />
    <link href='http://makinacorpus.github.io/Leaflet.FileLayer/Font-Awesome/css/font-awesome.min.css' rel='stylesheet' />

</head>

<body>

<div class="header">
    <h1 class="header"id="tweetsYoulike">TweetsYouLike</h1>
</div>

<?php
$domain = "";
if ($_SERVER['REQUEST_METHOD'] == 'POST')
{
    $domain = $_POST['domains'];
    //echo $domain;
}

?>

<form method = "post" action = "<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
    Domain:<select name= "domains" id="domains">
        <option value = "Health" <?php if($domain == 'Health') echo 'selected';?>>Health</option>
        <option value = "Science" <?php if($domain == 'Science') echo 'selected';?>>Science</option>
        <option value = "Sports" <?php if($domain == 'Sports') echo 'selected';?>>Sports</option>
    </select>
    <input type="submit" name="submit" value="Submit">
</form>



<div id="map"></div>

<!--jQuery-->
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.0.0-alpha1/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.0.0-alpha1/jquery.js"></script>

<!--Bootstrap-->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>

<!--Main Work Space-->
<script src="js/script_blank.js"></script>

<!--Mapbox-->
<script src="https://api.tiles.mapbox.com/mapbox.js/v2.2.1/mapbox.js"></script>

<!--GeoJson Data-->
<script src="js/auto_data.js"></script>
<script src="js/www.js"></script>

<!--Plugins-->
<script src='https://api.tiles.mapbox.com/mapbox.js/plugins/leaflet-markercluster/v0.4.0/leaflet.markercluster.js'></script>
<script src='https://api.tiles.mapbox.com/mapbox.js/plugins/leaflet-draw/v0.2.2/leaflet.draw.js'></script>
<script src='http://makinacorpus.github.io/Leaflet.FileLayer/leaflet.filelayer.js'></script>
<script src='http://makinacorpus.github.io/Leaflet.FileLayer/togeojson/togeojson.js'></script>

</body>
</html>