# -*- coding: utf-8 -*-

######################################################################
### info
# begin : 2011-04-17
# authors: Luca Delucchi
# copyright : (C) 2011 by luca delucchi, Fondazione Edmund Mach
# email : lucadeluge@gmail.com
# version : 0.2
###

### license
# This program is free software; you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published by 
# the Free Software Foundation; either version 2 of the License. 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License (GPL) for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
#  Free Software Foundation, Inc.,
#  59 Temple Place - Suite 330,
#  Boston, MA  02111-1307, USA.
###

import sys, os
try:
    import osgeo.ogr as ogr
    import osgeo.osr as osr
except ImportError:
    import ogr, osr
    

inputName = sys.argv[1]

#input file
inDatasource = ogr.Open(inputName)
#create datasource
layer = inDatasource.GetLayer()
#out list of fieldDefn
fields=[]
#feature definition
featureDefn=layer.GetLayerDefn()
for i in range(featureDefn.GetFieldCount()):
    #input field definition
    fieldDefn=featureDefn.GetFieldDefn(i)
    #append field name to the list
    fields.append(fieldDefn.GetName())
print fields

#outputString = "park = new OpenLayers.Layer.GML(\"Piemonte Parks\",\"data/parchi_piemonte.json\",{
    #format: OpenLayers.Format.GeoJSON,
    #projection: map.displayProjection,
    #styleMap: new OpenLayers.StyleMap({
	#'default': new OpenLayers.Style({
	    #'fillColor': \"ffffff\",
	    #'fillOpacity': \"0.0\",
	    #'strokeColor':  \"000000\",
	    #'strokeWidth':  \"1\"
	#}),
	#'select': new OpenLayers.Style({
	    #'fillColor': "ffffff",
	    #'fillOpacity': "0.0",
	    #'strokeColor':  "ffff00",
	    #'strokeWidth':  "2.0"
	#}),	
    #})
  #})
  #map.addLayer(park);   
  #//select feature
  #function onFeatureSelect(feature) {
#//       selectedFeature = feature;
      #listLayer.push(feature);
  #}

  #//remove feature from layer list
  #function onFeatureUnselect(feature) {
      #listLayer.remove(feature);
  #}
  #//add event on park layer
  #park.events.on({
      #"featureselected": function(e) {
	  #onFeatureSelect(e.feature);
      #},
      #"featureunselected": function(e) {
	  #onFeatureUnselect(e.feature);
      #}
  #});    
  
  #//STORES FOR LAYERS, THE NAME IS store + layer_name ########################
  #//store for park layer
  #var storepark = new GeoExt.data.FeatureStore({
    #fields: [
        #{name: "CODICE", type: "string"},
        #{name: "ENTE", type: "string"},
        #{name: "LOCALITA", type: "string"}/*,
        #{name: "number_fac", type: "int", defaultValue: 0}*/
    #],
    #layer: park
  #}); 

#"
