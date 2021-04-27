#!/usr/bin/env python3

import os
if os.path.exists("app/db.sqlite"):
  os.remove("app/db.sqlite")

from app import db, create_app
db.create_all(app=create_app())