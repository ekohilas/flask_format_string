#!/usr/local/bin/python3.5
from wsgiref.handlers import CGIHandler
from run import app
CGIHandler().run(app)
