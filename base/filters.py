# -*- coding: utf-8 -*-

from rest_framework import filters

from base.utils.urls import get_uuid_from_query_params


class UserFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = get_uuid_from_query_params(request, 'user')

        if user is not None:
            return queryset.filter(user=user)
        return queryset
