

class WindowPositioner:

    def __init__(self, windows):
        self.xposition, self.yposition = (0, 0)
        self.windows = windows

    def get_window_positions(self):
        self.window_xy_positions = []
        self.handle_laterales()
        for i, window in enumerate(self.windows):
            if i > 0:
                self.decide_window_position(window)
            self.add_window_ocurrances(window)

        return self.window_xy_positions

    def handle_laterales(self):
        for window in self.windows:
            if "laterales" in window.description:
                self.xposition += window.width

    def add_window_ocurrances(self, window):
        window_ocurrances = self.get_window_ocurrances(window)
        self.window_xy_positions.append(window_ocurrances)

    def decide_window_position(self, window):
        if "superior" in window.description:
            self.position_window_top()
        elif "antepecho" in window.description:
            self.position_antepecho()
        elif "inferior" in window.description:
            self.position_window_bottom(window)
        else:
            self.position_window_right(window)

    def position_window_top(self):
        self.yposition = self.windows[0].height
        if "dos" in self.windows[0].description:
            self.xposition = 0

    def position_window_right(self, window):
        prev_window_index = self.windows.index(window) - 1
        self.yposition = 0
        self.xposition += self.windows[prev_window_index].width

    def position_antepecho(self):
        self.yposition = self.windows[0].height
        self.xposition = 0

    def position_window_bottom(self, window):
        self.yposition = -window.height

    def get_window_ocurrances(self, window):
        self.window_ocurrances = []
        if "dos" in window.description:
            self.handle_window_twice(window)
        elif "tres" in window.description:
            self.position_three_times(window)
        else:
            self.position_window_once()

        return self.window_ocurrances

    def handle_window_twice(self, window):
        if "laterales" in window.description:
            self.position_laterales()
        else:
            self.position_window_twice(window)

    def position_window_once(self):
        xy = (self.xposition, self.yposition)
        self.window_ocurrances.append(xy)

    def position_window_twice(self, window):
        for i in range(1, 2+1):
            xy = (self.xposition, self.yposition)
            self.window_ocurrances.append(xy)
            if i % 2 != 0:
                self.xposition += window.width

    def position_three_times(self, window):
        for i in range(1, 3+1):
            xy = (self.xposition, self.yposition)
            self.window_ocurrances.append(xy)
            if i % 3 != 0:
                self.xposition += window.width

    def position_laterales(self):
        xy = (self.xposition, self.yposition)
        self.window_ocurrances.append(xy)
        xy = (0, self.yposition)
        self.window_ocurrances.append(xy)
