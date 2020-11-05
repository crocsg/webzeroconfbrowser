from flask import Flask
from flask_bootstrap import Bootstrap
import logging

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'spacelab'
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
logging.basicConfig(level=logging.DEBUG)

from zerobrowse import routes
