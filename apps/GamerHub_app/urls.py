from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login_page ),
    url(r'^register$', views.register_page ),
    url(r'^register_account$', views.register_account),
    url(r'^log_user_in$', views.log_user_in),
    url(r'^logout$', views.logout),
    url(r'^profile$', views.profile),
    url(r'^createProfile$', views.createProfile),
    url(r'^editProfile$', views.editProfile),
    url(r'^newProfilePicture$', views.newProfilePicture),
    url(r'^editProfilePicture$', views.editProfilePicture),
    url(r'^searchGame$', views.searchGame),
    url(r'^search/$', views.search),
    url(r'^addGame/(?P<id>\d+)/(?P<name>[\w|\W]+)$', views.addGame),
    url(r'^delete/(?P<id>\d+)$', views.deleteGame),
]
