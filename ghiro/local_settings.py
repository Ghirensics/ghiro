LOCAL_SETTINGS = True
from settings import *

DATABASES = {
    'default': {
        # Engine type. Ends with 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.sqlite3',
        # Database name or path to database file if using sqlite3.
        'NAME': 'db.sqlite',
        # Credntials. The following settings are not used with sqlite3.
        'USER': '',
        'PASSWORD': '',
        # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'HOST': '',
        # Set to empty string for default port.
        'PORT': '',
        # Set timeout (avoids SQLite "database is locked" errors).
        'timeout': 300,
    }
}

# MySQL tuning.
#DATABASE_OPTIONS = {
# "init_command": "SET storage_engine=INNODB",
#}

# Mongo database settings
MONGO_URI = "mongodb://localhost/"
MONGO_DB = "ghirodb"

# Max uploaded image size (in bytes).
# Default is 150MB.
MAX_FILE_UPLOAD = 157286400

# Allowed file types.
ALLOWED_EXT = ['image/bmp', 'image/x-canon-cr2', 'image/jpeg', 'image/png',
               'image/x-canon-crw', 'image/x-eps', 'image/x-nikon-nef',
               'application/postscript', 'image/gif', 'image/x-minolta-mrw',
               'image/x-olympus-orf', 'image/x-photoshop', 'image/x-fuji-raf',
               'image/x-panasonic-raw2', 'image/x-tga', 'image/tiff', 'image/pjpeg',
               'image/x-x3f', 'image/x-portable-pixmap']

# Override default secret key stored in secret_key.py
# Make this unique, and don't share it with anybody.
# SECRET_KEY = "YOUR_RANDOM_KEY"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

ADMINS = (
    # ("Your Name", "your_email@example.com"),
)

MANAGERS = ADMINS

# Allow verbose debug error message in case of application fault.
# It's strongly suggested to set it to False if you are serving the
# web application from a web server front-end (i.e. Apache).
DEBUG = True

# A list of strings representing the host/domain names that this Django site
# can serve.
# Values in this list can be fully qualified names (e.g. 'www.example.com').
# When DEBUG is True or when running tests, host validation is disabled; any
# host will be accepted. Thus it's usually only necessary to set it in production.
ALLOWED_HOSTS = ["*"]

# Automatically checks once a day for updates.
# Set it to False to disable update check.
UPDATE_CHECK = True

# Auto upload is used to upload ana analyze files from a directory, monitoring
# it for changes.
# It is usually used to upload images via a shared folder or FTP.
# It should be an absolute path.
# Example: "/home/ghiro_share"
AUTO_UPLOAD_DIR = None
# Delete a file after upload and submission.
# The default behaviour is True.
# WARNING: It is not suggested to set it to False, because you will re-submit images
# each startup.
AUTO_UPLOAD_DEL_ORIGINAL = True
# Clean up AUTO_UPLOAD_DIR when startup.
# The default behaviour is True.
# WARNING: It is not suggested to set it to False, because you will re-submit images
# each startup.
AUTO_UPLOAD_STARTUP_CLEANUP = True

# Auditing.
# Logs all user actions.
AUDITING_ENABLED = True

# Log directory. Here is where Ghiro puts all logs.
LOG_DIR = os.path.join(PROJECT_DIR, "log")
# File name used for image processor log.
LOG_PROCESSING_NAME = "processing.log"
# Processor log maximum size.
LOG_PROCESSING_SIZE = 1024*1024*16 # 16 megabytes
# How many copies of processor log keep while rotating logs.
LOG_PROCESSING_NUM = 3 # keep 3 copies
# File name used for audit log.
LOG_AUDIT_NAME = "audit.log"
# Audit log maximum size.
LOG_AUDIT_SIZE = 1024*1024*16 # 16 megabytes
# How many copies of audit log keep while rotating logs.
LOG_AUDIT_NUM = 3 # keep 3 copies