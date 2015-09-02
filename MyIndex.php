<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>GeoJson Test</title>
    
    <!--Mapbox-->
    <link href='https://api.tiles.mapbox.com/mapbox.js/v2.2.1/mapbox.css' rel='stylesheet' />
    
    <!--Bootstrap-->
    <link href='https://maxcdn.bootstrapcdn.com/bootswatch/3.3.5/cosmo/bootstrap.min.css' rel='stylesheet' />

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

<nav class="navbar navbar-default" id="Geo-navbar">
  <div class="container-fluid">
    <div class="navbar-header">
      <a class="navbar-brand" href="https://github.com/GIS-LYL/GeoTweets">GeoTweets</a>
    </div>

    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav">
        <li class="dropdown">
            <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">Link <span class="caret"></span></a>
            <ul class="dropdown-menu" role="menu" id="Geo-domain">
                <li><a href="https://github.com/GIS-LYL">LYL</a></li>
                <li><a href="http://www.usc.edu/">USC</a></li>
                <li><a href="http://spatial.usc.edu/">Spatial Science</a></li>
            </ul>
        </li>
        <li class="dropdown">
          <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">Domain <span class="caret"></span></a>
          <ul class="dropdown-menu" role="menu" id="Geo-domain">
            <li class="active"><a href="#" id="Geo-health">Health</a></li>
            <li><a href="#" id="Geo-sports">Sports</a></li>
            <li><a href="#" id="Geo-history">History</a></li>
            <li><a href="#" id="Geo-new-domain1">new domain1</a></li>
            <li><a href="#" id="Geo-new-domain2">new domain2</a></li>
          </ul>
        </li>
        <li id="Geo-event"><a href="#">Events</a></li>
        <li id="Geo-tweetHeat"><a href="#">TweetsHeat</a></li>
        <li id="Geo-eventHeat"><a href="#">EventsHeat</a></li>
      </ul>
        <form class="navbar-form navbar-right" role="search" id="Geo-form">
            <div class="form-group">
              <input type="date" class="form-control" id="Geo-from">
              <input type="date" class="form-control" id="Geo-to">
            </div>
            <button type="button" class="btn btn-default" id="Geo-submit">Submit</button>
        </form>
    </div>
  </div>
</nav>
    
<div id = "map"></div>

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
<script src='https://api.mapbox.com/mapbox.js/plugins/leaflet-heat/v0.1.3/leaflet-heat.js'></script>
<script src="http://leaflet.github.io/Leaflet.heat/dist/leaflet-heat.js"></script>



</body>
</html>