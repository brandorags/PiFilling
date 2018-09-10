import logging

from flask import Flask


# init logging
logging.basicConfig(filename='../../pifilling.log', format='[%(levelname)s] %(asctime)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.WARNING)

# init Flask
app = Flask(__name__)
app.config.from_pyfile('../app_config.py')
