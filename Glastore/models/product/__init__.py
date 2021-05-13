from sqlalchemy import (
    Column, Integer, String,
    Float, ForeignKey
)
from Glastore.models.window import Window
from .final_window import FinalWindowImage
from .orientation import WindowOrientation
from Glastore.models import db, MyModel

product_heads = {
    "name": "Nombre",
    "material": "Material",
    "acabado": "Acabado",
    "cristal": "Cristal",
    "unit_price": "Precio de Venta"
}


class Product(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    quote_id = Column(Integer, ForeignKey('quote.id'), nullable=False)
    name = Column(String(300), nullable=False, unique=False, default="")
    material = Column(String(100), nullable=False, unique=False, default="")
    cristal = Column(String(100), nullable=False, unique=False, default="")
    acabado = Column(String(100), nullable=False, unique=False, default="")
    unit_price = Column(Integer, nullable=False, default=0)
    medidas = Column(String(50), nullable=False, unique=False, default="")
    cantidad = Column(Integer, nullable=False, default=0)
    total = Column(Float, nullable=False, default=0)
    selected_window = Column(Integer, nullable=False, default=0)
    windows = db.relationship(
        'Window', backref='product', lazy=True,
        cascade='all, delete-orphan'
    )

    def get(id):
        return Product.query.get(id)

    def search(search_term):
        return Product.query.filter_by(name=search_term).first()

    def get_all(search_term=None):
        if not search_term:
            products = Product.query.all()
        else:
            products = Product.query.filter_by(material=search_term).all()
            if not products:
                products = Product.query.filter_by(cristal=search_term).all()

        return products

    @property
    def unique_keys(self):
        unique_value_keys = dict(
            name=f"name{self.id}",
            material=f"material{self.id}",
            acabado=f"acabado{self.id}",
            cristal=f"cristal{self.id}",
            medidas=f"medidas{self.id}",
            cantidad=f"cantidad{self.id}",
            unit_price=f"unit_price{self.id}"
        )

        return unique_value_keys

    @property
    def request(self):
        from .request import ProductRequest
        return ProductRequest(self)

    @property
    def diseño(self):
        window_image = FinalWindowImage(self)

        return window_image.temporary_uri

    @property
    def orientation(self):
        return WindowOrientation(self)
