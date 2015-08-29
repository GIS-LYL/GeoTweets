$(document).ready(function(){
    //initialize
    var CurrentDay =  new Date();
    var strYear1 = CurrentDay.getFullYear();
    var strDay1 = CurrentDay.getDate();
    var strMonth1 = CurrentDay.getMonth()+1;
    if(strMonth1 < 10)
    {
        strMonth1 = "0" + strMonth1;
    }
    var CurrentDayFormat = strYear1 + "-" + strMonth1 + "-" + strDay1;

    var LastDay = new Date();
    var Last_milliseconds = CurrentDay.getTime()-1000*60*60*24;
    LastDay.setTime(Last_milliseconds);
    var strYear2 = LastDay.getFullYear();
    var strDay2 = LastDay.getDate();
    var strMonth2 = LastDay.getMonth()+1;
    if(strMonth2 < 10)
    {
        strMonth2 = "0" + strMonth2;
    }
    var LastDayFormat = strYear2 + "-" + strMonth2 + "-" + strDay2;

    $("#Geo-from").val(LastDayFormat);
    $("#Geo-to").val(CurrentDayFormat);


    // Mapbox API
    L.mapbox.accessToken = 'pk.eyJ1IjoidHdlZXRzeW91bGlrZSIsImEiOiI1NDU3MjQxNjRhMWQwMGFlNjY5NGM2ODZjYjgwMWU0NyJ9.73PZ0OMKufVTFYd798HZmg';

    //load the map and the tileLayers
    var map = L.mapbox.map('map', 'tweetsyoulike.mpo7h6lm',{
            minzoom: 2,
            maxzoom: 14
        }).setView([12.15147921044203, 125.15157530234822],8);

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

    //Bounds Query
 //   map.on('moveend', FireEvents);

    //Time Query
    $("#Geo-submit").click(FireEvents);

    //Domain Query
    $("#Geo-domain").children().click(function(e){
        $("#Geo-domain").children(".active").removeClass("active");
        $(e.target).parent().addClass("active");
        FireEvents(e);
    });

    function FireEvents(e)
    {
        //Time
        var startTimeInput = $("#Geo-from").val();
        var endTimeInput = $("Geo-to").val();

        //Bounds
        var bounds = map.getBounds();

        //domains
        var domain = $("#Geo-domain").children(".active").children("a").html();

        var params = {
            startTime: startTimeInput,
            endTime: endTimeInput,
            domain: domain,
            west: bounds.getWest(),
            south: bounds.getSouth(),
            east: bounds.getEast(),
            north: bounds.getNorth()
        };
        $.ajax({
            type:'post',
            url:'GetTweets.php',
            dataType:'json',
            data: params,
            success:function(data){
                printDataToMap(data)
            },
            error:function(XMLHttpRequest, textStatus, errorThrown){
                //alert(errorThrown);
            }
        });
    }
    
    function printDataToMap(data)
    {
        var geoJsonLayerX = L.mapbox.featureLayer();
        geoJsonLayerX.setGeoJSON(data);
        
        function makeGroup(color) {
            return new L.MarkerClusterGroup({
                iconCreateFunction: function(cluster) {
                    return new L.DivIcon({
                        //iconUrl: "http://google-maps-utility-library-v3.googlecode.com/svn/trunk/markerclusterer/images/m1.png",
                        iconSize: [30, 30],
                        html: '<div style="text-align:center;color:#fff;background:' + color + '">' + cluster.getChildCount() + '</div>'
                        //html: '<div style="text-align:center;backgroud:rgba(0,0,0,0.5)><img src="http://google-maps-utility-library-v3.googlecode.com/svn/trunk/markerclusterer/images/m1.png">' + cluster.getChildCount() + '</div>'
                    });
                }
            }).addTo(map);
        }
        
        var color = [
            '#320b12',
            '#4b1144',
            '#641664',
            '#4c1c7d',
            '#2b2296',
            '#93bcd6',
            '#279aaf',
            '#3fc82d',
            '#a5e133',
            '#fbd639'
        ];
        var groups = [];
        for(i = 0; i <= 9; i++)
            groups.push(makeGroup(color[i]));
        
        geoJsonLayerX.eachLayer(function(layer){
            var prop = layer.feature.properties;
            var impor = prop.importance;
            
            groups[parseInt(impor*10)].addLayer(layer);
            
            var popup = "<h1>" + prop.name + "@" + prop.name + "</h1><p>" + prop.text + "</p> <p><a href=" + prop.media_url + "></a></p><h2>" + prop.location + "</h2>" + "<h2>" + impor +"</h2>";
                
            layer.on('click',function(e){
                    map.panTo(layer.getLatLng());
            });
            layer.bindPopup(popup);
            layer.setIcon(L.mapbox.marker.icon({
                    'marker-color':giveMeColor(impor),
                    'marker-symbol':'circle-stroked',
                    'marker-size':giveMeSize(impor)
            }));
        });

        
    }

/*    function printDataToMap(data){
        function makeGroup(tweets)
        {
            var f1 = new Array();

            for(var i = 0; i <= 9; i++)
                f1.push({"type":"FeatureCollection","features":[]});

            for (var i = 0; i < tweets.features.length; i++)
            {
                var obj = tweets.features[i];
                var impor =  obj.properties.importance;
                f1[parseInt(impor * 10)].features.push(obj);
            }
            return f1;
        };

        var color = [
            '#320b12',
            '#4b1144',
            '#641664',
            '#4c1c7d',
            '#2b2296',
            '#93bcd6',
            '#279aaf',
            '#3fc82d',
            '#a5e133',
            '#fbd639'
        ];
        var clusterGroups = [];
        for(var i = 0; i <= 9; i++)
            clusterGroups[i] = new L.MarkerClusterGroup({
                iconCreateFunction:function(cluster){
                    return L.mapbox.marker.icon({
                        'marker-symbol':cluster.getChildCount(),
                        'marker-color':color[i-1],
                        opacity:0.5
                    });
                }
            });
        var exam = makeGroup(data,"Health");
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
                var popup = "<h1>" + prop.name + "@" + prop.name + "</h1><p>" + prop.text + "</p> <p><a href=" + prop.media_url + "></a></p><h2>" + prop.location + "</h2>" + "<h2>" + impor +"</h2>";
                locale.on('click',function(e){
                    map.panTo(locale.getLatLng());
                });
                locale.bindPopup(popup);
                locale.setIcon(L.mapbox.marker.icon({
                    'marker-color':giveMeColor(impor),
                    'marker-symbol':'circle-stroked',
                    'marker-size':giveMeSize(impor)
                }));

            });

            map.addLayer(clusterGroups[i]);


        }
        }*/
    
    


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
function giveMeColor(impor)
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
        '#39fb8b'
    ];
    return color[parseInt(parseInt(impor * 100) / 10)];
}

//size of gradient by the importance of the data
function giveMeSize(impor)
{
    var size = [
        'small',
        'medium',
        'large'
    ];

    if(0 <= impor && impor < 0.33)
        return size[0]
    else if(0.33 <= impor && impor < 0.67)
        return size[1]
    else(0.67 <= impor)
        return size[2]
}