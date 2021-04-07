from sqlalchemy import (
    Column, Integer, String,
    Float, ForeignKey
)
from Glastore.models import db


class Window(db.Model):
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
