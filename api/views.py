# Ghiro - Copyright (C) 2013-2014 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import json
import analyses.forms as forms

from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

from ghiro.common import log_activity, mongo_connect, check_allowed_content
from ghiro.authorization import api_authenticate
from analyses.models import Case

@require_POST
@csrf_exempt
def new_case(request):
    """Creates a new case."""
    user = api_authenticate(request.POST.get("api_key"))

    if request.POST.get("name"):
        case = Case(name=request.POST.get("name"),
                    description=request.POST.get("description"),
                    owner=user)
        case.save()

        # Auditing.
        log_activity("C",
                     "Created new case via API {0}".format(case.name),
                     request,
                     user)

        response_data = {"id": case.id}
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponse("Request not valid", status=400)