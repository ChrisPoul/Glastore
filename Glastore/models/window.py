from sqlalchemy import (
    Column, Integer, String,
    Float, ForeignKey
)
from Glastore.models import db, add_to_db, commit_to_db
from Glastore.models.ventanas import (
    Corrediza, Fija, Guillotina, Abatible
)


class Window(db.Model):
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    description = Column(String(100), nullable=False, unique=False, default="fija")

    def add(self):
        add_to_db(self)

    def update(self):
        commit_to_db()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

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
            nums = "1234567890"
            for i, char in enumerate(self.description):
                if char in nums:
                    break
            dimensions = self.description[i:]
        else:
            dimensions = self.product.medidas

        return dimensions

    @property
    def width(self):
        try:
            width = self.dimensions.split(",")[0]
            width = float(width)
        except ValueError:
            width = 10

        return width

    @property
    def height(self):
        try:
            try:
                height = self.dimensions.split(",")[1]
            except IndexError:
                height = 10
            height = float(height)
        except ValueError:
            height = 10

        return height

    def has_dimensions(self):
        nums = "1234567890"
        has_dimensions = False
        for num in nums:
            if num in self.description:
                has_dimensions = True
                break

        return has_dimensions

    def update_description(self):
        window_descriptions = self.product.get_window_descriptions_from_name()
        for description in window_descriptions:
            if self.name in description:
                self.description = description
        self.update()

    def draw(self, ax):
        name = self.name
        orientacion = self.product.orientacion
        width = self.width
        height = self.height
        if "corrediza" in name:
            ventana = Corrediza(width, height, orientacion, ax)
        elif "abatible" in name:
            ventana = Abatible(width, height, orientacion, ax)
        elif "guillotina" in name:
            ventana = Guillotina(width, height, ax=ax)
        else:
            ventana = Fija(width, height, ax=ax)