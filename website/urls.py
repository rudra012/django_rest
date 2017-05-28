from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'website/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),

    url(r'^$', views.index),
    url(r'^accounts/login/$', views.login),
    url(r'^accounts/social-login/$', views.social_login),
    url(r'^accounts/logout/$', views.logout),
    url(r'^registration/$', views.register),
    url(r'^registration/success/$', views.register_success),
    url(r'^home/$', views.home),
]
