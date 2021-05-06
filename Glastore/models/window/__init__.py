from sqlalchemy import (
    Column, Integer, String,
    Float, ForeignKey, Boolean
)
from Glastore.models import db, add_to_db, commit_to_db
from .basic_windows import (
    Corrediza, Fija, Guillotina, Abatible,
    Oscilobatiente
)


class Window(db.Model):
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    description = Column(
        String(100), nullable=False, unique=False, default="fija"
    )
    orientacion = Column(Integer, nullable=False, default=1)
    selected = Column(Boolean, nullable=False, default=False)

    def add(self):
        add_to_db(self)

    def update(self):
        commit_to_db()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get(window_id):
        return Window.query.get(window_id)

    @property
    def name(self):
        if has_dimensions(self.description):
            nums = "1234567890"
            for i, char in enumerate(self.description):
                if char in nums:
                    break
            name = self.description[:i]
        else:
            name = self.description

        return name

    @property
    def dimensions(self):
        if has_dimensions(self.description):
            dimensions_str = self.extract_dimensions_string()
        else:
            dimensions_str = self.product.medidas
        width, height = self.get_width_and_height(dimensions_str)

        if has_dimensions(self.product.name) is False:
            width = width / len(self.product.windows)

        return (width, height)

    def extract_dimensions_string(self):
        nums = "1234567890"
        num_indexes = []
        for i, char in enumerate(self.description):
            if char in nums:
                num_indexes.append(i)
        first_num_index = num_indexes[0]
        last_num_index = num_indexes[-1] + 1
        dimensions = self.description[first_num_index:last_num_index]

        return dimensions

    def get_width_and_height(self, dimensions):
        separators = ["x", "X", ",", "*"]
        width = 10
        height = 10
        for separator in separators:
            if separator in dimensions:
                width = self.get_width(dimensions, separator)
                height = self.get_height(dimensions, separator)

        return (width, height)

    def get_width(self, dimensions, separator):
        try:
            width = dimensions.split(separator)[0]
            width = float(width)
        except ValueError:
            width = 10

        return width

    @property
    def width(self):
        return self.dimensions[0]

    def get_height(self, dimensions, separator):
        try:
            try:
                height = dimensions.split(separator)[1]
            except IndexError:
                height = 10
            height = float(height)
        except ValueError:
            height = 10

        return height

    @property
    def height(self):
        return self.dimensions[1]

    def update_description(self, description):
        self.description = description
        self.update()

    def draw(self, axis, xy):
        if self.is_corrediza():
            ventana = Corrediza(
                axis=axis,
                xy=xy,
                width=self.width,
                height=self.height,
                orientacion=self.orientacion,
                selected=self.selected
            )
        elif self.is_abatible():
            ventana = Abatible(
                axis=axis,
                xy=xy,
                width=self.width,
                height=self.height,
                orientacion=self.orientacion,
                selected=self.selected
            )
        elif self.is_guillotina():
            ventana = Guillotina(
                axis=axis,
                xy=xy,
                width=self.width,
                height=self.height
            )
        elif self.is_oscilobatiente():
            ventana = Oscilobatiente(
                axis=axis,
                xy=xy,
                width=self.width,
                height=self.height,
                orientacion=self.orientacion,
                selected=self.selected
            )
        else:
            ventana = Fija(
                axis=axis,
                xy=xy,
                width=self.width,
                height=self.height
            )
        self.ventana = ventana

    def is_door(self):
        return "uerta" in self.name.lower()

    def is_corrediza(self):
        return "corrediz" in self.name

    def is_abatible(self):
        return "abatible" in self.name

    def is_guillotina(self):
        return "guillotina" in self.name

    def is_oscilobatiente(self):
        return "oscilobatiente" in self.name

    def draw_selected(self):
        self.ventana.draw_selected_frame()


def has_dimensions(description):
    nums = "1234567890"
    for num in nums:
        if num in description:
            return True

    return False