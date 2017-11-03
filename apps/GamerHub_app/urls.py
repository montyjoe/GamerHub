from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index)
    url(r'^$', views.index),
    url(r'^login$', views.login_page ),
    url(r'^register$', views.register_page ),
    url(r'^register_account$', views.register_account),
    url(r'^log_user_in$', views.log_user_in),
]
