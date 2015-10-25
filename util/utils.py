# -*- coding: utf-8 -*-
import random
import time
import string
import sys
import os
import json
import datetime

sys.path.append('~/proyectosDjango/pymongoserver')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pymongoserver.settings')

from bson.objectid import ObjectId
from pymongo import MongoClient
client = MongoClient('localhost', 27017)

db = client['nearudb']


def getEmails(num):
	emails = list()
	i = 0
	while i < num:
		emailName = ''.join(random.choice( string.ascii_letters + string.digits) for j in xrange(8))
		emailDomain = random.choice(['gmail.com', 'yahoo.es', 'outlook.com', 'dcc.uchile.cl', 'interior.gob.cl'])
		
		email = emailName+'@'+emailDomain

		if not email in emails:
			emails.append(email)
			i+=1

	return emails

def getNames():
	f = open('nombres.list', 'r')
	nombres = [line.decode(encoding='UTF-8')[:-1] for line in f]
	f.close()
	return nombres

def getNeeds():
	f = open('needs.list', 'r')
	needs = [line.decode(encoding='UTF-8')[:-1] for line in f]
	f.close()
	return needs

# invoke from console to create users
def generateUsers(numUsers, numNeedsUser):

	names = getNames()
	needsDescriptions = getNeeds()
	emails = getEmails(numUsers)

	fileOut = open('usuarios_creados.list','w')
	
	for i in xrange(numUsers):

		nombre = random.sample(names, 1)[0]

		usuario = {'nombre': nombre, 'email': emails[i], 'password': '12345', 'needs':[]}
		fileOut.write(emails[i]+'\n')

		# ahora se setean sus needs
		j=0
		descripciones = list()

		while j < numNeedsUser:
			descripcion = random.sample(needsDescriptions, 1)[0]

			if not descripcion in descripciones:

				descripciones.append(descripcion)
				usuario['needs'].append({'descripcion': descripcion, 'tipo': 'need'})
				j += 1

		db.usuario.insert(usuario)

	fileOut.close()
	print str(numUsers)+" USUARIOS GENERADOS"

def main():
	import pdb; pdb.set_trace()
	print "FIN DEL SCRIPT"

if __name__ == '__main__':
	random.seed(time.time())
	main()

'''
DELETE
FROM api_need                      [ HOY ]
WHERE DATE(fecha_creacion) BETWEEN '2014-06-28' AND '2015-08-10'

DELETE
FROM api_usuario                   [ HOY ]
WHERE DATE(fecha_registro) BETWEEN '2014-06-28' AND '2015-08-10'
'''