# Ghiro - Copyright (C) 2013-2014 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import StringIO
import tempfile
import logging
import logging.handlers

from PIL import Image

from analyses.models import AnalysisMetadataDescription
from lib.db import save_file

try:
    import chardet
    IS_CHARDET = True
except ImportError:
    IS_CHARDET = False


class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

    def _convert_to_dict(self, d):
        if isinstance(d, AutoVivification):
            return dict((k, self._convert_to_dict(v)) for k, v in d.items())
        return d

    def to_dict(self):
        return self._convert_to_dict(self)

def to_unicode(str):
    """Attempt to fix non uft-8 string into utf-8. It tries to guess input encoding,
    if fail retry with a replace strategy (so undetectable chars will be escaped).
    @see: fuller list of encodings at http://docs.python.org/library/codecs.html#standard-encodings
    """

    def brute_enc(str):
        """Trying to decode via simple brute forcing."""
        result = None
        encodings = ("ascii", "utf8", "latin1")
        for enc in encodings:
            if result:
                break
            try:
                result = unicode(str, enc)
            except UnicodeDecodeError:
                pass
        return result

    def chardet_enc(str):
        """Guess encoding via chardet."""
        result = None
        enc = chardet.detect(str)["encoding"]

        try:
            result = unicode(str, enc)
        except UnicodeDecodeError:
            pass

        return result

    # If already in unicode, skip.
    if isinstance(str, unicode):
        return str

    # First try to decode against a little set of common encodings.
    result = brute_enc(str)

    # Try via chardet.
    if not result and IS_CHARDET:
        result = chardet_enc(str)

    # If not possible to convert the input string, try again with
    # a replace strategy.
    if not result:
        result = unicode(str, errors="replace")

    return result

def str2file(text_data):
    strIO = StringIO.StringIO()
    strIO.write(text_data)
    strIO.seek(0)
    return strIO

def str2temp_file(text_data):
    tmp = tempfile.NamedTemporaryFile(prefix="ghiro-")
    tmp.write(text_data)
    return tmp

def add_metadata_description(key, description):
    """Adds key metadata description to lookup table.
    @param key: fully qualified metadata key
    @param description: key description
    """
    # Skip if no description is provided.
    if description:
        try:
            AnalysisMetadataDescription.objects.get(key=key.lower())
        except AnalysisMetadataDescription.DoesNotExist:
            obj = AnalysisMetadataDescription(key=key.lower(), description=description)
            obj.save()

def str2image(data):
    """Converts binary data to PIL Image object.
    @param data: binarydata
    @return: PIL Image object
    """
    output = StringIO.StringIO()
    output.write(data)
    output.seek(0)
    return Image.open(output)

def image2str(img):
    """Converts PIL Image object to binary data.
    @param img: PIL Image object
    @return:  binary data
    """
    f = StringIO.StringIO()
    img.save(f, "JPEG")
    return f.getvalue()

def init_logging():
    """Initializes logging."""
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)

    # Create console handler.
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # Create formatter and add it to the handlers.
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    # Add the handlers to the logger.
    logger.addHandler(ch)


def create_thumb(file_path):
    """Create thumbnail
    @param file_path: file path
    @return: GridFS ID
    """
    try:
        thumb = Image.open(file_path)
        thumb.thumbnail([200, 150], Image.ANTIALIAS)
        return save_file(data=image2str(thumb), content_type="image/jpeg")
    except:
        return None