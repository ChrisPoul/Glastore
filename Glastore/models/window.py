from sqlalchemy import (
    Column, Integer, String,
    Float, ForeignKey
)
from Glastore.models import db, add_to_db, commit_to_db
from Glastore.models.basic_windows import (
    Corrediza, Fija, Guillotina, Abatible
)


class Window(db.Model):
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    description = Column(String(100), nullable=False, unique=False, default="fija")
    orientacion = Column(Integer, nullable=False, default=1)

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
        if self.has_dimensions():
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
        if self.has_dimensions():
            dimensions = self.get_dimensions()
        else:
            dimensions = self.product.medidas

        width, height = self.get_width_and_height(dimensions)

        return (width, height)

    def get_dimensions(self):
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
        separators = ["x", ",", "*"]
        width = 10
        height = 10
        for separator in separators:
            if separator in dimensions:
                try:
                    width = dimensions.split(separator)[0]
                    width = float(width)
                except ValueError:
                    width = 10
                try:
                    try:
                        height = dimensions.split(separator)[1]
                    except IndexError:
                        height = 10
                    height = float(height)
                except ValueError:
                    height = 10

        return (width, height)

    @property
    def width(self):
        return self.dimensions[0]

    @property
    def height(self):
        return self.dimensions[1]

    def has_dimensions(self):
        nums = "1234567890"
        has_dimensions = False
        for num in nums:
            if num in self.description:
                has_dimensions = True
                break

        return has_dimensions

    def update_description(self, description):
        self.description = description
        self.update()

    def draw(self, xy):
        ax = self.product.ax
        name = self.name
        orientacion = self.orientacion
        width = self.width
        height = self.height
        if "corrediza" in name:
            ventana = Corrediza(xy, width, height, orientacion, ax)
        elif "abatible" in name:
            ventana = Abatible(xy, width, height, orientacion, ax)
        elif "guillotina" in name:
            ventana = Guillotina(xy, width, height, ax)
        else:
            ventana = Fija(xy, width, height, ax)