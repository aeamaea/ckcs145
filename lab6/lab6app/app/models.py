from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from dataclasses import dataclass 

"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""

@dataclass
class User(Model):
    __tablename__ = 'User'

    email: str
    name: str

    email = Column( String() , primary_key=True)
    name = Column(String())
    
