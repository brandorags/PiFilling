import os
from datetime import timedelta


# These settings' values may be changed to accommodate where the code will be housed
# (development vs. production server)

# statement for enabling the development environment
DEBUG = True

# specify port
PORT = 5000

# application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# path of log file
LOG_FILE_LOC = os.path.join(BASE_DIR, 'info.log')

# file upload folder
UPLOADED_FILES_DEST = BASE_DIR + '/files'

# database location
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'pifilling.db')

# according to SQLAlchemy, this setting adds significant overhead,
# so don't use it
SQLALCHEMY_TRACK_MODIFICATIONS = False

# cookie settings
SESSION_DURATION = timedelta(minutes=15)
SECRET_KEY = 'thisisaveryverysecretkey'
