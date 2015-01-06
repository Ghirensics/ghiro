# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import re
import base64
import datetime
from django import template
from dateutil import parser
from bson.objectid import InvalidId
from lib.db import get_file

from analyses.models import AnalysisMetadataDescription

register = template.Library()
 
@register.filter("mongo_id")
def mongo_id(value):
    """Mongo ID lookup.
    @param value: mongo dict
    """
    # Retrieve _id value
    if type(value) == type({}):
        if value.has_key("_id"):
            value = value["_id"]
   
    # Return value
    return unicode(value)

@register.filter
def classname(obj):
    """Returns class name for an object.
    @param obj: object
    @return: class name as string
    """
    classname = obj.__class__.__name__
    return classname

@register.filter
def has_severity(value, severity):
    """Checks if a signature has severity.
    @param value: signature set
    @param severity: severity to check
    @return: comparison state
    """
    for sign in value:
        if sign["severity"] == int(severity):
            return True
    return False

@register.filter
def count_severity(value, severity):
    """Counts signatures with severity.
    @param value: signature set
    @param severity: severity to check
    @return: count
    """
    counter = 0
    # Check if there are signatures or it's none.
    if value:
        # Counter.
        for sign in value:
            if sign["severity"] == int(severity):
                counter += 1
    return counter

@register.filter
def to_date(date):
    """Returns a datetime object from a string.
    @note: This is an hack to be able to format sqlite datetime because in sqlite they are handled as string.
    @param date: object or string
    @return: datetime obj
    """
    if isinstance(date, datetime.date):
        return date
    elif isinstance(date, str) or isinstance(date, unicode):
        return parser.parse(date)
    else:
        return date

@register.filter
def get_metadata_description(key):
    """Get description for a metadata key.
    @param key: fully qualified metadata key
    @return: metadata key description
    """
    try:
        data = AnalysisMetadataDescription.objects.get(key=key.lower())
    except AnalysisMetadataDescription.DoesNotExist:
        return "Description not available."
    else:
        return data.description

@register.filter
def to_base64(image_id):
    """Return a base64 representation for an image to be used in html img tag.
    @param image_id: mongo gridfs id
    @return: base64 blob
    """
    image_obj = get_file(image_id)
    image_encoded = base64.encodestring(image_obj.read())
    return "data:%s;base64,%s" % (image_obj.content_type, image_encoded)

@register.filter
def to_strings(image_id):
    """Extract all strings.
    @param image_id: mongo gridfs id
    @return: strings list
    """
    data = get_file(image_id).read()
    # This strings extraction code comes form Cuckoo Sandbox.
    strings = re.findall("[\x1f-\x7e]{6,}", data)
    strings += [str(ws.decode("utf-16le")) for ws in re.findall("(?:[\x1f-\x7e][\x00]){6,}", data)]
    return strings

@register.filter
def to_relevant_strings(image_id):
    """Extract all relevant strings.
    @param image_id: mongo gridfs id
    @return: strings list
    """
    data = "\n".join(to_strings(image_id))
    # URLs.
    strings = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", data)
    # FTPs
    strings += re.findall("ftp[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", data)
    # IPs.
    strings += re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", data)
    return strings