from django.conf.urls import patterns, url
from api import views

urlpatterns = patterns('',
	url(r'^$', views.index, name="index"),
	url(r'^dos/$', views.dos, name="dos"),
	url(r'^signup/$', views.signup, name="signup"),
	url(r'^login/$', views.login, name="login"),
	url(r'^add_need/$', views.addNeed, name="addNeed"),
	url(r'^testLibgeo/$', views.testLibGeo, name="testLibgeo"),
	url(r'^testSem/$', views.testSem, name="testSem"),
	url(r'^matches/$', views.matches, name="matches"),
	#url(r'^borrarMatches/$', views.borrarMatches, name="borrarMatches")
)