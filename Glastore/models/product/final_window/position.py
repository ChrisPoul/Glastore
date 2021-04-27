

class WindowPositioner:

    def __init__(self, windows):
        self.xposition, self.yposition = (0, 0)
        self.windows = windows

    def get_window_positions(self):
        self.handle_laterales()
        self.window_positions = []
        self.add_window_positions()

        return self.window_positions

    def handle_laterales(self):
        for window in self.windows:
            if "laterales" in window.description:
                self.xposition += window.width
                break

    def add_window_positions(self):
        for i, window in enumerate(self.windows):
            self.current_window = window
            if i > 0:
                self.decide_window_position()
            self.add_current_window_position()

    def decide_window_position(self):
        if self.is_top_window():
            self.position_window_top()
        elif self.is_bottom_window():
            self.position_window_bottom()
        else:
            self.position_window_right()

    def is_top_window(self):
        if "superior" in self.current_window.description:
            return True
        elif "antepecho" in self.current_window.description:
            return True
        
        return False

    def position_window_top(self):
        self.yposition = self.windows[0].height
        self.xposition = 0
        self.current_window.position = "top"
        self.current_window.update()

    def position_window_right(self):
        prev_window_index = self.windows.index(self.current_window) - 1
        prev_window = self.windows[prev_window_index]
        self.yposition = 0
        self.xposition += prev_window.width

    def is_bottom_window(self):
        return "inferior" in self.current_window.description

    def position_window_bottom(self):
        self.yposition = -(self.current_window.height)
        self.xposition = 0
        self.current_window.position = "bottom"
        self.current_window.update()

    def add_current_window_position(self):
        current_window_position = self.get_current_window_position()
        self.window_positions.append(current_window_position)

    def get_current_window_position(self):
        self.current_window_position = (0, 0)
        if "dos" in self.current_window.description:
            self.handle_window_twice()
        else:
            self.position_window_once()

        return self.current_window_position

    def position_window_once(self):
        self.current_window_position = (self.xposition, self.yposition)

    def handle_window_twice(self):
        if "laterales" in self.current_window.description:
            self.position_lateral()
        else:
            self.position_window_once()

    def position_lateral(self):
        self.current_window_position = (0, self.yposition)
        self.xposition -= self.current_window.width
