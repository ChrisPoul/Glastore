from sqlalchemy import (
    Column, Integer, String,
    Float, ForeignKey
)
from Glastore.models.window import Window
from .final_window import FinalWindowImage
from .request import ProductRequest
from Glastore.models import (
    db, add_to_db, commit_to_db
)

product_heads = {
    "name": "Nombre",
    "material": "Material",
    "acabado": "Acabado",
    "cristal": "Cristal",
    "unit_price": "Precio de Venta"
}


class Product(db.Model):
    id = Column(Integer, primary_key=True)
    quote_id = Column(Integer, ForeignKey('quote.id'), nullable=False)
    name = Column(String(300), nullable=False, unique=False, default="")
    material = Column(String(100), nullable=False, unique=False, default="")
    cristal = Column(String(100), nullable=False, unique=False, default="")
    acabado = Column(String(100), nullable=False, unique=False, default="")
    unit_price = Column(Float, nullable=False, default=0)
    medidas = Column(String(50), nullable=False, unique=False, default="")
    cantidad = Column(Integer, nullable=False, default=0)
    total = Column(Float, nullable=False, default=0)
    selected_window = Column(Integer, nullable=False, default=0)
    windows = db.relationship(
        'Window', backref='product', lazy=True,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return self.__dict__

    def add(self):
        add_to_db(self)

    def update(self):
        commit_to_db()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get(search_term):
        product = Product.query.get(search_term)
        if not product:
            product = Product.query.filter_by(name=search_term).first()

        return product

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
        return ProductRequest(self)

    @property
    def diseño(self):
        window_image = FinalWindowImage(self)

        return window_image.temporary_uri

    def select_next_window(self):
        self.unselect_prev_window()
        self.set_selected_window()
        window = self.windows[self.selected_window]
        window.selected = True
        self.quote.focused_product_id = self.id
        self.update()

    def set_selected_window(self):
        for _ in self.windows:
            if self.selected_window != len(self.windows) - 1:
                self.selected_window += 1
            else:
                self.selected_window = 0
            if self.selected_window_is_rotatable():
                break

    def selected_window_is_rotatable(self):
        window = self.windows[self.selected_window]
        if "fija" in window.name or "fijo" in window.name:
            return False
        elif "antepecho" in window.name or "guillotina" in window.name:
            return False
        
        return True

    def unselect_prev_window(self):
        prev_window = self.windows[self.selected_window]
        prev_window.selected = False
        prev_window.update()

    def rotate_window(self):
        window = self.windows[self.selected_window]
        if window.orientacion >= 4:
            window.orientacion = 1
        else:
            window.orientacion += 1
        self.quote.focused_product_id = self.id
        self.update()
