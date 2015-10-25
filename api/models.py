#from django.db import models
# Create your models here.
from pymongo import MongoClient
client = MongoClient('localhost', 27017)

db = client['nearudb']

'''from pymongo.son_manipulator import SONManipulator
class ObjectIdManipulator(SONManipulator):
    def transform_incoming(self, son, collection):
        son[u'_id'] = str(son[u'_id'])      
        return son

db.add_son_manipulator(ObjectIdManipulator())'''

