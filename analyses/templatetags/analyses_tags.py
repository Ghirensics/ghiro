# Ghiro - Copyright (C) 2013 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import datetime
from django import template
from dateutil import parser

from analyses.models import AnalysisMetadataDescription

register = template.Library()
 
@register.filter("mongo_id")
def mongo_id(value):
    """Mongo ID lookup.
    @param value: mongo dict
    """
    # Retrieve _id value
    if type(value) == type({}):
        if value.has_key('_id'):
            value = value['_id']
   
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
        data =AnalysisMetadataDescription.objects.get(key=key.lower())
    except AnalysisMetadataDescription.DoesNotExist:
        return "Description not available."
    else:
        return data.description