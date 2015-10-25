# -*- coding: utf-8 -*-
''' python manage.py shell < mitest.py '''
''' sudo netstat -lpn |grep :8080 '''

import sys
import os
sys.path.append('/home/matias/proyectosDjango/pymongoServer')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pymongoServer.settings')

from api.models dbm
import timezone
import json

def testUsuarios():
    # primer usuario
    u1 = Usuario(nombre="Mati", email="mbensan@gmail.com", password="12345", fecha_registro=timezone.now())
    u1.fecha_modificacion = timezone.now()


    try:
        u1.save()
        print u1.__unicode__()+' guardado.'
    except IntegrityError:
        print "Mail "+u1.email+" duplicado"


    #segundo usuario
    u2 = Usuario(nombre="Juan Perez", email="jperez@gmail.com", password="76543", fecha_registro=timezone.now())
    u2.fecha_modificacion = timezone.now()
    u2.fecha_ultimo_login = timezone.now()

    try:
        u2.save()
        print u2.__unicode__()+' guardado.'
    except IntegrityError:
        print "Mail "+u2.email+" duplicado"

    #tercer usuario
    u3 = Usuario(nombre="Rhida", email="rhidi@gmail.com", password="12345")
    u3.fecha_modificacion = timezone.now()


    try:
        u3.save()
        print u3.__unicode__()+' guardado.'
    except IntegrityError:
        print "Mail "+u3.email+" duplicado"

    #cuarto usuario
    u4 = Usuario(nombre="Synaptic", email="synaptic@gmail.com", password="12345")
    u4.fecha_modificacion = timezone.now()


    try:
        u4.save()
        print u4.__unicode__()+' guardado.'
    except IntegrityError:
        print "Mail "+u4.email+" duplicado"


    print Usuario.objects.all()

    #añadiendo needs a usuario un
    print 'Añadiendo needs al usuario '+u1.__unicode__()


    # recuperar usuarios
    if u1.pk == None:
        u1 = Usuario.objects.get(email=u1.email)
    if u2.pk == None:
        u2 = Usuario.objects.get(email=u2.email)
    if u3.pk == None:
        u3 = Usuario.objects.get(email=u3.email)

def testNeeds():
    needs = {
        'mbensan@gmail.com': ['Clases de Salsa', 'Partido Futbol', 'Desarrollo de Software'],
        'jperez@gmail.com': ['Clases de Ajedrez', 'Compraventa de ropa', 'Desarrollo Software'],
        'rhidi@gmail.com': ['Clases de Salsas', 'Compraventa ropa', 'Quimicos Indistriales'],
        'synaptic@gmail.com': ['Desarrollo software', 'Escalabilidad', 'Kanban', 'Asados mundiales']
    }
    # recuperar usuarios
    u1 = Usuario.objects.get(email='mbensan@gmail.com')
    u2 = Usuario.objects.get(email='jperez@gmail.com')
    u3 = Usuario.objects.get(email='rhidi@gmail.com')
    u4 = Usuario.objects.get(email="synaptic@gmail.com")

    #import pdb; pdb.set_trace()

    #añadir necesidades
    for need in needs[u1.email]:
        try:
            need_u1 = u1.need_set.get(descripcion=need)
            print "YA EXISTE el need "+need+" para el usuario "+u1.email
        except Need.DoesNotExist:
            u1.need_set.create(descripcion=need)
            print "CREADO el need "+need+" para el usuario "+u1.email

    for need in needs[u2.email]:
        try:
            need_u2 = u2.need_set.get(descripcion=need)
            print "YA EXISTE el need "+need+" para el usuario "+u2.email
        except Need.DoesNotExist:
            u2.need_set.create(descripcion=need)
            print "CREADO el need "+need+" para el usuario "+u2.email

    for need in needs[u3.email]:
        try:
            need_u3 = u3.need_set.get(descripcion=need)
            print "YA EXISTE el need "+need+" para el usuario "+u3.email
        except Need.DoesNotExist:
            u3.need_set.create(descripcion=need)
            print "CREADO el need "+need+" para el usuario "+u3.email

    for need in needs[u4.email]:
        try:
            need_u4 = u4.need_set.get(descripcion=need)
            print "YA EXISTE el need "+need+" para el usuario "+u4.email
        except Need.DoesNotExist:
            u4.need_set.create(descripcion=need)
            print "CREADO el need "+need+" para el usuario "+u4.email

    #todos los needs
    print " "
    print 'Todos los '+str(u1.need_set.count())+' needs de '+u1.email
    print u1.need_set.all()

    print "Acceder a un Usuario desde un need"
    primerNeed = u1.need_set.all()[0] # accede al usuario primerNeed.usuario.email
    import pdb; pdb.set_trace()


def main():
    print "Testing de Usuarios:"
    testUsuarios()
    testNeeds()

if __name__ == '__main__':
    main()