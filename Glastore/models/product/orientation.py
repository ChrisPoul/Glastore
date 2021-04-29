class WindowOrientation:

    def __init__(self, product):
        self.product = product
        self.windows = product.windows
        self.quote = product.quote
        self.selected_window = product.selected_window

    def select_next_window(self):
        self.unselect_prev_window()
        self.set_selected_window()
        self.select_window()
        self.update()

    def select_window(self):
        window = self.windows[self.selected_window]
        window.selected = True
        self.quote.focused_product_id = self.product.id
    
    def update(self):
        self.product.selected_window = self.selected_window
        self.product.update()

    def set_selected_window(self):
        for _ in self.windows:
            if self.is_last_window():
                self.selected_window = 0
            else:
                self.selected_window += 1
            if self.selected_window_is_rotatable():
                break

    def is_last_window(self):
        return self.selected_window == len(self.windows) - 1

    def selected_window_is_rotatable(self):
        non_rotatable_window_types = [
            "guillotina",
            "fijo",
            "fija",
            "antepecho"
        ]
        window = self.windows[self.selected_window]
        print(window.name)
        for win_type in non_rotatable_window_types:
            if win_type in window.name:
                return False
        
        return True

    def unselect_prev_window(self):
        prev_window = self.windows[self.selected_window]
        prev_window.selected = False

    def rotate_window(self):
        window = self.windows[self.selected_window]
        if window.orientacion >= 4:
            window.orientacion = 1
        else:
            window.orientacion += 1
        if "uerta" in window.name:
            if window.orientacion == 4:
                window.orientacion = 2
            else:
                window.orientacion += 1
        self.quote.focused_product_id = self.product.id
        self.update()