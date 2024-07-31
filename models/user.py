from sqlalchemy import *
from sqlalchemy.orm import backref
from extentions import db

class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    firstName = Column(String, nullable=False, index=True)
    lastName = Column(String, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, unique=True, nullable=False, index=True)
    code = Column(Integer, unique=True, nullable=False, index=True)
    grade = Column(String, index=True)
    field = Column(String, index=True)
    class_name = Column(String, index=True)
    class_id = Column(Integer, ForeignKey('classes.id') ,nullable=False, index=True)
    number = Column(String, index=True)
    phone = Column(String, index=True)
    father_phone = Column(String, index=True)
    mather_phone = Column(String, index=True)
    home_phone = Column(String, index=True)
    home_addres = Column(String, index=True)

    my_class = db.relationship("Class", backref=backref("users" , lazy="dynamic"))
