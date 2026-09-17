'use client';

import React, { useState, useEffect } from 'react';
import MapGL, { Source, Layer, Marker } from 'react-map-gl/maplibre';

const start = [32.4222, 34.7720]; // Paphos
const end = [32.4258, 35.0344]; // Polis

export default function Map() {
  const [routeGeoJSON, setRouteGeoJSON] = useState<any>(null);

  useEffect(() => {
    fetch(`https://router.project-osrm.org/route/v1/driving/${start[0]},${start[1]};${end[0]},${end[1]}?geometries=geojson`)
      .then(res => res.json())
      .then(data => {
        if (data.routes && data.routes[0]) {
          setRouteGeoJSON(data.routes[0].geometry);
        }
      })
      .catch(err => console.error(err));
  }, []);

  return (
    <div style={{ width: '100%', height: '100%' }}>
      <MapGL
        initialViewState={{
          longitude: 32.42,
          latitude: 34.90,
          zoom: 9.5,
          pitch: 45
        }}
        mapStyle={{
          version: 8,
          sources: {
            'satellite': {
              type: 'raster',
              tiles: [
                'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
              ],
              tileSize: 256,
              attribution: 'Tiles &copy; Esri'
            }
          },
          layers: [
            {
              id: 'satellite-layer',
              type: 'raster',
              source: 'satellite',
              minzoom: 0,
              maxzoom: 19
            }
          ]
        }}
      >
        <Marker longitude={start[0]} latitude={start[1]} color="#FFDD00" />
        <Marker longitude={end[0]} latitude={end[1]} color="#FFDD00" />

        {routeGeoJSON && (
          <Source id="route-source" type="geojson" data={routeGeoJSON}>
            <Layer
              id="route-glow"
              type="line"
              layout={{ 'line-join': 'round', 'line-cap': 'round' }}
              paint={{
                'line-color': '#FFDD00',
                'line-width': 12,
                'line-blur': 15,
                'line-opacity': 0.6
              }}
            />
            <Layer
              id="route-core"
              type="line"
              layout={{ 'line-join': 'round', 'line-cap': 'round' }}
              paint={{
                'line-color': '#FFDD00',
                'line-width': 4
              }}
            />
          </Source>
        )}
      </MapGL>
    </div>
  );
}
