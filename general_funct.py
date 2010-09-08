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
# 2010-08-27 create file for general function 
###

######################################################################

def getMapData(geom,api,buf=0.0003):
    """ Return OSM data inside the bounding box of feature's geometry
    geom = OGR geometry object
    api = pythonOsmApi object
    buf = buffer to downloads osm data; default  0.0003 == 30 meters radius
    """
    #create a buffer around the point of 30 m
    geomBuffer = geom.Buffer(buf)
    #get bounding box
    bbox = geomBuffer.GetEnvelope()
    #download data
    osmData = api.Map(bbox[0],bbox[2],bbox[1],bbox[3])
    return osmData

def getPointData(osmData,line=False):
    """ Return the list of point data
    osmData = variable created with getMapData()
    line = False if you want point data, true if you want nodes of line data
    """
    pointData = []
    for i in osmData:
	#if is not a node without tags
	if line==False and i[unicode('type')] == 'node' and i[unicode('data')][unicode('tag')] != {}:
	    #if is not a node with only tag created_by
	    if len(i[unicode('data')][unicode('tag')]) == 1 and i[unicode('data')][unicode('tag')].keys() == unicode('created_by'):
		#not done
		continue
	    else:
		#add node
		pointData.append(i)
	# this is only for return nodes of line data
	elif line==True and i[unicode('type')] == 'node' and i[unicode('data')][unicode('tag')] == {}:
	    pointData.append(i)
    return pointData

def checkDiversityTags(tagOSM,tagPoint):
    """ Check the similarity of tags
    tagOSM = tags of osm data
    tagNew = tags of data to import
    """
    if len(tagOSM) >= len(tagPoint):
	tagMag = tagOSM
	tagMin = tagPoint
    else:
	tagMag = tagPoint
	tagMin = tagOSM
    allTags = 0.0
    tagsDifferent = 0.0    
    # for all tag in osm data
    for i in tagMin.keys():
	keyTag = i
	allTags = allTags + 1.0
	# if the tag's key of new point doesn't contain the tag in osm data 
	if tagMag.keys().count(i) == 0:
	    tagsDifferent = tagsDifferent + 1.0
	# if the tag's key of new point is contained in osm data
	else:
	    # if the value of tag is different
	    if tagMin[i] != tagMag[keyTag]:
		tagsDifferent = tagsDifferent + 1.0
    # check the % of ugual tags
    percUgual = tagsDifferent * 100 / allTags
    #print "Percentuale : " + str(percUgual)
    # if number of tags is <=2 all tag must be ugual for upload data
    if allTags <= 2: 
	if percUgual != 100:
	    return 0
	else:
	    return 1
    # if number of tags is >2 and <=4 the percent must be >66 for upload data 
    elif allTags <= 4 and allTags > 2:
	if percUgual < 66:
	    return 0
	else:
	    return 1     
    # if number of tags is >4 the percentual must be >75 for upload data
    if allTags > 4 :
	if percUgual < 75:
	    return 0
	else:
	    return 1

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