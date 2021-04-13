import base64
import matplotlib.pyplot as plt
from io import BytesIO
from sqlalchemy import (
    Column, Integer, String,
    Float, ForeignKey
)
from flask import request
from Glastore.models.window import Window, WindowPositioner, DescriptionExtractor
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
    cantidad = Column(Integer, nullable=False, default=0)
    total = Column(Float, nullable=False, default=0)
    selected_window = Column(Integer, nullable=True)
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
        self.update_attributes_on_submit()
        self.update_total()
        self.quote.error = self.update()
        if self.quote.error:
            self.name = previous_name

    def update_attributes_on_submit(self):
        attributes = [
            "name",
            "material",
            "acabado",
            "cristal",
            "unit_price",
            "medidas",
            "cantidad"
        ]
        for attribute in attributes:
            try:
                request_value = request.form[self.unique_keys[attribute]]
                setattr(self, attribute, request_value)
            except KeyError:
                pass

    def update_total(self):
        cantidad = float(self.cantidad)
        unit_price = float(self.unit_price)
        self.total = cantidad * unit_price

    @property
    def diseño(self):
        window_fig = plt.Figure(dpi=180, figsize=(4.5, 4.5))
        self.draw_final_window(window_fig)
        self.save_fig_to_temporary_buffer(window_fig)
        diseño = self.embed_in_html()

        return diseño

    def draw_final_window(self, window_fig):
        self.ax = window_fig.subplots()
        self.update_windows()
        for window, window_placement in zip(self.windows, self.window_positions):
            for xy in window_placement:
                window.draw(xy)

    def save_fig_to_temporary_buffer(self, fig):
        self.buffer = BytesIO()
        fig.savefig(self.buffer, format="png")

    def embed_in_html(self):
        # Embed the result in the html output.
        data_in_base64 = base64.b64encode(self.buffer.getbuffer())
        data = data_in_base64.decode("ascii")
        data_uri = 'data:image/png;base64,{}'.format(data)
        
        return data_uri

    @property
    def window_positions(self):
        window_positions = WindowPositioner(self.windows).get_window_positions()

        return window_positions

    def make_new_window(self, description):
        window = Window(
            product_id=self.id,
            description=description
        )
        window.add()

        return window

    def update_windows(self):
        self.update_existing_windows()
        self.add_new_windows()

    def update_existing_windows(self):
        for window in self.windows:
            self.update_existing_window(window)

    def update_existing_window(self, window):
        win_index = self.windows.index(window)
        try:
            description = self.window_descriptions[win_index]
        except IndexError:
            window.delete()
            return
        if window.description != description:
            window.update_description(description)

    def add_new_windows(self):
        for i, description in enumerate(self.window_descriptions):
            try:
                window = self.windows[i]
            except IndexError:
                window = self.make_new_window(description)

        if len(self.windows) == 0:
            self.make_new_window(description)

    @property
    def window_descriptions(self):
        window_descriptions = DescriptionExtractor(self.name).get_window_descriptions()

        return window_descriptions
