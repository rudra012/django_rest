# -*- coding: utf-8 -*-

import uuid

URL_TEMPLATE = "{scheme}://{domain}/{path}"


def get_uuid_from_query_params(request, param):
    """
        return uuid from a given queryset after parsing it.
    """
    param_field = request.query_params.get(param, None)
    if param_field:
        try:
            return uuid.UUID(param_field)
        except ValueError:
            return None
    return None
