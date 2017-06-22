#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from db import Db # voyez db.py
import os
import psycopg2
import urlparse

app = Flask(__name__)
app.debug = True


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/reset')
def route_dbinit():
  """Cette route sert à initialiser (ou nettoyer) la base de données."""
  db = Db()
  db.executeFile("database_reset.sql")
  db.close()
  return "Done."

##########################################################################################################################################
if __name__ == "__main__":
    app.run()
