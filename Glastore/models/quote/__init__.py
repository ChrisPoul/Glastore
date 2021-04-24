from datetime import datetime
from sqlalchemy import (
    Column, Integer, DateTime,
    ForeignKey, String
)
from Glastore.models import (
    db, add_to_db, commit_to_db, get_form
)
from Glastore.models.product import Product
from Glastore.models.window import Window
from .request import QuoteRequest

product_keys = {
    "name": ["Suministro y colocación de ", "nombre de pieza..."],
    "material": ["en ", "material..."],
    "acabado": ["acabado ", "acabado..."],
    "cristal": ["con ", "cristal o vidrio..."],
    "medidas": ["Dimenciones", "medidas..."]
}


class Quote(db.Model):
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False, default=datetime.now)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    address = Column(String(100), nullable=True, unique=False)
    products = db.relationship(
        'Product', backref='quote', lazy=True,
        cascade='all, delete-orphan'
    )
    focused_product_id = Column(Integer, nullable=False, default=0)
    done = False
    form = None

    def __repr__(self):
        return self.__dict__

    def add(self):
        add_to_db(self)

    def update(self):
        commit_to_db()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def new(customer_id=1):
        quote = Quote(customer_id=customer_id)
        quote.add()

        return quote

    def get(id):
        return Quote.query.get(id)

    def get_all(customer_id=None):
        if not customer_id:
            quotes = Quote.query.all()
        else:
            quotes = Quote.query.filter_by(customer_id=customer_id).all()

        return quotes

    @property
    def folio(self):
        id = str(self.id)
        folio = "G"
        num_of_zeros = 5 - len(id)
        for _ in range(num_of_zeros):
            folio += "0"
        folio += id

        return folio

    @property
    def total(self):
        total = 0
        for product in self.products:
            total += product.total
        return total

    @property
    def request(self):
        return QuoteRequest(self)

    def add_product(self, product):
        new_product = Product(
            quote_id=self.id,
            name=product.name,
            material=product.material,
            acabado=product.acabado,
            cristal=product.cristal,
            unit_price=product.unit_price
        )
        new_product.add()

    @property
    def new_product(self):
        if not self.form:
            self.form = self.get_form()
        new_product = Product(
            quote_id=self.id,
            name=self.form['name'],
            material=self.form['material'],
            acabado=self.form['acabado'],
            cristal=self.form['cristal'],
            unit_price=0
        )
        return new_product

    def get_form(self):
        return get_form(product_keys)

    @property
    def autocomplete_data(self):
        return get_autocomplete_data()


def get_autocomplete_data():
    autocomplete = {
        "names": [],
        "materials": [],
        "acabados": [],
        "cristals": []
    }
    for product in Product.get_all():
        if product.name not in set(autocomplete["names"]):
            autocomplete["names"].append(product.name)
        if product.material not in set(autocomplete["materials"]):
            autocomplete["materials"].append(product.material)
        if product.cristal not in set(autocomplete["cristals"]):
            autocomplete["cristals"].append(product.cristal)
        if product.acabado not in set(autocomplete["acabados"]):
            autocomplete["acabados"].append(product.acabado)
    return autocomplete