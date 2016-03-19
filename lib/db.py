# Ghiro - Copyright (C) 2013-2016 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import sys
import hashlib
import uuid
from django.conf import settings
import gridfs
from bson import ObjectId
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConnectionFailure


def mongo_connect():
    """Connects to Mongo, exits if unable to connect.
    @return: connection handler
    """
    try:
        # connect = False will open a connection to db only when really needed.
        db = Database(MongoClient(settings.MONGO_URI, connect=False), settings.MONGO_DB)
    except ConnectionFailure:
        print("ERROR: unable to connect to MongoDB. Please check the server availability.")
        sys.exit()
    else:
        return db

# Mongo connection.
db = mongo_connect()
fs = gridfs.GridFS(db)

def save_file(data=None, file_path=None, content_type=None):
    """Save file in GridFS.
    @param data: file data
    @param file_path: file path
    @param content_type: file content type
    @return: saved file ID
    """
    if file_path:
        try:
            fh = open(file_path, "rb")
            data = fh.read()
        finally:
            fh.close()

    # Using SHA1 as file key.
    sha1 = hashlib.sha1(data).hexdigest()

    # File identifier.
    id = uuid.uuid4().hex + sha1

    # Save file and returns UUID.
    try:
        fs.put(data, content_type=content_type, sha1=sha1, uuid=id)
    except gridfs.errors.FileExists:
        id = db.fs.files.find_one({"sha1": sha1})["uuid"]
    finally:
        return id

def get_file(id):
    """Get a file from GridFS.
    @param id: file uuid
    @return: file object"""
    obj_id = db.fs.files.find_one({"uuid": id})["_id"]
    return fs.get(ObjectId(obj_id))

def get_file_length(id):
    """Get a file length from GridFS.
    @param id: file uuid
    @return: integer"""

    return db.fs.files.find_one({"uuid": id})["length"]

def save_results(results):
    """Save results in mongo.
    @param results: data dict
    @return: object id
    """
    return db.analyses.save(results)