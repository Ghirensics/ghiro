# Ghiro - Copyright (C) 2013-2016 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

from django.conf.urls import patterns, url, include
from django.contrib.auth import views as auth_views

urlpatterns = patterns("",
    (r"^login/$", "django.contrib.auth.views.login", {"template_name": "users/login.html"}),
    (r"^logout/$", "django.contrib.auth.views.logout", {"next_page": "/"}),
    (r"^profile/$", "users.views.profile"),
    (r"^password_change/$", "django.contrib.auth.views.password_change", {"template_name": "users/password_change.html"}),
    (r"^password_change_done/$", "django.contrib.auth.views.password_change_done" ,{"template_name": "users/password_change_done.html"}, "password_change_done"),

    # Admin
    (r"^management/index/$", "users.views.admin_list_users"),
    (r"^management/activity/$", "users.views.admin_list_activity"),
    (r"^management/new/$", "users.views.admin_new_user"),
    (r"^management/show/(?P<user_id>[\d]+)/$", "users.views.admin_show_user"),
    (r"^management/show/(?P<user_id>[\d]+)/activity/$", "users.views.admin_show_activity"),
    (r"^management/edit/(?P<user_id>[\d]+)/$", "users.views.admin_edit_user"),
    (r"^management/disable/(?P<user_id>[\d]+)/$", "users.views.admin_disable_user"),
)