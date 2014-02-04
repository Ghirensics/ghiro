# Ghiro - Copyright (C) 2013-2014 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import datetime
from django import template
from dateutil import parser
from bson.objectid import InvalidId

from analyses.models import AnalysisMetadataDescription
from analyzer.db import get_file

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
def hexview(image_id, length=8):
    """Hexdump representation.
    @param image_id: gridfs image id
    @return: hexdump
    @see: code inspired to http://code.activestate.com/recipes/142812/
    """

    # Get image from gridfs.
    try:
       file = get_file(image_id)
    except (InvalidId, TypeError):
        return  None

    # Read data.
    src = file.read()

    hex_dump = []

    # Deal with unicode.
    if isinstance(src, unicode):
        digits = 4
    else:
        digits = 2

    # Create hex view.
    for i in xrange(0, len(src), length):
        line = {}
        s = src[i:i+length]
        hexa = b" ".join(["%0*X" % (digits, ord(x)) for x in s])
        text = b"".join([x if 0x20 <= ord(x) < 0x7F else b"." for x in s])
        line["address"] = b"%04X" % i
        line["hex"] = b"%-*s" % (length*(digits + 1), hexa)
        line["text"] = text
        hex_dump.append(line)
    return hex_dump