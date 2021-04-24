import base64
import matplotlib.pyplot as plt
from io import BytesIO
from .position import WindowPositioner
from .description import SubWindowDescription
from . import Window


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
        positioner = WindowPositioner(self.windows)
        window_positions = positioner.get_window_positions()

        return window_positions


class SubWindows:

    def __init__(self, product):
        self.product = product
        self.windows = product.windows
        self.product_name = product.name

    def update(self):
        self.update_existing_windows()
        self.add_new_windows()

    def update_existing_windows(self):
        for window in self.windows:
            self.update_window(window)

    def update_window(self, window):
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
                self.windows[i]
            except IndexError:
                self.make_new_window(description)

        if len(self.product.windows) == 0:
            self.make_new_window(self.product_name)

    def make_new_window(self, description):
        window = Window(
            product_id=self.product.id,
            description=description
        )
        window.add()

    @property
    def window_descriptions(self):
        final_window_description = SubWindowDescription(self.product_name)
        sub_window_descriptions = final_window_description.get_sub_window_descriptions()

        return sub_window_descriptions
