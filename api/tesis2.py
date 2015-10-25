''' Función Principal de la API '''
def matches(request):
	form = MatchesForm(request.POST)
	if request.method == 'POST' and form.validate():
		# Obtener variables
		email = request.POST['email']
		latitude = float(request.POST['latitude'])
		longitude = float(request.POST['longitude'])
		distance = int(request.POST['distance'])

		# Actualiza la locacion
		db.location.update({'email': email},
						   {'latitude': latitude,
						   'longitude': longitude,
						   'last_update': int(time())},
						   {'upsert': True})

		closeUsers = getCloseUsers(email, latitude, longitude, distance)
		matched_users = getMatchedUsers(email, closeUsers)

		return ajaxReturn({'status':'OK', 'matched_users':matched_users})
	else:
		return ajaxReturn({'status':'NO', 'forms_errors':form.errors})


''' str x long x long => list[dict(location )*]
Retorna los usuarios más cercanos a la distancia dada
'''
def getCloseUsers(email, latitude, longitude, distance):
	allLocations = db.location.find({'email': notEqual(email)})
	# Todas las Locaciones excepto la del usuario

	closeUsers = []
	closeLocations = []
	now = int(time())
	
	for location in allLocations:
		if now - location['last_update'] < TIME_INTER_REFRESH: 
			# Si locacion está actualizada
			if distance == 0:
				closeLocations.append(location)
			else:
				distanceFromLocation = harvesianDistance(latitude,
														 longitude, 
														 location['latitude'], 
														 location['longitude'])
				if distanceFromLocation <= distance:
					# Si está a una distancia cercana, se guarda
					closeLocations.append(location)

	# Ahora se obtiene el usuario de cada Location
	for closeLocation in closeLocations:
		user = db.usuario.find_one({'email': closeLocation['email']})
		closeUsers.append(user)

	return closeUsers


''' str x list(dict[USERS]) => list(dict[USERS])
Retorna lista de los usuarios con los que hay calce 
'''
def getMatchedUsers(emailConsultor, closeUsers):
	consultor = db.usuario.find_one({'email': emailConsultor})
	matchedUsers = list()

	for closeUser in closeUsers:
		usuarioConsultado = db.usuario_consultado.find_one({'consultor': emailConsultor, 
														    'consultado': closeUser['email']})
		if usuarioConsultado == None:
			# Si usuarios no se han visto aún
			consultado = db.usuario.find_one({'email': emailConsultor})
			if hasMatches(consultor, consultado):
				# Si tiene al menos 1 match

				matchedUsers.append(closeUser)
				db.usuario_consultado.insert({'consultor': emailConsultor,
											  'consultado': closeUser['email'],
											  'needs_matched': True,
											  'needs_updated': False })
			else:
				# Si no hay matches
				db.usuario_consultado.insert({'consultor': emailConsultor,
											  'consultado': closeUser['email'],
											  'needs_matched': False,
											  'needs_updated': False })
		else:
			# Usuarios ya se han visto antes
			if usuarioConsultado['needs_matched']:
				# Si usuarios ya tienen un match previo
				matchedUsers.append(closeUser)
			elif usuarioConsultado['needs_updated']:
				# No existe match previo, pero "consultado" actualizo sus needs
				consultado = db.usuario.find_one({'email': closeUser['email']})

				if hasMatches(consultor, consultado):
					matchedUsers.append(closeUser)
					usuarioConsultado['needs_matched'] = True
	return matchedUsers


def hasMatches(consultor, consultado):
for myNeed in consultor['needs']:
	for otherNeed in consultado['needs']:
		if stringDiff(myNeed['descripcion'],otherNeed['descripcion']) > SIMILARITY:
			return True
return False