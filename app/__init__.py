from flask import Flask

app = Flask(__name__)

from app import routes  # or views, depending on the file name

