# Ghiro - Copyright (C) 2013-2014 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.
import chardet


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
    if not result:
        result = chardet_enc(str)

    # If not possible to convert the input string, try again with
    # a replace strategy.
    if not result:
        result = unicode(str, errors="replace")

    return result