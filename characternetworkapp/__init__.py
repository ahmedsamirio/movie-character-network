from flask import Flask

app = Flask(__name__)

from characternetworkapp import routes
