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


class Ventana:

    def __init__(self, width, height, ax):
        self.width = width
        self.height = height
        self.ax = ax


class Fija(Ventana):

    def __init__(self, width, height, ax):
        Ventana.__init__(self, width, height, ax)
        self.draw_window()

    def draw_window(self):
        draw_frame(
            width=self.width,
            height=self.height,
            ax=self.ax
        )


class Corrediza(Ventana):

    def __init__(self, width, height, cantidad, ax):
        Ventana.__init__(self, width, height, ax)
        self.cantidad = cantidad
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


class Guillotina(Ventana):

    def __init__(self, width, height, cantidad, ax):
        Ventana.__init__(self, width, height, ax)
        self.cantidad = cantidad
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
        y2 = 1.3 * position
        x = self.width / 2
        ydata = (y1, y2)
        xdata = (x, x)
        draw_line(xdata, ydata, self.ax)
        points = [
            [0.8 * x, 0.8 * y2],
            [x, y2],
            [1.2 * x, 0.8 * y2]
        ]
        arrow_head = plt.Polygon(
            points,
            fill=False,
            closed=False,
            color="blue",
            lw=2
        )
        self.ax.add_line(arrow_head)


class Abatible(Ventana):

    def __init__(self, width, height, ax):
        Ventana.__init__(self, width, height, ax)
        self.draw_window()

    def draw_window(self):
        draw_frame(
            width=self.width,
            height=self.height,
            ax=self.ax
        )
        self.draw_triangle()
    
    def draw_triangle(self):
        ymax = self.height
        ymin = 0
        points = [
            [0, ymin],
            [self.width/2, ymax],
            [self.width, ymin]
        ]
        triangle = plt.Polygon(
            points,
            fill=False,
            closed=False,
            color="blue",
            lw=2
        )
        self.ax.add_line(triangle)
