# -*- coding: utf-8 -*-

import json
import datetime

from api.forms import RegisterForm, LoginForm, AddNeedForm, MatchesForm
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from api.models import db
from bson.objectid import ObjectId
import libGeo
# Max elapsed time between two location updates (seconds).
TIME_INTER_REFRESH = 200
# Min demanded similarity between 2 texts
SIMILARITY = 0.7

def ajaxReturn(dict):
	return HttpResponse(json.dumps(dict, ensure_ascii=False))

'''   BEGIN VIEWS '''
def index(request):
	return render(request, "index.html")

def dos(request):
	return HttpResponse('dos');

@csrf_exempt
def signup(request):
	form = RegisterForm(request.POST)

	if request.method == 'POST' and form.validate():
		form_args = {
			'nombre': request.POST['nombre'],
			'email': request.POST['email'],
			'password': request.POST['password'],
			'creado': datetime.datetime.now().isoformat(),
			'needs': []
		}
		usuario = db.usuario.find_one({'email': request.POST['email']})
		if not usuario == None:
			return ajaxReturn({'status':'NO', 'mensaje': 'Correo ya está usuado'})

		db.usuario.insert(form_args)
		form_args['_id'] = str(form_args['_id'])

		return ajaxReturn({'status':'OK', 'usuario': form_args})
	else:
		return ajaxReturn({ 'status':'NO', 'form_errors': form.errors})

@csrf_exempt
def login(request):
	form = LoginForm(request.POST)

	if request.method == 'POST' and form.validate():
		u = db.usuario.find_one({'email': request.POST['email'], 'password': request.POST['password']})

		if u == None:
			return ajaxReturn({'status':'NO', 'mensaje':'Usuario no encontrado o contraseña inexistente'})

		u['_id'] = str(u['_id'])
		return ajaxReturn({'status':'OK', 'usuario':u })

	else:
		return ajaxReturn({'status':'NO', 'form_errors':form.errors})

@csrf_exempt
def addNeed(request):
	form = AddNeedForm(request.POST)

	if request.method == 'POST' and form.validate():
		u = db.usuario.find_one({'email':request.POST['usuario_email']})
		
		if u== None:
			return ajaxReturn({'status':'NO', 'mensaje':'Usuario no encontrado o contraseña inexistente'})
		
		if any(need['descripcion']==request.POST['descripcion'] for need in u['needs']):
			return ajaxReturn({'status':'NO', 'mensaje':'Item Duplicado'})

		u['needs'].append({
			'descripcion': request.POST['descripcion'],
			'tipo': request.POST['tipo']
		})

		db.usuario.save(u)
		db.usuario_consultado.update({'usuario_consultado': request.POST['usuario_email']}, {'$set': {'needs_consultados_actualizados': True}})

		return ajaxReturn({'status':'OK'})

	else:
		#return ajaxReturn({'status':'OK', 'mensaje':form.errors})
		return ajaxReturn({'status':'NO', 'form_errors':form.errors})


def testLibGeo(request):
	res = {
		'HD) Eliecer -> Montenegro: 220 - ':libGeo.harvesianDistance(-33.43461, -70.58308, -33.435987, -70.581212),
		'GD) Eliecer -> Montenegro: 220 - ':libGeo.distanciaGeodesica(-33.43461, -70.58308, -33.435987, -70.581212),
		'Eliecer cn  S. Juan -> Elicer con D de Almagro: 120 - ':libGeo.harvesianDistance(-33.43461, -70.58308, -33.435663, -70.583833),
	}

	return ajaxReturn(res)

def testSem(request):
	res = {
		'Entre \"hola a todos\" y \"holanda a todos\"': str(libGeo.getStringDiff('hola a todos', 'holanda a todos')),
		'Entre \"cafe" y "cafeta\"': str(libGeo.getStringDiff('cafe','cafeta')),
		'Entre \"profe" y "atleta\"': str(libGeo.getStringDiff('profe','atleta'))
	}
	return ajaxReturn(res)

