# -*- coding: utf-8 -*-

import hashlib
import logging
import random
import sys

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.template import RequestContext, TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token

from base import exceptions as exc

user_model = get_user_model()
log = logging.getLogger(__name__)


# current_site = get_current()


def get_token_for_user(user):
    """
    Generate a new signed token containing
    a specified user limited for a scope (identified as a string).
    """
    return str(Token.objects.get_or_create(user=user)[0])


# def get_user_for_token(token, scope):
#     """
#     Given a self-contained token and a scope try to parse and
#     unsign it.
#
#     If max_age is specified it checks token expiration.
#
#     If token passes a validation, returns
#     a user instance corresponding with user_id stored
#     in the incoming token.
#     """
#     try:
#         data = jwt.decode(token, settings.SECRET_KEY)
#     except jwt.DecodeError:
#         raise exc.NotAuthenticated("Invalid request. Please retry.")
#
#     try:
#         user = user_model.objects.get(pk=data["user_%s_id" % (scope)])
#     except (user_model.DoesNotExist, KeyError):
#         raise exc.NotAuthenticated("Invalid request. Please retry.")
#     else:
#         return user


def get_authenticated_active_user(username_or_email=None, password=None):
    if (not username_or_email) and (not password):
        raise exc.BadRequest(_("Missing required credentials."))

    users = get_user_model().objects.filter(Q(email=username_or_email) | Q(username=username_or_email))
    if users.count() > 1:
        raise exc.BadRequest(_('Multiple Users with same email, contact support!'))
    elif users.count() == 1:
        user = authenticate(email=users.first().email, password=password)

        if not user:
            raise exc.WrongArguments(_("Unable to login with provided credentials."))

        # Did we get active user?
        if not user.is_active:
            raise exc.PermissionDenied(_("Please Verify Account Email Address."))

        return user
    else:
        raise exc.WrongArguments(_("Unable to login with provided credentials."))


def generate_activation_key(user):
    """
    The activation key for the ``User`` will be a
    SHA1 hash, generated from a combination of the ``User``'s
    pk and a random salt.
    """
    salt = hashlib.sha1(six.text_type(random.random())
                        .encode('ascii')).hexdigest()[:5]
    salt = salt.encode('ascii')
    user_pk = str(user.pk)
    if isinstance(user_pk, six.text_type):
        user_pk = user_pk.encode('utf-8')
    activation_key = hashlib.sha1(salt + user_pk).hexdigest()
    # UserActivationKey.objects.update_or_create(
    #     user=user,
    #     defaults={'activation_key': activation_key}
    # )
    return activation_key


def send_mail(subject_template_name, email_template_name,
              context, to_email, html_email_template_name=None, request=None):
    """
    Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
    """
    ctx_dict = {}
    if request is not None:
        ctx_dict = RequestContext(request, ctx_dict)
    # update ctx_dict after RequestContext is created
    # because template context processors
    # can overwrite some of the values like user
    # if django.contrib.auth.context_processors.auth is used
    if context:
        ctx_dict.update(context)
    ctx_dict.update({
        # 'site': current_site,
    })
    subject = (render_to_string(subject_template_name, ctx_dict))
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL')
    message_txt = render_to_string(email_template_name,
                                   ctx_dict)

    email_message = EmailMultiAlternatives(subject, message_txt,
                                           from_email, [to_email])

    if html_email_template_name:
        try:
            message_html = render_to_string(
                html_email_template_name, ctx_dict)
            email_message.attach_alternative(message_html, 'text/html')
        except TemplateDoesNotExist:
            pass
    try:
        email_message.send()
    except:
        if settings.DEBUG:
            print(sys.exc_info())


def get_active_users(email):
    """
    Given an email, return matching user(s) who should receive a reset.
    """
    active_users = user_model._default_manager.filter(
        email__iexact=email, is_active=True)
    return (u for u in active_users if u.has_usable_password())
