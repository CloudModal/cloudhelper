#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: middleware.py
@ide: PyCharm
@time: 2019/12/19 16:35
@desc:
"""
from django.conf import settings
from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import BACKEND_SESSION_KEY

from common.utils import get_logger
from .utils import new_client
from .models import OIDT_ACCESS_TOKEN

BACKEND_OPENID_AUTH_CODE = 'OpenIDAuthorizationCodeBackend'
logger = get_logger(__file__)
__all__ = ['OpenIDAuthenticationMiddleware']


class OpenIDAuthenticationMiddleware(MiddlewareMixin):
    """
    Check openid user single logout (with access_token)
    """
    @staticmethod
    def process_request(request):
        # Don't need openid auth if AUTH_OPENID is False
        if not settings.AUTH_OPENID:
            return
        # Don't need openid auth if no shared session enabled
        if not settings.AUTH_OPENID_SHARE_SESSION:
            return
        # Don't need check single logout if user not authenticated
        if not request.user.is_authenticated:
            return
        elif not request.session[BACKEND_SESSION_KEY].endswith(
                BACKEND_OPENID_AUTH_CODE):
            return
        # Check openid user single logout or not with access_token
        try:
            client = new_client()
            client.get_userinfo(token=request.session.get(OIDT_ACCESS_TOKEN))
        except Exception as e:
            logout(request)
            logger.error(e)
