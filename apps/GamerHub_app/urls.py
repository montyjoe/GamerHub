from django.conf.urls import url
from . import views           # This line is new!
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
         # This line has changed!
]
