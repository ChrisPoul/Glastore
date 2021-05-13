import matplotlib.pyplot as plt
from .position import WindowPositioner
from .description import SubWindowDescriptionGetter
from Glastore.models.window import Window
from Glastore.models import get_temporary_uri


class FinalWindowImage:

    def __init__(self, product):
        self.product = product
        self.update_sub_windows()
    
    @property
    def temporary_uri(self):
        figure = self.make_figure()
        temporary_uri = get_temporary_uri(figure)

        return temporary_uri

    def update_sub_windows(self):
        sub_windows = SubWindows(self.product)
        sub_windows.update()

    def make_figure(self):
        figure = plt.Figure(dpi=150, figsize=(4.5, 4.5))
        axis = figure.subplots()
        final_window = FinalWindow(self.product)
        final_window.draw(axis)

        return figure


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
        if selected_window and self.quote.done is False:
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
        final_window_description = SubWindowDescriptionGetter(self.product_name)
        sub_window_descriptions = final_window_description.get_window_descriptions()

        return sub_window_descriptions