'''
bilbao con tobalaba: -33.431887 - -70.584771
bilbao con sanches fontecilla: -33.431735 - -70.584050
tobalaba con pocuro: -33.430669 - -70.585839
'''

def refreshLocation(email, latitude, longitude):
	import time

	u = db.location.find_one({'email': email})
	if u == None:
		_id = db.location.insert({
			'email': email,
			'latitude': latitude,
			'longitude': longitude,
			'last_update': int(time.time())
		})
		return _id

	loc = db.location.find_one({'email': email})
	loc['latitude'] = latitude
	loc['longitude'] = longitude
	loc['last_update'] = int(time.time())

	db.location.save(loc)

	return str(loc['_id'])

#str x long x long => list[usuario(BSON)]
def getCloseUsers(email, latitude, longitude, distance):
	import time

	allLocations = db.location.find({'email': {'$nin': [email]}})

	closeUsers = []
	closeLocations = []
	current_time_stamp = int(time.time())
	
	for location in allLocations:

		if current_time_stamp - location['last_update'] < TIME_INTER_REFRESH: # case where tarjet user is actualizated
			
			if distance == 0:
				closeLocations.append(location)
			
			else:
				distanceFromLocation = libGeo.harvesianDistance(latitude, longitude, location['latitude'], location['longitude'])
				if distanceFromLocation <= distance:
					closeLocations.append(location)

	# get user of each location
	for closeLocation in closeLocations:
		user = db.usuario.find_one({'email': closeLocation['email']})
		closeUsers.append(user)

	return closeUsers


def getMatchesByNeeds(emailConsultor, closeUsers):
	''' Primero se obtienen los matches por usuario '''
	consultor = db.usuario.find_one({'email': emailConsultor})
	matches = list()

	for closeUser in closeUsers:

		matchesFromUser = getMatchedNeeds(consultor, closeUser)
		matches += matchesFromUser

	return matches

	''' Luego se ordenan por need '''
	# matchesByNeeds = dict()
	# for match in matches:
	# 	match_need_name = match['need_consultor_descripcion']

	# 	if not match_need_name in matchesByNeeds.keys():
	# 		matchesByNeeds[match_need_name] = list()

	# 	matchesByNeeds[match_need_name].append(match)

	# return matchesByNeeds


def getMatchedNeeds(consultor, consultado):
	''' Obtiene los matches entre dos usuarios '''
	matches = list()

	for needConsultor in consultor['needs']:

		for needConsultado in consultado['needs']:

			if libGeo.getStringDiff(needConsultor['descripcion'], needConsultado['descripcion']) > SIMILARITY:
				matches.append({
					'email_consultado': consultado['email'],
					'nombre_consultado': consultado['nombre'],
					'need_consultor_descripcion': needConsultor['descripcion'],
					'need_consultor_tipo': needConsultor['tipo'],
					'need_consultado_descripcion': needConsultado['descripcion'],
					'need_consultado_tipo': needConsultado['tipo']
				})
	return matches

# email x latitude x longitude x distance => {
# 	status: 'OK',
# 	matched_users: {
# 		nombre: String,
# 		email: String,
# 		latitude: long,
# 		longitude: long,
# 		new_matched_needs: [{
# 			id: int,
# 			descripcion: String,
# 			tipo: String,
# 			my_matched_needs:['Descripcion':String, ...]
# 		}...]
# 	}
# }
@csrf_exempt
def matches(request):
	form = MatchesForm(request.POST)

	if request.method == 'POST' and form.validate():

		email = request.POST['email']
		latitude = float(request.POST['latitude'])
		longitude = float(request.POST['longitude'])
		distance = int(request.POST['distance'])
		isOldLocation = refreshLocation(email, latitude, longitude)

		closeUsers = getCloseUsers(email, latitude, longitude, distance)
		matches = getMatchesByNeeds(email, closeUsers)

		return ajaxReturn({'status':'OK', 'matches':matches})    # the real
	
	else:
		return ajaxReturn({'status':'NO', 'forms_errors':form.errors})

'''
import time
from pymongo import MongoClient 
client = MongoClient('localhost')
db = client['nearudb']

'''