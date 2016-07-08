from django.conf.urls import url

from . import views

app_name = 'polls'

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),


    #Åben og Luk
    url(r'^Aaben/(?P<event_id>[0-9]+)/$', views.aaben, name='aaben'),
    url(r'^Luk/', views.luk, name='luk'),
    url(r'^aabenhistorik/', views.aabenhistorik, name='aabenhistorik'),
    
    #Priser
    url(r'^priser/(?P<event_id>[0-9]+)/$', views.prislister, name='prislister'),
    #url(r'^priser/(?P<pk>[0-9]+)/$', views.prislisteView.as_view(), name='prislister'),
    url(r'^prisskift/(?P<event_id>[0-9]+)/$', views.prisskift, name='prisskift'),
    
    
    #Varemodtagelse
    url(r'^modtagelser/ny/', views.nymodtagelse, name='nymodtagelse'),
    url(r'^modtagelser/historik/', views.modtagehistorik, name='modtagehistorik'),
    
    #event urls
    #url(r'^events/(?P<pk>)', views.EventsView.as_view(), name='events'),
    url(r'^events/skabny/', views.createevent, name='createevent'),
    
    url(r'^events/(?P<event_id>[0-9]+)/$', views.eventdetail, name='eventdetail'),
    url(r'^eventpriser/(?P<event_id>[0-9]+)/$', views.eventpriser, name='eventpriser'),
    url(r'^events/historik/', views.eventhistory, name='eventhistory'),
    url(r'^events/slet/(?P<event_id>[0-9]+)/$', views.eventdelete, name='eventdelete'), 
    url(r'^events/', views.events, name='events'),
    
    
    #wares urls
    #url(r'^detail/(?P<pk>[0-9]+)$', views.WareView.as_view(), name='detail2'),
    url(r'^(?P<wares_id>[0-9]+)/$', views.detail, name='detail'),
    #url(r'^(?P<pk>[0-9]+)/$', views.WareDetailView.as_view(), name='detail'),
    url(r'^hisnavn/', views.hisnavn, name='hisnavn'),
    url(r'^hisvareantal/', views.hisvareantal, name='hisvareantal'),
    url(r'^hisvarepriser/', views.hisvarepriser, name='hisvarepriser'),
    url(r'^skab_vare/', views.createware, name='skab_vare'),
    url(r'^slet_vare/(?P<wares_id>[0-9]+)/$', views.waredelete, name='waredelete'), 
    
    #Waregroups
    url(r'^varegruppe/(?P<wg_id>[0-9]+)/$', views.wgdetail, name='wgdetail'),
    url(r'^skab_varegruppe/', views.createwg, name='skab_varegruppe'),
    url(r'^wgpris/(?P<wg_id>[0-9]+)/$', views.wgpris, name='wgpris'),
    url(r'^slet_varegruppe/(?P<wg_id>[0-9]+)/$', views.waregroupdelete, name='waregroupdelete'), 

    
    #test of forms
    url(r'^test/', views.get_name, name='get_name'),
    ]

