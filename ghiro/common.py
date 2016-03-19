# Ghiro - Copyright (C) 2013-2016 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import json
import logging
import requests

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.conf import settings

from users.models import Activity
from system.models import UpdateCheck

logger = logging.getLogger("audit")


def log_activity(category, message, request=None, user=None):
    """Logs an activity for auditing.
    @param category: message category (see model)
    @param message: message description
    @param request: optional request object
    @param user: optional user instance
    """

    # Skip if auditing is not enabled.
    if not settings.AUDITING_ENABLED:
        return

    # In local submissions the request object could be missing.
    if request:
        # Get forwarded for if exists.
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            forwarded_for_ip = x_forwarded_for.split(",")[0]
        else:
            forwarded_for_ip = None

        # Fetch user from request object.
        if not user:
            user = request.user

        ip = request.META.get("REMOTE_ADDR")
    else:
        ip = "127.0.0.1"
        user = None
        forwarded_for_ip = None

    # Log.
    Activity.objects.create(category=category,
        message=message,
        user=user,
        source_ip=ip,
        forwarded_for_ip=forwarded_for_ip)

    # Log sto standard log.
    logger.info('"%s" "%s" "%s"', ip, user, message)

def log_logon(sender, user, request, **kwargs):
    """Logs user logons."""
    log_activity("A", "User logon for %s" % user.username, request)

def log_logout(sender, user, request, **kwargs):
    """Logs user logouts."""
    log_activity("A", "User logout for %s" % user.username, request)

user_logged_in.connect(log_logon)
user_logged_out.connect(log_logout)

def check_allowed_content(content_type):
    """Check if a content type is allowed to be scanned.
    @param content_type: content type in MIME format
    @return: boolean test result
    """
    if content_type in settings.ALLOWED_EXT:
        return True
    else:
        return False

def check_version(url="https://update.getghiro.org/update/check/", force=False):
    """Checks version of Ghiro.
    It connects to Ghiro update website to check if a new release is available.
    You can optionally disable this via configuration file.
    @param url: update service URL
    @param force: force update check
    @return: boolean status of update available
    """

    # Do i have to check? It checks only out of a time frame.
    # Disable with "UPDATE_CHECK" option in configuration file.
    if (UpdateCheck.should_check() and settings.UPDATE_CHECK) or force:

        # Create new check entry.
        check = UpdateCheck.objects.create()

        # Format request.
        data = {"version": settings.GHIRO_VERSION}
        headers = {"User-Agent": "Ghiro update client"}
        try:
            request = requests.post(url, data=data, headers=headers, verify=True)
            response = request.text
        except requests.exceptions.RequestException as e:
            check.state = "E"
            check.save()
            raise Exception("Unable to establish connection: %s" % e)

        try:
            data = json.loads(response)
        except ValueError as e:
            check.state = "E"
            check.save()
            raise Exception("Invalid response: %s" % e)

        if data["new_release"]:
            check.state = "A"
            check.save()
            return True
        else:
            check.state = "N"
            check.save()
            return False
    else:
        return False
