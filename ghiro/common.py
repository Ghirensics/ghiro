# Ghiro - Copyright (C) 2013-2014 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import json
import urllib
import urllib2

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.conf import settings

from users.models import Activity
from manage.models import UpdateCheck


def log_activity(category, message, request, user=None):
    """Logs an activity for auditing.
    @param category: message category (see model)
    @param message: message description
    @param request: request object
    @param user: optional user instance
    """

    # Get forwarded for if exists.
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        forwarded_for_ip = x_forwarded_for.split(",")[0]
    else:
        forwarded_for_ip = None

    # Fetch user from request object.
    if not user:
        user = request.user

    # Log.
    Activity.objects.create(category=category,
        message=message,
        user=user,
        source_ip=request.META.get("REMOTE_ADDR"),
        forwarded_for_ip=forwarded_for_ip)

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

def check_version():
    """Checks version of Ghiro."""

    # Do i have to check?
    if UpdateCheck.should_check():

        # Create new check entry.
        check = UpdateCheck.objects.create()

        # Format request.
        url = "http://update.getghiro.org/update/check/"
        data = urllib.urlencode({"version": settings.GHIRO_VERSION})

        try:
            request = urllib2.Request(url, data)
            response = urllib2.urlopen(request)
        except (urllib2.URLError, urllib2.HTTPError) as e:
            check.state = "E"
            check.save()
            raise Exception("Unable to establish connection: %s" % e)

        try:
            data = json.loads(response.read())
        except ValueError:
            check.state = "E"
            check.save()
            raise Exception("Invalid response.")

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
