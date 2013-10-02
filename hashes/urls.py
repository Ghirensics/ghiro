# Ghiro - Copyright (C) 2013 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

from django.conf.urls import patterns, url

urlpatterns = patterns("",
    url(r"^index/$", "hashes.views.list_hashes"),
    url(r"^new/", "hashes.views.new_hashes"),
    url(r"^show/(?P<list_id>[\d]+)/", "hashes.views.show_hashes"),
    url(r"^delete/(?P<list_id>[\d]+)/", "hashes.views.delete_hashes"),
)