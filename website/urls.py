from django.contrib.auth.views import login
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', login),
    # url(r'^logout/$', logout_page),
    # url(r'^accounts/login/$', 'django.contrib.auth.views.login'),  # If user is not login it will redirect to login page
    url(r'^register/$', views.register),
    # url(r'^register/success/$', register_success),
    url(r'^home/$', views.home),
]
