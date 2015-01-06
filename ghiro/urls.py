# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

from django.conf.urls import patterns, include, url

urlpatterns = patterns("",
    url(r"^$", "analyses.views.dashboard"),
    (r"^users/", include("users.urls")),
    (r"^analyses/", include("analyses.urls")),
    (r"^hashes/", include("hashes.urls")),
    (r"^manage/", include("manage.urls")),
    (r"^api/", include("api.urls")),
)
