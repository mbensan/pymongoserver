# -*- coding: utf-8 -*-
import math
from difflib import SequenceMatcher

def harvesianDistance(latitude1, longitude1, latitude2, longitude2):
	earthRadius = 6371 # 6378137 in meters

	radianLatitudeDiff = math.radians(latitude2 - latitude1)
	radianLongitudeDiff = math.radians(longitude2 - longitude1)

	a = math.sin(radianLatitudeDiff/2) * math.sin(radianLatitudeDiff/2) + math.cos(math.radians(latitude1)) * math.cos(math.radians(latitude2)) * math.sin(radianLongitudeDiff/2) * math.sin(radianLongitudeDiff/2)
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

	d = earthRadius * c
	#return d # in Km
	return 1000*d  # in meters

def distanciaGeodesica(latitude1, longitude1, latitude2, longitude2):
	degtorad = 0.01745329
	radtodeg = 57.29577951

	dlong = (longitude1 - longitude2)
	dvalue = (math.sin(latitude1 * degtorad) * math.sin(latitude2 * degtorad))
	dvalue += (math.cos(latitude1 * degtorad) * math.cos(latitude2 * degtorad) * math.cos(dlong * degtorad))

	dd = math.acos(dvalue) * radtodeg

	metros = (dd * 111302)
	return metros

def getStringDiff(str1, str2):
	return SequenceMatcher(None, str1, str2).ratio()



