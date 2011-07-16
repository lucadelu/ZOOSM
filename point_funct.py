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
# 2010-08-27 create file for function interesting import point data
###

######################################################################

import general_funct as funct

def checkNewPoint(geom,tags,pointData):
    '''Function check the similarity of a point, check before inside a buffer and after in the tag
    geom = geometry of the feature
    tags = tags of the feature, return of tagsDef function
    pointData = point data present on osm db, return of getPointData function
    '''   
    #if pointData is null is possible add that feature
    if pointData == []:
        return 1
    else:
	# all point
	nPointData = len(pointData)
	# variable per different data
	nPointDifferent = 0
     	for i in pointData:
	    #print i[unicode('data')][unicode('tag')],tags
	    #check if the tags are similar
	    if funct.checkDiversityTags(i[unicode('data')][unicode('tag')],tags):
		nPointDifferent = nPointDifferent + 1
	# if the number of all point and the different are the same is possible to upload data
	if nPointDifferent == nPointData:
	    return 1
	else:
	    return 0	      

def loadPoint(layer,api):
    """ The function to load point vector inside OSM DB
    layer = OGR layer object
    api = PythonOsmApi object
    """
    #fields name of input vector
    fields = funct.fieldsName(layer)
    #loop inside the feature
    feature = layer.GetNextFeature()
    #first id for (after it will be sobstitute on osmdb
    iD=-1
    n_feature = 0
    while feature:
	#define the tags for the feature
	tags = funct.tagDef(feature,fields)
	#get the geometry of the feature
	geom = feature.GetGeometryRef()
	#get osm data near the feature (look function getMapData)
	osmData = funct.getMapData(geom,api)
	#from osm data extract only point
	pointData = funct.getPointData(osmData)
	#made some control to search if feature already exist on osm db
	if checkNewPoint(geom,tags,pointData):
	    #if the function return true it create the new point
	    nodeDef={unicode('id'):iD, unicode('lon'):geom.GetX(), 
	    unicode('lat'):geom.GetY(),unicode('tag'):tags}
	    api.NodeCreate(nodeDef)
	    n_feature += 1
	    iD=iD-1
	feature=layer.GetNextFeature()
    #load data on OSM database
    api.flush()
    return n_feature