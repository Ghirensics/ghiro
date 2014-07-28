# Ghiro - Copyright (C) 2013-2014 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

from django.conf.urls import patterns, url

urlpatterns = patterns("",
    url(r"^cases/new$", "api.views.new_case"),
    url(r"^images/new$", "api.views.new_image"),
)
