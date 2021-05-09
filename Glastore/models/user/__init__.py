from sqlalchemy import (
    Column, Integer, DateTime,
    ForeignKey, String, Text
)
from Glastore.models import (
    db, add_to_db, commit_to_db
)


class User(db.Model):
    id = Column(Integer, primary_key=True)
    email = Column(String(150), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(Text, nullable=False)

    def __repr__(self):
        return self.__dict__

    def add(self):
        add_to_db(self)

    def update(self):
        commit_to_db()

    def delete(self):
        db.session.delete(self)
        commit_to_db()

    def get(id):
        return User.query.get(id)

    def search(search_term):
        user = User.query.filter_by(username=search_term).first()
        if not user:
            user = User.query.filter_by(email=search_term).first()

        return user

