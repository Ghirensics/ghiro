# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

class GhiroException(Exception):
    """Base Ghiro exception."""
    pass

class GhiroValidationException(GhiroException):
    """Validation error."""
    pass

class GhiroPluginException(GhiroException):
    """An error occurred when running the plugin."""
    pass