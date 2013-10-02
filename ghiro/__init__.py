# Ghiro - Copyright (C) 2013 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

from pymongo import GEO2D

from ghiro.common import mongo_connect
# Mongo connection.
db = mongo_connect()

# Indexes.
db.fs.files.ensure_index("sha1", unique=True, name="sha1_unique")
db.fs.files.ensure_index("uuid", unique=True, name="uuid_unique")
db.analyses.ensure_index([("metadata.gps.pos", GEO2D)])