var d = document.getElementById('domains').value;

$(document).ready(function(){

// Mapbox API    
L.mapbox.accessToken = 'pk.eyJ1IjoidHdlZXRzeW91bGlrZSIsImEiOiI1NDU3MjQxNjRhMWQwMGFlNjY5NGM2ODZjYjgwMWU0NyJ9.73PZ0OMKufVTFYd798HZmg';

//load the map and the tileLayers
var map = L.mapbox.map('map', 'tweetsyoulike.mpo7h6lm',{
        minzoom: 2,
        maxzoom: 14,
       
    });

    L.control.layers({
        'Streets':L.mapbox.tileLayer('mapbox.streets').addTo(map),
        'Light':L.mapbox.tileLayer('mapbox.light'),
        'Dark':L.mapbox.tileLayer('mapbox.dark'),
        'Satellite':L.mapbox.tileLayer('mapbox.satellite'),
        'Comic':L.mapbox.tileLayer('mapbox.comic'),
        'Outdoors':L.mapbox.tileLayer('mapbox.outdoors'),
        'Pirates':L.mapbox.tileLayer('mapbox.pirates'),
        'High Contrast':L.mapbox.tileLayer('mapbox.high-contrast')     
    }).addTo(map);

map.on('moveend',getBounds);

function getBounds(e)
{
    var bounds = map.getBounds();
    var boundsObject = {
        west: bounds.getWest(),
        south: bounds.getSouth(),
        east: bounds.getEast(),
        north: bounds.getNorth()
    };

    $.ajax({
        type:'post',
        url:'GetTweets.php',
        dataType:'json',
        data: boundsObject,
        success:function(data){
            printDataToMap(data)
        },
        error:function(XMLHttpRequest, textStatus, errorThrown){
            alert(errorThrown);
        }
    });
}

    function printDataToMap(data){
    function makeGroup(tweets, domain)
    {
        var f1 = new Array();

        for(var i = 0; i <= 9; i++)
            f1.push({"type":"FeatureCollection","features":[]});

        for (var i = 0; i < tweets.features.length; i++)
        {
            var obj = tweets.features[i];
            var impor =  obj.properties.importance[domain];
            f1[parseInt(impor * 10)].features.push(obj);
        }
        return f1;
    };

    var color1 = [
        'red',
        '#114b29',
        '#166437',
        '#1c7d45',
        '#229653',
        '#93d6af',
        '#27af61',
        '#2dc86f',
        '#33e17d'
    ];
    var clusterGroups = [];
    for(var i = 0; i <= 9; i++)
        clusterGroups[i] = new L.MarkerClusterGroup({
            iconCreateFunction:function(cluster){
                return L.mapbox.marker.icon({
                    'marker-symbol':"marker-stroked",
                    'marker-color':color1[i-1],
                    opacity:0.5
                });
            }
        });
    var exam = makeGroup(test,"Health");
    for(var i = 0; i <= 9; i++)
    {
        if(i > 6)
        break;
        var tweets = exam[i];
        var geoJsonLayerX = L.mapbox.featureLayer();

        geoJsonLayerX.setGeoJSON(tweets).addTo(clusterGroups[i]);
        geoJsonLayerX.eachLayer(function(locale){
            var prop = locale.feature.properties;
            var impor = prop.importance;
            var popup = '<h1>' + prop.name + '</h1>' + '<h2>' + prop.location + '</h2>' + '<h2>' + prop.time + '</h2>' +
                '<h2>' + prop.text + '</h2>';
            if(d == 'Science')
                popup += d + ':' + '<h2>' + prop.importance.Science + '</h2>';
            else if(d == 'Sports')
                popup += d + ':' + '<h2>' + prop.importance.Sports + '</h2>';
            else if(d == 'Health')
                popup += d + ':' + '<h2>' + prop.importance.Health + '</h2>';
            locale.on('click',function(e){
                map.panTo(locale.getLatLng());
            });
            locale.bindPopup(popup);
            locale.setIcon(L.mapbox.marker.icon({
                'marker-color':giveMeColor('Health',impor),
                'marker-symbol':'circle-stroked',
                'marker-size':giveMeSize('Health',impor)
            }));

        });

        map.addLayer(clusterGroups[i]);


    }
    }
//ClusterLayers and GeoJson    
//var clusterGroup = new L.MarkerClusterGroup();

    /*.eachLayer(function(locale){
        var prop = locale.feature.properties;
        var impor = prop.importance;
        var popup = '<h1>' + prop.name + '</h1>' + '<h2>' + prop.location + '</h2>' + '<h2>' + prop.time + '</h2>' +
            '<h2>' + prop.text + '</h2>';
        if(d == 'Science')
            popup += d + ':' + '<h2>' + prop.importance.Science + '</h2>';
        else if(d == 'Sports')
            popup += d + ':' + '<h2>' + prop.importance.Sports + '</h2>';
        else if(d == 'Health')
            popup += d + ':' + '<h2>' + prop.importance.Health + '</h2>';
        locale.on('click',function(e){
            map.panTo(locale.getLatLng());
        });
        locale.bindPopup(popup);
        locale.setIcon(L.mapbox.marker.icon({
            'marker-color':giveMeColor(d,impor),
            'marker-symbol':'circle-stroked',
            'marker-size':giveMeSize(d,impor)
        }))


    });*/
    
    //map.addLayer(clusterGroup);

//GeoJson2    
/*var clusterGroup2 = new L.MarkerClusterGroup();
    
var geoJsonLayer2 = L.mapbox.featureLayer();
    
    geoJsonLayer2.setGeoJSON(www).addTo(clusterGroup2);
    
    geoJsonLayer2.eachLayer(function(locale){
        var prop = locale.feature.properties;
        var popup = '<h1>'+ prop.type +'</h1>'+'<h2>'+prop.place+'</h2>';
        locale.on('click',function(e){
            map.panTo(locale.getLatLng());
        });
        locale.bindPopup(popup);
    });
    
    map.addLayer(clusterGroup2);*/

    
//VectorLayers and Draw Function
var drawnItems = new L.FeatureGroup();

    map.addLayer(drawnItems);
    
var drawControl = new L.Control.Draw({
    edit:{
        featureGroup:drawnItems
    },
    position:'topleft',
});

    map.addControl(drawControl);
    
    map.on('draw:created',function(e){
    var type = e.layerType,
        layer = e.layer;
    map.addLayer(layer);
});

    
//FileLayers and load files function
var style = {color:'red', opacity: 1.0, fillOpacity: 1.0, weight: 2, clickable: false,};
    
    L.Control.FileLayerLoad.LABEL = '<i class="fa fa-folder-open"></i>';
    
    L.Control.fileLayerLoad({
                position:'topright',
                fitBounds: true,
                layerOptions: {
                    style: style,
                    pointToLayer: function (data, latlng) {
                            return L.circleMarker(latlng, {style: style});
                           }},
        }).addTo(map);
});


