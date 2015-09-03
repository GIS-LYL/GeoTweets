$(document).ready(function(){
    
    //initialize
    var tweetData = null; //Tweet data
    var tweetClusterGroups = []; // Tweets cluster group Array
    var eventClusterGroup = null; // Events cluster group
    var eventData = null; // Events data
    var tweetHeatLayer = null;
    var tweetHeat = null; // Tweets heat map
    var eventHeatLayer = null;
    var eventHeat = null; // Events heat map
    //Date part
    var CurrentDay =  new Date();    
    var strYear1 = CurrentDay.getFullYear(); 
    var strDay1 = CurrentDay.getDate(); 
    var strMonth1 = CurrentDay.getMonth()+1;    
    if(strMonth1 < 10) 
    { 
        strMonth1 = "0" + strMonth1; 
    }
    if(0 <= strDay1 && strDay1 <= 9)
    {
        strDay1 = "0" + strDay1;
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
    if(0 <= strDay2 && strDay2 <= 9)
    {
        strDay2 = "0" + strDay2;
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
    
    //Fade in/out events geoJson
    $("#Geo-tweet").click(function(){
        if($(this).hasClass("active")){
            $(this).removeClass("active");
            clearTweetDataFromMap();
        }
        else{
            $(this).addClass("active");
            printTweetDataToMap();
        }
    });
    
    //Fade in/out events geoJson
    $("#Geo-event").click(function(){
        if($(this).hasClass("active")){
            $(this).removeClass("active");
            clearEventDataFromMap();
        }
        else{
            $(this).addClass("active");
            printEventDataToMap();
        }
    });
    
    //Fade in/out heatmap
    $("#Geo-tweetHeat").click(function(){
        if($(this).hasClass("active")){
            $(this).removeClass("active");
            clearTweetHeatFromMap();
        }
        else{
            $(this).addClass("active");
            displayTweetHeatToMap();
        }
    });
    
    $("#Geo-eventHeat").click(function(){
        if($(this).hasClass("active")){
            $(this).removeClass("active");
            clearEventHeatFromMap();
        }
        else{
            $(this).addClass("active");
            displayEventHeatToMap();
        }
    });

    function FireEvents(e)
    {
        //Time
        var startTimeInput = $("#Geo-from").val();
        var endTimeInput = $("#Geo-to").val();

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
                clearTweetDataFromMap();
                tweetData = data.tweets;
                printTweetDataToMap();
                $("#Geo-tweet").addClass("active");
                eventData = data.events;
                tweetHeat = data.tweetsHeat;
                eventHeat = data.eventsHeat;
            },
            error:function(XMLHttpRequest, textStatus, errorThrown){
                //alert(errorThrown);
            }
        });
    }
    
    function printTweetDataToMap()
    {
        var tweetLayer = L.mapbox.featureLayer();
        tweetLayer.setGeoJSON(tweetData);
        
        function makeGroup(color) {
            /*return new L.MarkerClusterGroup({
                iconCreateFunction: function(cluster) {
                    return new L.DivIcon({
                        //iconUrl: "http://google-maps-utility-library-v3.googlecode.com/svn/trunk/markerclusterer/images/m1.png",
                        iconSize: [30, 30],
                        html: '<div style="text-align:center;color:#fff;background:' + color + '">' + cluster.getChildCount() + '</div>'
                        //html: '<div style="text-align:center;backgroud:rgba(0,0,0,0.5)><img src="http://google-maps-utility-library-v3.googlecode.com/svn/trunk/markerclusterer/images/m1.png">' + cluster.getChildCount() + '</div>'
                    });
                }
            }).addTo(map);*/
                        
            return new L.MarkerClusterGroup({
                iconCreateFunction: function(cluster){
                    return L.mapbox.marker.icon({
                        'marker-symbol': cluster.getChildCount(),
                        'marker-color': color,
                        'marker-size': 'large'
                    });
                }
            }).addTo(map);
        }
        
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
        
        for(i = 0; i <= 9; i++)
            tweetClusterGroups.push(makeGroup(color[i]));
        //alert(data.type);
        
        tweetLayer.eachLayer(function(layer){
            var prop = layer.feature.properties;
            var impor = prop.importance;
            tweetClusterGroups[parseInt(impor*10)].addLayer(layer);
            //alert(data.type);
            var popup = "<h1>" + prop.name + "@" + prop.name + "</h1><p>" + prop.text + "</p> <p><a href=" + prop.media_url + "></a></p><h2>" + prop.location + "</h2>" + "<h2>" + impor +"</h2>";
                
            layer.on('click',function(e){
                    map.panTo(layer.getLatLng());
            });
            layer.bindPopup(popup);
            layer.setIcon(L.mapbox.marker.icon({
                    'marker-color':giveMeColor(impor)
                    //'marker-symbol':'embassy'
                    //'marker-size':giveMeSize(impor)
            }));
        });
        //alert(data.type);
    }
    
    function clearTweetDataFromMap()
    {
        for(var i = 0; i != tweetClusterGroups.length; i++)
            tweetClusterGroups[i].clearLayers();
        tweetClusterGroups = [];
    }
    
    function printEventDataToMap()
    {
        //alert(eventData.type);
        eventClusterGroup = new L.MarkerClusterGroup();

        var eventLayer = L.mapbox.featureLayer();

        eventLayer.setGeoJSON(eventData).addTo(eventClusterGroup);

        eventLayer.eachLayer(function(locale){
            var prop = locale.feature.properties;
            var popup = '<h1>'+ prop.type +'</h1>'+'<h2>'+prop.place+'</h2>';
            locale.on('click',function(e){
                map.panTo(locale.getLatLng());
            });
            locale.bindPopup(popup);
        });

        map.addLayer(eventClusterGroup);
    }
    
    function clearEventDataFromMap()
    {
        if(eventClusterGroup != null)
            eventClusterGroup.clearLayers();
    }
    
    //Heat map function
    function displayTweetHeatToMap()
    {
        tweetHeatLayer = L.heatLayer(tweetHeat,{
            maxzoom:17,
            minOpacity:0.4,
            max:1,
            radius:25,
            blur:10,
            gradient:{
                0.2: '#ffffb2',
                0.4: '#fecc5c',
                0.6: '#fd8d3c',
                0.8: '#f03b20',
                1.0: '#bd0026'
            }
        }).addTo(map);
    }
    
    function displayEventHeatToMap()
    {
        eventHeatLayer = L.heatLayer(eventHeat,{
            maxzoom:17,
            minOpacity:0.4,
            max:1,
            radius:25,
            blur:10,
            gradient:{
                0.2: '#1debf0',
                0.4: '#1dc0f0',
                0.6: '#1dcbf0',
                0.8: '#1d96f0',
                1.0: '#1d56f0'
            }
        }).addTo(map);
    }
    
    function clearTweetHeatFromMap()
    {
        if(tweetHeatLayer != null)
            tweetHeatLayer.onRemove(map);
    }
    
    function clearEventHeatFromMap()
    {
        if(eventHeatLayer != null)
            eventHeatLayer.onRemove(map);
    }



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
    var style = {color:'red', opacity: 1.0, fillOpacity: 1.0, weight: 2, clickable: false};

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