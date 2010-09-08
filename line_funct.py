# -*- coding: utf-8 -*-

######################################################################
### info
# begin : 2010-05-10
# authors: Luca Delucchi
# copyright : (C) 2010 by luca delucchi, Fondazione Edmund Mach
# email : lucadeluge@gmail.com
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
# 2010-08-27 create file for function interesting import line data
###

######################################################################

import general_funct as funct

def createListNodes(geom):
    """ Return a list of nodes for line/polygon elements
    geom = OGR geometry object
    """
    # return geometry in WKT format
    geomWKT = geom.ExportToWkt()
    # if geometry is point
    if geom.GetGeometryType() == 2:
	# return a list of point (x,y)
	listPoints = geomWKT.replace(')','').split('(')[1].split(',')
    # if geometry is line
    elif geom.GetGeometryType() == 3:
	listPoints = geomWKT.replace('))','').split('((')[1].split(',')
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

def foundNearNode(geom,api):
    """ Function to found the nearest node of a geometry 
    geom = geometry of first / last point
    api = pythonOsmApi object
    
    """
    osmData = funct.getMapData(geom,api,buf=0.0002)
    osmNodes = funct.getPointData(osmData,line=True)

def correctEndNodes(listNodes,geom,api):
    """ Function control if is present a way near the first and last point, 
    if it's present it connect the two lines 
    listNodes = element returned by createListNodes function
    geom = the geometry of line
    api = pythonOsmApi object
    """
    nPoints = geom.GetPointCount()
    # geometry of first point
    geomStartNode = ogr.Geometry(ogr.wkbPoint)
    geomStartNode.addpoint(geom.GetPoint(0))
    # geometry of last point
    geomEndNode = ogr.Geometry(ogr.wkbPoint)
    geomEndNode.addpoint(geom.GetPoint(nPoints-1))
    # function to found the near point
    foundNearNode(geomStartNode,api)
    foundNearNode(geomEndNode,api)

    #startOsmData = funct.getMapData()
    
def loadLines(layer,api):
    """ The function to load line and polygon vector inside OSM DB
    layer = OGR layer object
    api = PythonOsmApi object
    """
    fields = funct.fieldsName(layer)
    feature = layer.GetNextFeature()
    listAllNodes = []
    while feature:
	geomFeat = feature.GetGeometryRef()
	tags = funct.tagDef(feature,fields)
	if geomFeat.GetGeometryType() == 3:
	    tags[unicode('area')] = unicode('yes')
	listNodes = createListNodes(geomFeat)
	correctEndNodes(listNodes,geomFeat,api)
	wayDef = {unicode('nd'):listNodes, unicode('tag'):tags}
	api.WayCreate(wayDef)
	feature=layer.GetNextFeature()
    api.flush()   	    