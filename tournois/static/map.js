import Map from '/static/ol/Map.js';
import View from '/static/ol/View.js';
import OSM from '/static/ol/source/OSM.js';
import TileLayer from '/static/ol/layer/Tile.js';
import {fromLonLat} from '/static/ol/proj.js';

var mapElem = document.getElementById('map')
var coords = [parseFloat(mapElem.getAttribute("start-longitude").replace(",", ".")), parseFloat(mapElem.getAttribute("start-lattitude").replace(",", "."))]
var zoom = parseFloat(mapElem.getAttribute("zoom").replace(",", "."))

new Map({
  layers: [
    new TileLayer({source: new OSM()}),
  ],
  view: new View({
    center: fromLonLat(coords),
    zoom: zoom,
  }),
  target: 'map',
});
