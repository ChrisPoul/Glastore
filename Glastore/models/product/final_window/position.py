

class WindowPositioner:

    def __init__(self, windows):
        self.xposition, self.yposition = (0, 0)
        self.windows = windows

    def get_window_positions(self):
        self.window_positions = []
        self.handle_laterales()
        self.add_window_positions()

        return self.window_positions

    def handle_laterales(self):
        for window in self.windows:
            if "laterales" in window.description:
                self.xposition += window.width
                break

    def add_window_positions(self):
        for i, window in enumerate(self.windows):
            if i > 0:
                self.decide_window_position(window)
            self.add_current_window_position(window)

    def decide_window_position(self, window):
        if "superior" in window.description or "antepecho" in window.description:
            self.position_window_top(window)
        elif "inferior" in window.description:
            self.position_window_bottom(window)
        else:
            self.position_window_right(window)

    def position_window_top(self, window):
        self.yposition = self.windows[0].height
        self.xposition = 0

    def position_window_right(self, window):
        prev_window_index = self.windows.index(window) - 1
        self.yposition = 0
        self.xposition += self.windows[prev_window_index].width

    def position_window_bottom(self, window):
        self.yposition = -window.height
        self.xposition = 0

    def add_current_window_position(self, window):
        current_window_position = self.get_current_window_position(window)
        self.window_positions.append(current_window_position)

    def get_current_window_position(self, window):
        self.current_window_position = (0, 0)
        if "dos" in window.description:
            self.handle_window_twice(window)
        else:
            self.position_window_once()

        return self.current_window_position

    def position_window_once(self):
        self.current_window_position = (self.xposition, self.yposition)

    def handle_window_twice(self, window):
        if "laterales" in window.description:
            self.position_lateral(window)
        else:
            self.position_window_once()

    def position_lateral(self, window):
        self.current_window_position = (0, self.yposition)
        self.xposition -= window.width
