from django.conf.urls import url

from api.snippets import snippets_api

urlpatterns = [
    url(r'^$', snippets_api.snippet_list),
    url(r'^(?P<pk>[0-9]+)/$', snippets_api.snippet_detail),
]

