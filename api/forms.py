from wtforms import Form, StringField, validators, IntegerField
import wtforms.ext.i18n.form as iform

''' validators '''
def appIdValidator(form, field):
	if field.data != '12':
		raise validators.ValidationError('Error de Verificacion de Autenticidad de la Aplicacion')

def tipoNeedValidator(form, field):
	if not field.data in ['wish', 'do', 'share']:
		raise validators.ValidationError('Need de Tipo no Existente')

def isNumValidator(form, field):
	#import pdb; pdb.set_trace()
	try:
		float(field.data)
		return True
	except ValueError:
		return False
	return False

''' Forms /home/matias/.virtualenvs/nearuEnv/lib/python2.7/site-packages/wtforms/ext/i18n/form/Form '''

class BaseForm():
	pass


class RegisterForm(iform.Form):
	nombre = StringField('nombre', [
		validators.Length(min=4, max=25)
	])
	email = StringField('email', [
		validators.Length(min=4, max=50),
		validators.Email()
	])
	password = StringField('password', [
		validators.Length(min=4, max=25)
	])
	password_conf = StringField('password_conf', [
		validators.Length(min=4, max=25),
		validators.EqualTo('password')
	])
	app_id = StringField('app_id', [
		validators.Required(),
		appIdValidator
	])

class LoginForm(iform.Form):
	email = StringField('email', [
		validators.Length(min=4, max=50),
		validators.Email()
	])
	password = StringField('password', [
		validators.Length(min=4, max=25)
	])
	app_id = StringField('app_id', [
		validators.Required(),
		appIdValidator
	])

class AddNeedForm(iform.Form):
	usuario_email = StringField('usuario_email', [
		validators.Length(min=4, max=50),
		validators.Email()
	])
	descripcion = StringField('descripcion', [
		validators.Length(min=5, max=50)
	])
	tipo = StringField('tipo', [
		validators.Length(min=1, max=5),
		tipoNeedValidator
	])
	app_id = StringField('app_id', [
		validators.Required(),
		appIdValidator
	])

class MatchesForm(iform.Form):
	email = StringField('email', [
		validators.Length(min=4, max=50),
		validators.Email()
	])
	latitude = StringField('latitude', [
		validators.Required(),
		isNumValidator
	])
	longitude = StringField('longitude', [
		validators.Required(),
		isNumValidator
	])
	app_id = StringField('app_id', [
		validators.Required(),
		appIdValidator
	])
	distance = IntegerField('distance', [
		validators.Required()
	])



