"""Data models."""
from main.__init__ import db

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, Boolean
from sqlalchemy.orm import relationship, backref
from config import Config

class Example(db.Model):
    __tablename__ = 'examples'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=False, nullable=True)
    email = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return '<Example {}>'.format(self.name)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()