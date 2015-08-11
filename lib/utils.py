# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import tempfile
import magic
# Deal with Python 3.
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from PIL import Image
from pymongo.errors import InvalidId
from lib.db import save_file, get_file


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

def hexdump(image_id, length=8):
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

def import_is_available(module_name):
    """Checks if a module is available.
    @param module_name: module name
    @return: import status
    """
    try:
        __import__(module_name, globals(), locals(), ["dummy"], -1)
        return True
    except ImportError:
        return False

def deps_check():
    """Check for all dependencies."""
    # TODO: move the dict to a configuration file.
    deps = [{"name": "Django", "module": "django"},
            {"name": "GExiv2", "module": "gi.repository.GExiv2"},
            {"name": "Pillow", "module": "PIL"},
            {"name": "Pdfkit", "module": "pdfkit"},
            {"name": "Pymongo", "module": "pymongo"},
            {"name": "Chardet", "module": "chardet"},
            {"name": "Python Dateutil", "module": "dateutil"},
            {"name": "Python Magic", "module": "magic"},
            ]

    for dep in deps:
        dep["available"] = import_is_available(dep["module"])

    return deps

def get_content_type_from_file(file_path):
    """Returns content type of a file.
    @param file_path: file path
    @return: content type
    """
    mime = magic.Magic(mime=True)
    return mime.from_file(file_path)