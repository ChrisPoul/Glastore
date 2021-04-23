import base64
import matplotlib.pyplot as plt
from io import BytesIO
from sqlalchemy import (
    Column, Integer, String,
    Float, ForeignKey
)
from flask import request
from Glastore.models.window import Window
from .position import WindowPositioner
from .description import SubWindowDescription
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
    selected_window = Column(Integer, nullable=False, default=0)
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


class FinalWindowImage:

    def __init__(self, product):
        self.product = product
        self.update_sub_windows()
    
    @property
    def temporary_uri(self):
        figure = self.make_figure()
        temporary_buffer = self.save_to_temporary_buffer(figure)
        temporary_uri = self.get_temporary_uri(temporary_buffer)

        return temporary_uri

    def update_sub_windows(self):
        windows = SubWindows(self.product)
        windows.update()

    def make_figure(self):
        figure = plt.Figure(dpi=150, figsize=(4.5, 4.5))
        axis = figure.subplots()
        final_window = FinalWindow(self.product)
        final_window.draw(axis)

        return figure

    def save_to_temporary_buffer(self, figure):
        buffer = BytesIO()
        figure.savefig(buffer, format="png")

        return buffer

    def get_temporary_uri(self, buffer):
        data_in_base64 = base64.b64encode(buffer.getbuffer())
        data = data_in_base64.decode("ascii")
        data_uri = 'data:image/png;base64,{}'.format(data)
        
        return data_uri


class FinalWindow:

    def __init__(self, product):
        self.windows = product.windows
        self.quote = product.quote
    
    def draw(self, axis):
        for window, xy in zip(self.windows, self.window_positions):
            window.draw(axis, xy)
        self.draw_selected_window()

    def draw_selected_window(self):
        selected_window = None
        for window in self.windows:
            if window.selected is True:
                selected_window = window
        if selected_window:
            selected_window.draw_selected()

    @property
    def window_positions(self):
        window_positions = WindowPositioner(self.windows).get_window_positions()

        return window_positions


class SubWindows:

    def __init__(self, product):
        self.id = product.id
        self.windows = product.windows
        self.product_name = product.name

    def update(self):
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
            self.make_new_window(self.product_name)

    def make_new_window(self, description):
        window = Window(
            product_id=self.id,
            description=description
        )
        window.add()

        return window

    @property
    def window_descriptions(self):
        final_window_description = SubWindowDescription(self.product_name)
        sub_window_descriptions = final_window_description.get_sub_window_descriptions()

        return sub_window_descriptions
