import matplotlib.pyplot as plt


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

    def __init__(self, width, height, orientacion, ax):
        self.orientacion = orientacion
        Ventana.__init__(self, width, height, ax)

    def draw(self):
        xposition = 0
        for i in range(2):
            self.draw_frame((xposition, 0))
            xposition += self.width
            if i % 2 != 0:
                self.draw_arrow(xposition)

    def draw_arrow(self, position):
        y = self.height / 2
        if self.orientacion == 1 or self.orientacion == 3:
            x1 = 0.8 * position
            x2 = position
            xmin = 1.15 * x1
            xmax = x1
        else:
            x1 = 0
            x2 = 0.35 * self.width
            xmin = 0.50 * x2
            xmax = x2

        points = [
            [xmin, 1.2 * y],
            [xmax, y],
            [xmin, 0.8 * y]
        ]
        xdata = (x1, x2)
        ydata = (y, y)
        draw_line(xdata, ydata, self.ax)
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
        self.set_triangle_points()
        points = [
            [self.xmin, self.ymin],
            [self.xmid, self.ymid],
            [self.xmax, self.ymax]
        ]
        triangle = plt.Polygon(
            points,
            fill=False,
            closed=False,
            color="blue",
            lw=2
        )
        self.ax.add_line(triangle)

    def set_triangle_points(self):
        if self.orientacion == 1 or self.orientacion == 2:
            self.xmin = 0
            self.xmid = self.width / 2
            self.xmax = self.width
            if self.orientacion == 1:
                self.ymin = 0
                self.ymid = self.height
                self.ymax = 0
            elif self.orientacion == 2:
                self.ymin = self.height
                self.ymid = 0
                self.ymax = self.height
        elif self.orientacion == 3 or self.orientacion == 4:
            self.ymin = self.height
            self.ymid = self.height / 2
            self.ymax = 0
            if self.orientacion == 3:
                self.xmin = 0
                self.xmid = self.width
                self.xmax = 0
            elif self.orientacion == 4:
                self.xmin = self.width
                self.xmid = 0
                self.xmax = self.width


if __name__ == "__main__":
    corrediza = Corrediza(10, 10, 2, plt.gca())
    plt.show()