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
        self.ax.axis('off')
        self.draw()
        self.ax.axis('scaled')

    
    def draw_frame(self, xy=(0, 0), lw=3):
        frame = plt.Rectangle(
            xy,
            self.width,
            self.height,
            fill=False,
            linewidth=lw
        )
        self.ax.add_patch(frame)


class Fija(Ventana):

    def __init__(self, width, height, ax):
        Ventana.__init__(self, width, height, ax)

    def draw(self):
        self.draw_frame()


class Corrediza(Ventana):

    def __init__(self, width, height, cantidad, ax):
        self.cantidad = cantidad
        Ventana.__init__(self, width, height, ax)

    def draw(self):
        x = 0
        for i in range(self.cantidad):
            self.draw_frame((x, 0))
            x += self.width
            if i % 2 != 0:
                self.draw_arrow(x)

    def draw_arrow(self, position):
        x1 = 0.8 * position
        x2 = position
        y = self.height / 2
        xdata = (x1, x2)
        ydata = (y, y)
        draw_line(xdata, ydata, self.ax)
        points = [
            [1.15 * x1, 0.8 * y],
            [x1, y],
            [1.15 * x1, 1.2 * y]
        ]
        arrow_head = plt.Polygon(
            points,
            fill=False,
            closed=False,
            color="blue",
            lw=2
        )
        self.ax.add_line(arrow_head)


class Guillotina(Ventana):

    def __init__(self, width, height, ax):
        Ventana.__init__(self, width, height, ax)

    def draw(self):
        y = 0
        for i in range(2):
            self.draw_frame((0, y))
            if i == 0:
                self.draw_arrow(y)
            y += self.height

    def draw_arrow(self, position):
        y1 = position
        y2 = 0.3 * self.height
        x = self.width / 2
        ydata = (y1, y2)
        xdata = (x, x)
        draw_line(xdata, ydata, self.ax)
        points = [
            [0.8 * x, 0.5 * y2],
            [x, y2],
            [1.2 * x, 0.5 * y2]
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

    def __init__(self, width, height, orientacion, ax):
        self.orientacion = orientacion
        Ventana.__init__(self, width, height, ax)

    def draw(self):
        self.draw_frame()
        self.draw_triangle()
    
    def draw_triangle(self):
        if self.orientacion == 1:
            points = [
                [0, 0],
                [self.width/2, self.height],
                [self.width, 0]
            ]
        elif self.orientacion == 2:
            points = [
                [0, self.height],
                [self.width/2, 0],
                [self.width, self.height]
            ]
        elif self.orientacion == 3:
            points = [
                [0, self.height],
                [self.width, self.height/2],
                [0, 0]
            ]
        elif self.orientacion == 4:
            points = [
                [self.width, self.height],
                [0, self.height/2],
                [self.width, 0]
            ]

        triangle = plt.Polygon(
            points,
            fill=False,
            closed=False,
            color="blue",
            lw=2
        )
        self.ax.add_line(triangle)
