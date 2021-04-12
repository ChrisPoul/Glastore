import matplotlib.pyplot as plt


def draw_line(xdata, ydata, ax=plt):
    line = plt.Line2D(xdata, ydata, lw=2, color="blue")
    ax.add_line(line)


class Ventana:

    def __init__(self, xy, width, height, ax):
        self.xy = xy
        self.width = width
        self.height = height
        self.ax = ax
        self.ax.axis('off')
        self.draw()
        self.ax.axis('scaled')

    
    def draw_frame(self, xy=(0, 0), lw=6):
        frame = plt.Rectangle(
            xy,
            self.width,
            self.height,
            fill=False,
            linewidth=lw
        )
        self.ax.add_patch(frame)


class Fija(Ventana):

    def __init__(self, xy, width, height, ax):
        Ventana.__init__(self, xy, width, height, ax)

    def draw(self):
        self.draw_frame(
            xy=self.xy
        )


class Corrediza(Ventana):

    def __init__(self, xy, width, height, orientacion, ax):
        self.orientacion = orientacion
        Ventana.__init__(self, xy, width, height, ax)

    def draw(self):
        xposition, yposition = self.xy
        self.draw_frame(
            xy=(xposition, yposition)
        )
        self.draw_arrow(xposition)

    def draw_arrow(self, position):
        xposition, yposition = self.xy
        y = self.height/2 + yposition
        if self.orientacion == 1 or self.orientacion == 3:
            x1 = 0.7 * self.width + xposition
            x2 = self.width + xposition
            xmin = 1.15 * (0.7 * self.width) + position
            xmax = x1
        else:
            x1 = xposition
            x2 = 0.30 * self.width + x1
            xmin = 0.70 * (0.30 * self.width) + position
            xmax = x2

        points = [
            [xmin, 1.1 * y + (0.1 * self.width)],
            [xmax, y],
            [xmin, 0.9 * y - (0.1 * self.width)]
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

    def __init__(self, xy, width, height, ax):
        Ventana.__init__(self, xy, width, height, ax)

    def draw(self):
        xposition, yposition = self.xy
        for i in range(2):
            self.draw_frame((xposition, yposition))
            if i == 0:
                self.draw_arrow(yposition)
            yposition += self.height

    def draw_arrow(self, position):
        xposition, yposition = self.xy
        y1 = position + self.height
        y2 = 0.6 * self.height + yposition
        x = self.width / 2 + xposition
        ydata = (y1, y2)
        xdata = (x, x)
        draw_line(xdata, ydata, self.ax)
        xmin = 0.9 * x
        xmid = x
        xmax = 1.1 * x
        ymin = y2
        ymax = 1.1 * y2
        points = [
            [xmin, ymax],
            [xmid, ymin],
            [xmax, ymax]
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

    def __init__(self, xy, width, height, orientacion, ax):
        self.orientacion = orientacion
        Ventana.__init__(self, xy, width, height, ax)

    def draw(self):
        self.draw_frame(
            xy=self.xy
        )
        self.draw_triangle()
    
    def draw_triangle(self):
        points = self.get_triangle_points()
        triangle = plt.Polygon(
            points,
            fill=False,
            closed=False,
            color="blue",
            lw=2
        )
        self.ax.add_line(triangle)

    def get_triangle_points(self):
        xposition, yposition = self.xy
        if self.orientacion == 1 or self.orientacion == 2:
            xmin = xposition
            xmid = self.width / 2 + xposition
            xmax = self.width + xposition
            if self.orientacion == 1:
                ymin = yposition
                ymid = self.height + yposition
                ymax = yposition
            elif self.orientacion == 2:
                ymin = self.height + yposition
                ymid = yposition
                ymax = self.height + yposition
        elif self.orientacion == 3 or self.orientacion == 4:
            ymin = self.height + yposition
            ymid = self.height / 2 + yposition
            ymax = yposition
            if self.orientacion == 3:
                xmin = xposition
                xmid = self.width + xposition
                xmax = xposition
            elif self.orientacion == 4:
                xmin = self.width + xposition
                xmid = xposition
                xmax = self.width + xposition
        points = [
            [xmin, ymin],
            [xmid, ymid],
            [xmax, ymax]
        ]

        return points


if __name__ == "__main__":
    corrediza = Corrediza((20, 20), 10, 10, 2, plt.gca())
    plt.show()