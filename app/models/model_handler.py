"""
Module that initializes one database from SQLAlchemy so that all tables
are being stored to that single database. 
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()