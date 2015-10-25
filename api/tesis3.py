''' str x long x long => list[dict(location )*]
Retorna los usuarios más cercanos a la distancia dada
'''
def getCloseUsers(*kwargs):
	# se realiza llamado a servidor NodeJS
	closeLocations = json.loads(requests.post('localhost:5000/close_users', kwargs))

	# Ahora se obtiene el usuario de cada Location
	for closeLocation in closeLocations:
		user = db.usuario.find_one({'email': closeLocation['email']})
		closeUsers.append(user)

	return closeUsers
