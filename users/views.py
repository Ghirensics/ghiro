# Ghiro - Copyright (C) 2013-2014 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_safe
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from users.models import Profile, Activity
from ghiro.common import log_activity

import users.forms as forms

@require_safe
@login_required
def profile(request):
    """User's profile."""
    # Set sidebar no active tab.
    request.session["sidebar_active"] = None

    return render_to_response("users/profile.html",
                              context_instance=RequestContext(request))

@require_safe
@login_required
def admin_list_users(request):
    """Show users list."""

    # Set sidebar active tab.
    request.session["sidebar_active"] = "side-admin"

    # Security check.
    if not request.user.is_superuser:
        return render_to_response("error.html",
                                  {"error": "You must be superuser"},
                                  context_instance=RequestContext(request))

    users = Profile.objects.all()

    return render_to_response("admin/index.html",
                              {"users": users},
                              context_instance=RequestContext(request))

@login_required
def admin_new_user(request):
    """Create new users."""

    # Security check.
    if not request.user.is_superuser:
        return render_to_response("error.html",
                                  {"error": "You must be superuser"},
                                  context_instance=RequestContext(request))

    if request.method == "POST":
        form = forms.ProfileCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Auditing.
            log_activity("A",
                         "Created new user %s" % user.username,
                         request)
            return HttpResponseRedirect(reverse("users.views.admin_show_user", args=(user.id,)))
    else:
        form = forms.ProfileCreationForm()

    return render_to_response("admin/new_user.html",
                              {"form": form},
                              context_instance=RequestContext(request))

@login_required
def admin_show_user(request, user_id):
    """Show user details."""

    # Security check.
    if not request.user.is_superuser:
        return render_to_response("error.html",
                                  {"error": "You must be superuser"},
                                  context_instance=RequestContext(request))

    user = get_object_or_404(Profile, pk=user_id)

    return render_to_response("admin/show_user.html",
                              {"user": user},
                              context_instance=RequestContext(request))

@login_required
def admin_edit_user(request, user_id):
    """Edit user."""

    # Security check.
    if not request.user.is_superuser:
        return render_to_response("error.html",
                                  {"error": "You must be superuser"},
                                  context_instance=RequestContext(request))

    user = get_object_or_404(Profile, pk=user_id)

    if request.method == "POST":
        form = forms.ProfileForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            # Auditing.
            log_activity("A",
                         "Edited user %s" % user.username,
                         request)
            return HttpResponseRedirect(reverse("users.views.admin_show_user", args=(user.id,)))
    else:
        form = forms.ProfileForm(instance=user)

    return render_to_response("admin/edit_user.html",
                              {"form": form, "user": user},
                              context_instance=RequestContext(request))

@login_required
def admin_disable_user(request, user_id):
    """Disable user."""

    # Security check.
    if not request.user.is_superuser:
        return render_to_response("error.html",
                                  {"error": "You must be superuser"},
                                  context_instance=RequestContext(request))

    user = get_object_or_404(Profile, pk=user_id)

    if request.user == user:
        return render_to_response("error.html",
                                  {"error": "You can not disable yourself"},
                                  context_instance=RequestContext(request))

    user.is_active = False
    user.save()
    # Auditing.
    log_activity("A",
                 "Disabled user %s" % user.username,
                 request)

    return HttpResponseRedirect(reverse("users.views.admin_list_users"))

@login_required
def admin_list_activity(request):
    """Activity index."""

    # Security check.
    if not request.user.is_superuser:
        return render_to_response("error.html",
                                  {"error": "You must be superuser"},
                                  context_instance=RequestContext(request))

    activities = Activity.objects.all()

    return render_to_response("admin/activity.html",
                              {"activities": activities},
                              context_instance=RequestContext(request))

@login_required
def admin_show_activity(request, user_id):
    """Show user activity."""

    # Security check.
    if not request.user.is_superuser:
        return render_to_response("error.html",
                                  {"error": "You must be superuser"},
                                  context_instance=RequestContext(request))

    user = get_object_or_404(Profile, pk=user_id)
    activities = Activity.objects.filter(user=user)

    return render_to_response("admin/user_activity.html",
                              {"activities": activities},
                              context_instance=RequestContext(request))