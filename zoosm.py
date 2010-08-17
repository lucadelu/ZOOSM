# -*- coding: utf-8 -*-

######################################################################
### info
# begin : 2010-05-10
# authors: Luca Delucchi
# copyright : (C) 2010 by luca delucchi, Fondazione Edmund Mach
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

### history
# 2010-08-17 version 0.2 import line and polygon elements
# 2010-05-24 version 0.1 import point elements
# 2010-05-10 start writing code 
###

######################################################################


import sys, os
try:
    import osgeo.ogr as ogr
    import osgeo.osr as osr
except ImportError:
    import ogr, osr
#import OSMapi
from OsmApi import OsmApi

def ZoOSM(conf,inputs,outputs):
    """ Function for ZOO for import vector data on OSM DB 
    All parameters are passed from ZOO request
    """
    #the name of vector
    inputName = conf["main"]["tmpPath"]+inputs["inputvector"]["value"]
    #the username of openstreetmap
    usern = inputs["username"]["value"]
    #the password of user in openstreetmap
    passw = inputs["password"]["value"]

    #input file
    inDatasource = ogr.Open(inputName)
    #create datasource
    inLayer = inDatasource.GetLayer()
    #create input spatial reference system
    inSpatial = inLayer.GetSpatialRef()
    #create lat/long spatial reference system
    latlongSpatial = osr.SpatialReference()
    latlongSpatial.ImportFromEPSG(4326)
    #check if the input spatial reference system is lat/long
    if inSpatial.ExportToProj4() != latlongSpatial.ExportToProj4():
	output = 'The input vector has not the correct spatial reference' \
	+' system; it would be LatLong, ESPG code number 4326'
	outputs["output"]["value"]= output
	return 3
    #get first feature for the geometry type
    inFeature = inLayer.GetFeature(0)
    inGeomType = inFeature.GetGeometryRef().GetGeometryType()

    #create osm api
    osmapi = OsmApi(username = unicode(usern), password = unicode(passw), 
    appid = unicode('Z0OSM 0.2'), changesetauto = True, changesetautotags = 
    {unicode('comment'): unicode('auto import of features' \
    + ' from '+inLayer.GetName()+' using ZOOSM')})

    #check the geometry type
    if inGeomType == 1:
	# point data, load point on OSM DB
	loadPoint(inLayer,osmapi)
    elif inGeomType == 2 or inGeomType == 3:
	# line/area data, load point on OSM DB
	loadLines(inLayer,osmapi)
    else :
	output = 'The input vector has a geometry type is not yet supported'
	outputs["output"]["value"]= output
	return 3
    #destroy input datasource
    inDatasource.Destroy()

    outputs["output"]["value"]="All data are imported correctly"
    return 3

def fieldsName(layer):
    """ Function for return the field's name list 
    layer = OGR layer object
    """
    #out list of fieldDefn
    fields=[]
    #feature definition
    featureDefn=layer.GetLayerDefn()
    for i in range(featureDefn.GetFieldCount()):
	#input field definition
	fieldDefn=featureDefn.GetFieldDefn(i)
	#append field name to the list
	fields.append(fieldDefn.GetName())
    return fields

def tagDef(feature,fieldsname):
    """ Return a dictionary with the tag from attribute value 
    of vector feature 
    feature = OGR feature object
    fieldsname = list of name's fields returned from fieldsName function
    """   
    #the dictionary of tags
    tag={}
    for field in fieldsname:
	tag[unicode(field.lower())]=unicode(feature.GetField(field))
    return tag
    
def createListNodes(geom):
    """ Return a list of nodes for line/polygon elements
    geom = OGR geometry object
    """
    # return geometry in WKT format
    geomWKT = geom.ExportToWkt()
    if geom.GetGeometryType() == 2:
	# return a list of point (x,y)
	listPoint = geomWKT.replace(')','').split('(')[1].split(',')
    elif geom.GetGeometryType() == 3:
	listPoint = geomWKT.replace('))','').split('((')[1].split(',')
    # create list of nodes
    listNodes = []
    iD=-1
    # for each point
    for i in listPoints:
	# create a list of x and y values
	xy = i.split(' ')
	# create node definition in osm format
	nodeDef={unicode('id'):iD, unicode('lon'):i[0],unicode('lat'):i[1], 
	unicode('tag'):{}}
	# add node to listnode
	listNodes.append(nodeDef)
	iD=iD-1
    # if geometry type is polygon copy the first poi with the last
    if geom.GetGeometryType() == 3:
	listNodes[-1]=listNodes[0]
    # return nodes list
    return listNodes
      
def loadPoint(layer,api):
    """ The function to load point vector inside OSM DB
    layer = OGR layer object
    api = PythonOsmApi object
    """
    #fields name of input vector
    fields=fieldsName(layer)
    #loop inside the feature
    feature=layer.GetNextFeature()
    #first id for (after it will be sobstitute on osmdb
    iD=-1
    while feature:
	#define the tags for the feature
	tags=tagDef(feature,fields)
	#get the geometry of the feature
	geom=feature.GetGeometryRef()
	#get osm data near the feature (look function getMapData)
	osmData=getMapData(geom,api)
	#from osm data extract only point
	pointData=getPointData(osmData)
	#create the new point
	nodeDef={unicode('id'):iD, unicode('lon'):geom.GetX(), 
	unicode('lat'):geom.GetY(),unicode('tag'):tags}
	api.NodeCreate(nodeDef)
	iD=iD-1
	feature=layer.GetNextFeature()
    #load data on OSM database
    api.flush()
    
def loadLines(layer,api):
    """ The function to load line and polygon vector inside OSM DB
    layer = OGR layer object
    api = PythonOsmApi object
    """
    fields = fieldsName(layer)
    feature = layer.GetNextFeature()
    listAllNodes = []
    while feature:
	geomFeat = feature.GetGeometryRef()
	tags = tagDef(feature,fields)
	if geomFeat.GetGeometryType() == 3:
	    tags[unicode('area')] = unicode('yes')
	listNodes = createListNodes(geomFeat)
	wayDef = {unicode('nd'):listNodes, unicode('tag'):tags}
	api.WayCreate(wayDef)
	feature=layer.GetNextFeature()
    api.flush()