# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_safe
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from ghiro.common import check_version
from lib.utils import deps_check


@require_safe
@login_required
def update_check(request):
    """Checks for new version available."""
    try:
        new_version = check_version()
    except Exception:
        new_version = False

    return HttpResponse(new_version)

@require_safe
@login_required
def dependencies_list(request):
    return render_to_response("admin/dependencies.html",
                              {"dependencies": deps_check()},
                              context_instance=RequestContext(request))