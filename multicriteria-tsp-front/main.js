import "./style.css";
import "ol/ol.css";
import {Feature, Map, View} from 'ol';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import Point from 'ol/geom/Point';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import {Fill, Icon, Stroke, Style, Text} from 'ol/style';
import {GeoJSON} from 'ol/format';
import LineString from 'ol/geom/LineString';
import $ from 'jquery';

var properties = [];

var counter = 1;

$.ajax({
  url: 'http://127.0.0.1:5000/properties',
  dataType: 'json',
  method: 'GET',
  contentType: 'application/json',
  success: function (data) {
    let fieldsDiv = $("#fields");
    let fields = '<div class="input-group m-3">';
    properties = data.properties;
    properties.forEach(function(item, i, arr) {
      let field;
      if (i === 0) {
        field = "<span class='input-group-text'>" + 
          item +" is main</span>";
      } else {
        field = "<span class='input-group-text'>" + item +"</span> \
          <input type='number' min='0' class='form-control' id='" + item + "'>"
      }
      fields += field;
    });
    fields += "</div>";
    fieldsDiv.append(fields);
  }
});

var points = [];

const style = new Style({
  image: new Icon({
    anchor: [0.5, 1],
    anchorXUnits: 'fraction',
    anchorYUnits: 'fraction',
    src: 'marker.png',
    opacity: 0.95,
  }),
  stroke: new Stroke({
    width: 3,
    color: [255, 0, 0, 1],
  }),
  fill: new Fill({
    color: [0, 0, 255, 0.6],
  }),
  text: new Text({
    text: counter
  })
});

const vectorSource = new VectorSource({
  format: new GeoJSON()
});

const map = new Map({
  target: 'map',
  layers: [
    new TileLayer({
      source: new OSM({
        transition: 0
      })
    }),
    new VectorLayer({
      source: vectorSource
    })
  ],
  view: new View({
    center: [0, 0],
    zoom: 6,
  })
});

map.on('singleclick', function(evt) {
  let newFeature = new Feature({
    geometry: new Point(evt.coordinate)
  });
  newFeature.setStyle(new Style({
    image: new Icon({
      anchor: [0.5, 1],
      anchorXUnits: 'fraction',
      anchorYUnits: 'fraction',
      src: 'marker.png',
      opacity: 0.95,
    }),
    text: new Text({
      font: 'bold 16px serif',
      text: "" + counter,
      offsetY: 10
    })
  }));
  points.push(evt.coordinate);
  vectorSource.addFeature(newFeature);
  counter++;
});

function drawLines(data) {
  let header = "<thead><tr><th>#</th><th>Kind</th>";
  properties.forEach(function (item, i, arr) {
    header += "<th>" + item + "</th>"
  });
  header += "</tr></thead>";
  $("#result").append(header);
  $("#result").append("<tbody>");
  for (let i = 0; i < data.length; i++) {
    let responseLine = data[i];
    let line = new LineString([
      points[responseLine.pointA], 
      points[responseLine.pointB]
    ]);
    let feature = new Feature({
      geometry: line
    });
    feature.setStyle(new Style({
      stroke: new Stroke({
        width: 3,
        color: [0, 0, 255, 0.5],
      }),
      text: new Text({
        text: "" + (i+1),
        offsetY: 10
      })
    }));
    vectorSource.addFeature(feature);
    let row = "<tr><td>" + (i+1) + "</td>" +
              "<td>" + responseLine.kind + "</td>" +
              "<td>" + responseLine.path + "</td>" +
              "<td>" + responseLine.cost + "</td>" +
              "<td>" + responseLine.time + "</td>" +
              "<td>" + responseLine.class + "</td></tr>";
    $("#result").append(row);
  }
  $("#result").append("</tbody>");
};

$("#clear-map").on('click', function (evt) {
  vectorSource.clear();
  points = [];
  counter = 1;
  $("#result").empty();
});

$("#send-request").on('click', function(evt) {
  let features = vectorSource.getFeatures();
  let points = [];
  features.forEach(function(item, i, arr) {
    if (item.getGeometry() instanceof Point) {
      points.push({coordinate: item.getGeometry().getCoordinates()});
    }
  });
  $.ajax({
    data:JSON.stringify({
      points: points,
      limits: initLimits(),
      properties: properties
    }),
    url: 'http://127.0.0.1:5000/process',
    dataType: 'json',
    method: 'POST',
    contentType: 'application/json',
    success: function (data) {
      drawLines(data.result);
    }
  })
});

function initLimits() {
  let fields = $("#fields").find(".form-control");
  let limits = [];
  for (let i = 0; i < fields.length; i++) {
    limits.push({
      name: $(fields[i]).attr('id'),
      value: Number($(fields[i]).val())
    });
  }
  return limits;
};