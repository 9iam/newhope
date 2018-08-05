from django.conf.urls import url

from . import views

urlpatterns = [
    url('^$', views.wikitranslator),
    url('^translator/$', views.wikitranslator),
    url('^translator/(?P<req>\w+)$', views.wikitranslator),
    url('^translator/(?P<fromlang>\w+)/(?P<tolang>\w+)$', views.wikitranslator),
    url('^translator/(?P<fromlang>\w+)/(?P<tolang>\w+)/(?P<req>\w+)$', views.wikitranslator),
    url('^translatorlist/$', views.wikitranslatorlist),
    url('^translatorlist/(?P<fromlang>\w+)/(?P<tolang>\w+)$', views.wikitranslatorlist),
    url('^translatorlist/(?P<fromlang>\w+)/(?P<tolang>\w+)/(?P<req>\w+)$', views.wikitranslatorlist),    
    url('^perevod/$', views.wikiperevod),
    url('^perevod/(?P<req>\w+)$', views.wikiperevod),

]
