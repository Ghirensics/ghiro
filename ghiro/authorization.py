# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

from users.models import Profile

def api_authenticate(api_key):
    """Authenticate users via API key.
    @param api_key: API key for authentication
    @return: authenticated user instance
    @raise: PermissionDenied if API key is not valid
    """
    if api_key:
        try:
            return Profile.objects.get(api_key=api_key)
        except ObjectDoesNotExist:
            raise PermissionDenied
    else:
        raise PermissionDenied