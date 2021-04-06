import matplotlib.pyplot as plt


def draw_frame(xy=(0, 0), width=10, height=10, lw=3, ax=plt):
    frame = plt.Rectangle(
        xy,
        width,
        height,
        fill=False,
        linewidth=lw
    )
    ax.add_patch(frame)


def draw_line(xdata, ydata, ax=plt):
    line = plt.Line2D(xdata, ydata, lw=2, color="blue")
    ax.add_line(line)


class Fija:

    def __init__(self, width, height, ax=plt):
        self.width = width
        self.height = height
        self.ax = ax
        self.draw_window()

    def draw_window(self):
        draw_frame(
            width=self.width,
            height=self.height,
            ax=self.ax
        )


class Corrediza:

    def __init__(self, width, height, cantidad, ax=plt):
        self.width = width
        self.height = height
        self.cantidad = cantidad
        self.ax = ax
        self.draw_windows()

    def draw_windows(self):
        x = 0
        for i in range(self.cantidad):
            self.draw_frame((x, 0))
            x += self.width
            if i % 2 == 0:
                self.draw_arrow(x)

    def draw_arrow(self, position):
        x1 = 0.7 * position
        x2 = position
        y = self.height / 2
        xdata = (x1, x2)
        ydata = (y, y)
        draw_line(xdata, ydata, self.ax)
        points = [
            [1.2 * x1, 0.8 * y],
            [x1, y],
            [1.2 * x1, 1.2 * y]
        ]
        arrow_head = plt.Polygon(
            points,
            fill=False,
            closed=False,
            color="blue",
            lw=2
        )
        self.ax.add_line(arrow_head)

    def draw_frame(self, xy):
        draw_frame(
            xy,
            self.width,
            self.height,
            ax=self.ax
        )


class Guillotina:

    def __init__(self, width, height, cantidad, ax=plt):
        self.width = width
        self.height = height
        self.cantidad = cantidad
        self.ax = ax
        self.draw_windows()

    def draw_windows(self):
        y = 0
        for _ in range(self.cantidad):
            self.draw_frame((0, y))
            y += self.height
        self.draw_arrow(self.height)

    def draw_frame(self, xy):
        draw_frame(
            xy,
            self.width,
            self.height,
            ax=self.ax
        )

    def draw_arrow(self, position):
        y1 = position
        y2 = position + 5
        x = self.height / 2
        ydata = (y1, y2)
        xdata = (x, x)
        draw_line(xdata, ydata, self.ax)
        arrow_head = plt.Polygon(
            [[x-3, y2-3], [x, y2], [x+3, y2-3]],
            fill=False,
            closed=False,
            color="blue",
            lw=2
        )
        self.ax.add_line(arrow_head)

