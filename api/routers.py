# -*- coding: utf-8 -*-
"""
This urls.py is for all API related URLs.

URL Naming Pattern (lowercased & underscored)
<app_name>_<model_name> or
<app_name>_<specific_action>

For base name use:
<app_name>
"""

from rest_framework import routers

from api.snippets import snippets_api
from api.users import user_api

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'auth', user_api.AuthViewSet, base_name='auth')
router.register(r'me', user_api.CurrentUserViewSet, base_name='me')
router.register(r'snippets', snippets_api.SnippetList, base_name='api_snippet_list')
# router.register(r'snippets/(?P<pk>[0-9]+)', snippets_api.SnippetDetail, base_name='api_snippet_detail')
