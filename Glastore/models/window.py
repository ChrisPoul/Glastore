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


class WindowPositioner:

    def __init__(self, windows):
        self.xposition, self.yposition = (0, 0)
        self.windows = windows

    def get_window_positions(self):
        window_xy_positions = []
        self.handle_laterales()
        for i, window in enumerate(self.windows):
            if i > 0:
                self.deside_window_position(window)
            window_repetitions = self.get_window_repetitions(window)
            window_xy_positions.append(window_repetitions)

        return window_xy_positions

    def handle_laterales(self):
        for window in self.windows:
            if "laterales" in window.description:
                self.xposition += window.width

    def deside_window_position(self, window):
        if "superior" in window.description:
            self.position_window_top()
        elif "antepecho" in window.description:
            self.position_antepecho()
        elif "inferior" in window.description:
            self.position_window_bottom(window)
        else:
            self.position_window_right(window)

    def position_window_right(self, window):
        prev_window_index = self.windows.index(window) - 1
        self.yposition = 0
        self.xposition += self.windows[prev_window_index].width

    def position_window_top(self):
        self.yposition = self.windows[0].height
        if "dos" in self.windows[0].description:
            self.xposition = 0

    def position_antepecho(self):
        self.yposition = self.windows[0].height
        self.xposition = 0

    def position_window_bottom(self):
        self.yposition = -window.height

    def get_window_repetitions(self, window):
        self.window_repetitions = []
        if "dos" in window.description:
            self.handle_window_twice(window)
        elif "tres" in window.description:
            for i in range(1, 3+1):
                xy = (self.xposition, self.yposition)
                self.window_repetitions.append(xy)
                if i % 3 != 0:
                    self.xposition += window.width
        else:
            self.position_window_once()

        return self.window_repetitions

    def handle_window_twice(self, window):
        if "laterales" in window.description:
            self.position_laterales()
        else:
            self.position_window_twice(window)

    def position_window_once(self):
        xy = (self.xposition, self.yposition)
        self.window_repetitions.append(xy)

    def position_window_twice(self, window):
        for i in range(1, 2+1):
            xy = (self.xposition, self.yposition)
            self.window_repetitions.append(xy)
            if i % 2 != 0:
                self.xposition += window.width

    def position_laterales(self):
        xy = (self.xposition, self.yposition)
        self.window_repetitions.append(xy)
        xy = (0, self.yposition)
        self.window_repetitions.append(xy)


class DescriptionExtractor:

    def __init__(self, description):
        self.full_description = description

    def get_window_descriptions(self):
        self.window_descriptions = {}
        for description_start in self.start_of_descriptions:
            self.current_description_start = description_start
            self.save_description()
        window_descriptions = self.get_window_descriptions_list()

        return window_descriptions

    def get_window_descriptions_list(self):
        return [self.window_descriptions[i] for i in self.window_descriptions]

    def save_description(self):
        self.current_description_index = self.start_of_descriptions.index(self.current_description_start)
        window_description = self.get_window_description()
        prev_description = self.get_previous_description()
        if not self.is_relative_window(prev_description):
            self.window_descriptions[self.current_description_index] = window_description

    def get_window_description(self):
        self.make_basic_description()
        self.handle_window_repetitions()

        return self.window_description

    def make_basic_description(self):
        if self.current_description_index == len(self.start_of_descriptions) - 1:
            self.window_description = self.full_description[self.current_description_start:]
        else:
            next_description_start = self.start_of_descriptions[self.current_description_index+1]
            self.window_description = self.full_description[self.current_description_start:next_description_start]
    
    def handle_window_repetitions(self):
        if self.is_relative_window(self.window_description):
            self.extend_window_description()

    def extend_window_description(self):
        try:
            next_description_start = self.start_of_descriptions[self.current_description_index+2]
            self.window_description = self.full_description[self.current_description_start:next_description_start]
        except IndexError:
            self.window_description = self.full_description[self.current_description_start:]

    def is_relative_window(self, description):
        relative_descriptors = [
            "dos",
            "antepecho",
            "tres"
        ]
        for descriptor in relative_descriptors:
            if descriptor in description:
                return True
        return False

    def get_previous_description(self):
        try:
            prev_description_index = self.current_description_index - 1
            prev_description = self.window_descriptions[prev_description_index]
        except KeyError:
            prev_description = ""

        return prev_description

    @property
    def start_of_descriptions(self):
        window_identifiers = [
            "dos",
            "tres",
            "antepecho",
            "fija",
            "fijo",
            "corrediza",
            "abatible",
            "guillotina"
        ]
        self.description_start_indexes = []
        for win_identifier in window_identifiers:
            self.get_start_of_description(win_identifier)
        if len(self.description_start_indexes) == 0:
            self.description_start_indexes.append(0)

        return sorted(self.description_start_indexes)

    def get_start_of_description(self, win_identifier):
        win_type_count = self.full_description.count(win_identifier)
        start = 0
        for _ in range(win_type_count):
            description_start_index = self.full_description.find(win_identifier, start)
            start = self.add_description_start(description_start_index)
    
    def add_description_start(self, description_start_index):
        start = 0
        if description_start_index != -1:
            self.description_start_indexes.append(description_start_index)
            start = description_start_index + 1
        
        return start
