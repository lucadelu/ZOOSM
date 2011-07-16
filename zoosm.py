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
# 2010-10-08 version 0.2 add check if point is already present
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
import general_funct as funct
import line_funct as line
import point_funct as point

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
    osmapi = OsmApi(api="api06.dev.openstreetmap.org", username = unicode(usern), password = unicode(passw), appid = unicode('Z0OSM 0.2'), changesetauto = True, changesetautotags = 
    {unicode('comment'): unicode('auto import of features' \
    + ' from '+inLayer.GetName()+' using ZOOSM')})

    #check the geometry type
    if inGeomType == 1:
	# point data, load point on OSM DB
	npoint = point.loadPoint(inLayer,osmapi)
        output = '%i features are imported' % npoint
        outputs["output"]["value"]= output
        return 3	
    elif inGeomType == 2 or inGeomType == 3:
	# line/area data, load point on OSM DB
	#line.loadLines(inLayer,osmapi)
	output = 'The input vector has a geometry type is not yet supported'
	outputs["output"]["value"]= output
	return 3	
    else :
	output = 'The input vector has a geometry type is not supported'
	outputs["output"]["value"]= output
	return 3
    #destroy input datasource
    inDatasource.Destroy()

    outputs["output"]["value"]="All data are imported correctly"
    return 3