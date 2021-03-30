from sqlalchemy import (
    Column, Integer, ForeignKey, Float,
    String
)
from flask import request
from Glastore.models import (
    db, add_to_db, commit_to_db
)


class SoldProduct(db.Model):
    id = Column(Integer, primary_key=True)
    quote_id = Column(Integer, ForeignKey('quote.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    medidas = Column(String(50), nullable=False, unique=False, default="")
    cantidad = Column(Integer, nullable=False, default=0)
    total = Column(Float, nullable=False, default=0)

    def __repr__(self):
        return self.__dict__

    def add(self):
        self.cantidad = 0
        error = add_to_db(self)
        return error

    def update(self):
        error = commit_to_db()
        return error

    def get(id):
        return SoldProduct.query.get(id)

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

    def update_on_submit(self):
        self.update_medidas_on_submit()
        self.update_cantidad_on_submit()
        self.update_product_on_submit()
        self.update_total()

    def update_medidas_on_submit(self):
        try:
            self.medidas = request.form[self.unique_keys["medidas"]]
        except KeyError:
            pass

    def update_cantidad_on_submit(self):
        try:
            self.cantidad = request.form[self.unique_keys["cantidad"]]
        except KeyError:
            pass

    def update_total(self):
        cantidad = float(self.cantidad)
        unit_price = float(self.product.unit_price)
        self.total = cantidad * unit_price

    def update_product_on_submit(self):
        previous_name = self.product.name
        self.update_name_on_submit()
        self.update_material_on_submit()
        self.update_acabado_on_submit()
        self.update_cristal_on_submit()
        self.update_unit_price_on_submit()
        self.quote.error = self.product.update()
        if self.quote.error:
            self.product.name = previous_name

    def update_name_on_submit(self):
        try:
            self.product.name = request.form[self.unique_keys["name"]]
        except KeyError:
            pass

    def update_material_on_submit(self):
        try:
            self.product.material = request.form[self.unique_keys["material"]]
        except KeyError:
            pass

    def update_acabado_on_submit(self):
        try:
            self.product.acabado = request.form[self.unique_keys["acabado"]]
        except KeyError:
            pass

    def update_cristal_on_submit(self):
        try:
            self.product.cristal = request.form[self.unique_keys["cristal"]]
        except KeyError:
            pass

    def update_unit_price_on_submit(self):
        try:
            self.product.unit_price = request.form[self.unique_keys["unit_price"]]
        except KeyError:
            pass
