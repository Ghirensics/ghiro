# Ghiro - Copyright (C) 2013-2014 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

from ghiro.common import check_version
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_safe
from django.http import HttpResponse

@require_safe
@login_required
def update_check(request):
    """Checks for new version available."""
    try:
        new_version = check_version()
    except Exception:
        new_version = False

    return HttpResponse(new_version)