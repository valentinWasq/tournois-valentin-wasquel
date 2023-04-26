import Map from '/static/ol/Map.js';
import View from '/static/ol/View.js';
import OSM from '/static/ol/source/OSM.js';
import TileLayer from '/static/ol/layer/Tile.js';
new Map({
  layers: [
    new TileLayer({source: new OSM()}),
  ],
  view: new View({
    center: [0, 0],
    zoom: 2,
  }),
  target: 'map',
});