//show the data on the map
function showSomething(feature,layer){
    layer.bindPopup("<h1>Hi! This is the map section</h1><p>"+feature.properties.title+"</p><p>"+feature.properties.description+"</p>");
}

//colors of gradient by the importance of the data
function giveMeColor(domain, impor)
{
    var color = [
        '#0b321b',
        '#114b29',
        '#166437',
        '#1c7d45',
        '#229653',
        '#93d6af',
        '#27af61',
        '#2dc86f',
        '#33e17d',
        '#39fb8b',
        '#94fdc0'
    ];
    switch (domain)
    {
        case 'Science':
            if(impor.Science > 1)
                return color[10];
            else
                return color[parseInt(parseInt(impor.Science * 100) / 10)];
        case 'Health':
            if(impor.Health > 1)
                return color[10];
            else
            return color[parseInt(parseInt(impor.Health * 100) / 10)];
        case 'Sports':
            if(impor.Sports > 1)
                return color[10];
            else
            return color[parseInt(parseInt(impor.Sports * 100) / 10)];
    }
}

//size of gradient by the importance of the data
function giveMeSize(domain , impor)
{
    var size = [
        'small',
        'medium',
        'large'
    ];
    switch (domain)
    {
        case 'Science':
            if(0 <= impor.Science && impor.Science < 0.33)
                return size[0];
            else if(0.33 <= impor.Science && impor.Science < 0.67)
                return size[1];
            else if(0.67 <= impor.Science)
                return size[2];
            break;
        case 'Health':
            if(0 <= impor.Health && impor.Health < 0.33)
                return size[0];
            else if(0.33 <= impor.Health && impor.Health < 0.67)
                return size[1];
            else if(0.67 <= impor.Health)
                return size[2];
            break;
        case 'Sports':
            if(0 <= impor.Sports && impor.Sports < 0.33)
                return size[0];
            else if(0.33 <= impor.Sports && impor.Sports < 0.67)
                return size[1];
            else if(0.67 <= impor.Sports)
                return size[2];
            break;
    }
}