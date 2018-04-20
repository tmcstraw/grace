var LIBRARY_OBJECT=function(){"use strict";var e,t,a,o,r,l,n,i,s,c,u,d,p,y,v,f,g,m,S,h,w,b,x,E,P,T,F,I,O,C,L,N,M,R,_,j;return N=function(){var a=$("#layers");S=a.attr("data-slider-max"),o=a.attr("data-color-bar"),o=JSON.parse(o),r=a.attr("data-range-min"),l=a.attr("data-range-max"),v=$("#plotter"),i=$("#get-plot"),u=$("#modalUpload"),t=$("#btn-add-shp"),e=1e3,h={}},I=function(){var e=document.getElementById("cv").getContext("2d");o.forEach(function(t,a){e.beginPath(),e.fillStyle=t[0],e.fillRect(35*a,0,35,20),e.fillText(t[1],35*a,30)})},j=function(){var e=document.getElementById("cv"),t=e.getContext("2d");t.clearRect(0,0,e.width,e.height),o.forEach(function(e,a){t.beginPath(),t.fillStyle=e[0],t.fillRect(35*a,0,35,20),t.fillText(e[1],35*a,30)})},P=function(){$("#poly-lat-lon").val(""),$("#point-lat-lon").val(""),$("#shp-lat-lon").val("")},C=function(){!function(){var e,t,a;e=$("#app-content-wrapper")[0],t=new MutationObserver(function(){window.setTimeout(function(){p.updateSize()},350)}),$(window).on("resize",function(){p.updateSize()}),a={attributes:!0},t.observe(e,a)}(),p.on("singleclick",function(e){if($(n).popover("destroy"),"pointer"==p.getTargetElement().style.cursor&&"None"==$("#types").find("option:selected").val()){var t=e.coordinate;y.setPosition(t);var o=p.getView(),r=o.getResolution(),l=a.getSource().getGetFeatureInfoUrl(e.coordinate,r,o.getProjection(),{INFO_FORMAT:"application/json"});l&&$.ajax({type:"GET",url:l,dataType:"json",success:function(e){var t=parseFloat(e.features[0].properties.GRAY_INDEX);t=t.toFixed(2),$(n).popover({placement:"top",html:!0,content:"Value: "+t}),$(n).popover("show"),$(n).next().css("cursor","text")},error:function(e,t,a){console.log(Error)}})}}),p.on("pointermove",function(e){if(!e.dragging){var t=p.getEventPixel(e.originalEvent),o=p.forEachLayerAtPixel(t,function(e){if(e!=s[0]&&e!=s[1]&&e!=s[2]&&e!=s[4])return a=e,!0});p.getTargetElement().style.cursor=o?"pointer":""}})},L=function(){function e(){var e,t=new ol.format.GeoJSON;try{e=t.writeFeatures(i.getSource().getFeatures())}catch(e){return void $("#data").val(e.name+": "+e.message)}return e}var t=ol.proj.get("EPSG:3857"),a=new ol.layer.Tile({source:new ol.source.BingMaps({key:"5TC0yID7CYaqv3nVQLKe~xWVt4aXWMJq2Ed72cO4xsA~ApdeyQwHyH_btMjQS1NJ7OHKY8BK-W-EMQMrIavoQUMYXeZIQOUURnKGBOC7UCt4",imagerySet:"AerialWithLabels"})}),o=new ol.control.FullScreen,r=new ol.View({center:[16697923.619,2315372.27532],projection:t,zoom:2});g=new ol.source.Vector,m=new ol.layer.Vector({source:g});var l=new ol.source.Vector({wrapX:!1}),i=new ol.layer.Vector({name:"my_vectorlayer",source:l,style:new ol.style.Style({fill:new ol.style.Fill({color:"rgba(255, 255, 255, 0.2)"}),stroke:new ol.style.Stroke({color:"#ffcc33",width:2}),image:new ol.style.Circle({radius:7,fill:new ol.style.Fill({color:"#ffcc33"})})})});w=new ol.source.ImageWMS,b=new ol.layer.Image({source:w}),s=[a,i,m,b],c={},(p=new ol.Map({target:document.getElementById("map"),layers:s,view:r})).addControl(new ol.control.ZoomSlider),p.addControl(o),p.crossOrigin="anonymous",n=document.getElementById("popup"),y=new ol.Overlay({element:n,positioning:"bottom-center",stopEvent:!0}),p.addOverlay(y);var d,v,f,S=function(e){var t=document.getElementById("types").value;$("#data").val(""),"None"!==t&&(v&&p.removeInteraction(v),v=new ol.interaction.Draw({source:l,type:e}),p.addInteraction(v)),"Point"!==f&&"Polygon"!==f||(v.on("drawend",function(e){d=e.feature}),v.on("drawstart",function(e){l.clear()}))};i.getSource().on("addfeature",function(t){var a=e(),o=JSON.parse(a),r=o.features[0].geometry.type;if("Point"==r){var l=o.features[0].geometry.coordinates,n=ol.proj.transform(l,"EPSG:3857","EPSG:4326");$("#point-lat-lon").val(n)}else if("Polygon"==r){l=o.features[0].geometry.coordinates[0];n=[],l.forEach(function(e){var t=ol.proj.transform(e,"EPSG:3857","EPSG:4326");n.push("["+t+"]")});var i='{"type":"Polygon","coordinates":[['+n+"]]}";$("#poly-lat-lon").val(i)}}),$("#types").change(function(e){"None"==(f=$(this).find("option:selected").val())?($("#data").val(""),P(),p.removeInteraction(v),i.getSource().clear(),m.getSource().clear()):"Upload"==f?(P(),i.getSource().clear(),m.getSource().clear(),p.removeInteraction(v),u.modal("show")):"Point"==f?(P(),m.getSource().clear(),S(f)):"Polygon"==f&&(P(),m.getSource().clear(),S(f))}).change()},E=function(){p.removeLayer(b);var e=T(),t="sw_global:"+$("#select_layer").find("option:selected").val(),a='<StyledLayerDescriptor version="1.0.0"><NamedLayer><Name>'+t+'</Name><UserStyle><FeatureTypeStyle><Rule>        <RasterSymbolizer>         <ColorMap>        <ColorMapEntry color="#000000" quantity="'+r+'" label="nodata" opacity="0.0" />'+e+"</ColorMap>        </RasterSymbolizer>        </Rule>        </FeatureTypeStyle>        </UserStyle>        </NamedLayer>        </StyledLayerDescriptor>";w=new ol.source.ImageWMS({url:"http://tethys.byu.edu:8181/geoserver/wms",params:{LAYERS:t,SLD_BODY:a},serverType:"geoserver",crossOrigin:"Anonymous"}),b=new ol.layer.Image({source:w}),p.addLayer(b)},_=function(e){var t=T(),a="sw_global:"+e,o='<StyledLayerDescriptor version="1.0.0"><NamedLayer><Name>'+a+'</Name><UserStyle><FeatureTypeStyle><Rule>        <RasterSymbolizer>         <ColorMap>         <ColorMapEntry color="#000000" quantity="'+r+'" label="nodata" opacity="0.0" />'+t+"</ColorMap>        </RasterSymbolizer>        </Rule>        </FeatureTypeStyle>        </UserStyle>        </NamedLayer>        </StyledLayerDescriptor>";w.updateParams({LAYERS:a,SLD_BODY:o})},T=function(){var e="";return o.forEach(function(t,a){var o='<ColorMapEntry color="'+t[0]+'" quantity="'+t[1]+'" label="label'+a+'" opacity="'+t[2]+'"/>';e+=o}),e},O=function(){$("#slider").slider({value:1,min:0,max:S-1,step:1,animate:"fast",slide:function(e,t){var a=$("#select_layer option")[t.value].text;$("#grace-date").val(a);var o=$("#select_layer option")[t.value].value;_(o)}}),$("#opacity-slider").slider({value:.7,min:.2,max:1,step:.1,animate:"fast",slide:function(e,t){var a=t.value;$("#opacity").val(a);var r=$("#slider").slider("option","value"),l=$("#select_layer option")[r].value;o.forEach(function(e,t){e[2]=a}),_(l)}}),$("#max-slider").slider({value:50,min:1,max:50,step:1,animate:"fast",slide:function(e,t){var a=t.value;$("#cbar-slider").val(a);for(var r=$("#slider").slider("option","value"),n=$("#select_layer option")[r].value,i=(l=t.value)/10,s=-l,c=[],u=0;u<=20;u+=1)c.push(parseFloat(s).toFixed(1)),s+=i;o.forEach(function(e,t){e[1]=c[t]}),j(),_(n)},start:function(){$("#cbar-slider").val(10);for(var e=$("#slider").slider("option","value"),t=$("#select_layer option")[e].value,a=(l=10)/10,r=-l,n=[],i=0;i<=20;i+=1)n.push(parseFloat(r).toFixed(1)),r+=a;o.forEach(function(e,t){e[1]=n[t]}),j(),_(t),$("#max-slider").slider("value",10)}})},F=function(){if(""==$("#poly-lat-lon").val()&&""==$("#point-lat-lon").val()&&""==$("#shp-lat-lon").val())return $(".warning").html("<b>No feature selected. Please create a feature using the map interaction dropdown. Plot cannot be generated without a feature.</b>"),!1;$(".warning").html("");var e=i.serialize(),t=$("#view-file-loading");$("#btn-get-plot").attr("disabled",!0),t.removeClass("hidden"),$("#plotter").addClass("hidden"),$.ajax({type:"POST",url:"/apps/grace/plot-global-sw/",dataType:"HTML",data:e,success:function(e){var a=JSON.parse(e);$("#plotter").highcharts({chart:{type:"area",zoomType:"x",height:350},title:{text:"Values at "+a.location,style:{fontSize:"11px"}},xAxis:{type:"datetime",labels:{format:"{value:%d %b %Y}",rotation:45,align:"left"},title:{text:"Date"}},yAxis:{title:{text:"Total Surface Water Storage Anomaly (cm)"}},exporting:{enabled:!0},series:[{data:a.values,name:"Total Surface Water Storage Anomaly (cm)"}]}),$("#plotter").removeClass("hidden"),t.addClass("hidden"),$("#btn-get-plot").attr("disabled",!1)}})},$("#btn-get-plot").on("click",F),x=function(){var t=$("#slider").slider("value");h=setInterval(function(){t+=1,$("#slider").slider("value",t),t===S-1&&(t=0)},e)},$(".btn-run").on("click",x),$(".btn-stop").on("click",function(){clearInterval(h)}),$(".btn-increase").on("click",function(){clearInterval(h),e>250&&(e-=250,$("#speed").val((1/(e/1e3)).toFixed(2)),x())}),$(".btn-decrease").on("click",function(){clearInterval(h),e+=250,$("#speed").val((1/(e/1e3)).toFixed(2)),x()}),R=function(){var e,t=$("#shp-upload-input")[0].files;u.modal("hide"),e=M(t),$.ajax({url:"/apps/grace/upload-shp/",type:"POST",data:e,dataType:"json",processData:!1,contentType:!1,error:function(e){},success:function(e){var t=e.bounds;g=new ol.source.Vector({features:(new ol.format.GeoJSON).readFeatures(e.geo_json)}),m=new ol.layer.Vector({name:"shp_layer",extent:[t[0],t[1],t[2],t[3]],source:g,style:new ol.style.Style({stroke:new ol.style.Stroke({color:"blue",lineDash:[4],width:3}),fill:new ol.style.Fill({color:"rgba(0, 0, 255, 0.1)"})})}),p.addLayer(m),p.getView().fit(m.getExtent(),p.getSize()),p.updateSize(),p.render();var a=ol.proj.transform([t[0],t[1]],"EPSG:3857","EPSG:4326"),o=ol.proj.transform([t[2],t[3]],"EPSG:3857","EPSG:4326"),r=a.concat(o);$("#shp-lat-lon").val(r)}})},$("#btn-add-shp").on("click",R),M=function(e){var t=new FormData;return Object.keys(e).forEach(function(a){t.append("files",e[a])}),t},f={},$(function(){L(),C(),N(),O(),I(),(d=$("#max-slider")).slider("option","start").call(d),$("#speed").val((1/(e/1e3)).toFixed(2)),$("#select_layer").change(function(){E();var e=$(this).find("option:selected").index();$("#slider").slider("value",e)}).change(),$("#slider").on("slidechange",function(e,t){var a=$("#select_layer option")[t.value].text;$("#grace-date").val(a);var o=$("#select_layer option")[t.value].value;_(o)})}),f}();