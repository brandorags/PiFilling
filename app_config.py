# Copyright 2018 Brandon Ragsdale
#
# This file is part of PiFilling.
#
# PiFilling is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PiFilling is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PiFilling.  If not, see <https://www.gnu.org/licenses/>.


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

# URL where files are made publicly available
UPLOADED_FILES_URL = 'http://localhost:5000/'

# database location
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'pifilling.db')

# according to SQLAlchemy, this setting adds significant overhead,
# so don't use it
SQLALCHEMY_TRACK_MODIFICATIONS = False

# cookie settings
SESSION_DURATION = timedelta(minutes=15)
SECRET_KEY = 'thisisaveryverysecretkey'
