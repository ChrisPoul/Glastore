from sqlalchemy import (
    Column, Integer, DateTime,
    ForeignKey, String, Text
)
from Glastore.models import db, MyModel


class User(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    email = Column(String(150), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(Text, nullable=False)

    def get(id):
        return User.query.get(id)

    def search(search_term):
        user = User.query.filter_by(username=search_term).first()
        if not user:
            user = User.query.filter_by(email=search_term).first()

        return user

