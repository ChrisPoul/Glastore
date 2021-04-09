import base64
import matplotlib.pyplot as plt
from io import BytesIO
from sqlalchemy import (
    Column, Integer, String,
    Float, ForeignKey
)
from flask import request
from Glastore.models.window import Window, window_types
from Glastore.models import (
    db, add_to_db, commit_to_db, get_form
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
    orientacion = Column(Integer, nullable=False, default=1)
    cantidad = Column(Integer, nullable=False, default=0)
    total = Column(Float, nullable=False, default=0)
    windows = db.relationship(
        'Window', backref='product', lazy=True,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return self.__dict__

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

    def add(self):
        error = self.validate_product()
        if not error:
            error = add_to_db(self)
        return error

    def update(self):
        error = self.validate_product()
        if not error:
            error = commit_to_db()

        return error

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def new(name):
        product = Product(
            quote_id=1,
            name=name,
            material=name,
            acabado=name,
            cristal=name,
            unit_price=0
        )
        error = product.add()
        if error:
            return product, error

        return product

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

    def validate_product(self):
        error = self.validate_fields()
        if not error:
            error = self.validate_price()

        return error

    def validate_fields(self):
        error_msg = "No se pueden dejar campos en blanco"
        error = None
        if self.name == "" or self.material == "" or self.cristal == "" or self.acabado == "":
            error = error_msg

        return error

    def validate_price(self):
        error = None
        if self.unit_price:
            try:
                float(self.unit_price)
            except ValueError:
                error = "Numero invalido"
                self.unit_price = 0
        else:
            self.unit_price = 0

        return error

    def update_on_submit(self):
        previous_name = self.name
        self.update_name_on_submit()
        self.update_material_on_submit()
        self.update_acabado_on_submit()
        self.update_cristal_on_submit()
        self.update_unit_price_on_submit()
        self.update_medidas_on_submit()
        self.update_cantidad_on_submit()
        self.update_total()
        self.quote.error = self.update()
        if self.quote.error:
            self.name = previous_name

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
        unit_price = float(self.unit_price)
        self.total = cantidad * unit_price

    def update_name_on_submit(self):
        try:
            self.name = request.form[self.unique_keys["name"]]
        except KeyError:
            pass

    def update_material_on_submit(self):
        try:
            self.material = request.form[self.unique_keys["material"]]
        except KeyError:
            pass

    def update_acabado_on_submit(self):
        try:
            self.acabado = request.form[self.unique_keys["acabado"]]
        except KeyError:
            pass

    def update_cristal_on_submit(self):
        try:
            self.cristal = request.form[self.unique_keys["cristal"]]
        except KeyError:
            pass

    def update_unit_price_on_submit(self):
        try:
            self.unit_price = request.form[self.unique_keys["unit_price"]]
        except KeyError:
            pass

    @property
    def diseño(self):
        fig = plt.Figure(dpi=150)
        self.ax = fig.subplots()
        self.draw_window()
        # Save figure to a temporary buffer.
        buffer = BytesIO()
        fig.savefig(buffer, format="png")
        # Embed the result in the html output.
        data = base64.b64encode(buffer.getbuffer()).decode("ascii")
        diseño = 'data:image/png;base64,{}'.format(data)

        return diseño

    def draw_window(self):
        self.update_windows()
        xy = (0, 0)
        xposition = 0
        for i, window in enumerate(self.windows):
            if i > 0:
                xposition += self.windows[i-1].width
                xy = (xposition, 0)
            window.draw(xy)

    def make_new_window(self, description):
        window = Window(
            product_id=self.id,
            description=description
        )
        window.add()

        return window

    def update_windows(self):
        for i, description in enumerate(self.window_descriptions):
            try:
                window = self.windows[i]
            except IndexError:
                window = self.make_new_window(description)
            if window.name not in self.name:
                window.delete()
            else:
                window.update_description(description)
        if len(self.windows) == 0:
            self.make_new_window(description)

    @property
    def window_descriptions(self):
        window_descriptions = []
        win_indexes = self.window_indexes
        for i, win_index in enumerate(win_indexes):
            if i == len(win_indexes) - 1:
                description = self.name[win_index:]
            else:
                next_win_index = win_indexes[i+1]
                description = self.name[win_index:next_win_index]
            window_descriptions.append(description)

        return window_descriptions

    @property
    def window_indexes(self):
        window_indexes = []
        for win_type in window_types:
            win_type_count = self.name.count(win_type)
            start = 0
            for _ in range(win_type_count):
                window_index = self.name.find(win_type, start)
                if window_index != -1:
                    window_indexes.append(window_index)
                    start = window_index + 1
            start = 0
        if len(window_indexes) == 0:
            window_indexes.append(0)

        return sorted(window_indexes)
