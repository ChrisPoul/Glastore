import matplotlib.pyplot as plt


class BasicWindow:

    def __init__(self, axis, xy, width, height):
        self.axis = axis
        self.xy = xy
        self.width = width
        self.height = height
        self.axis.axis('off')
        self.draw()
        self.axis.axis('scaled')

    def draw(self):
        self.draw_frame()
    
    def draw_frame(self, lw=8):
        frame = plt.Rectangle(
            self.xy,
            self.width,
            self.height,
            fill=False,
            linewidth=lw,
            color="#18100a"
        )
        self.axis.add_patch(frame)

    def draw_selected_frame(self, lw=5):
        frame = plt.Rectangle(
            self.xy,
            self.width * 0.99,
            self.height * 0.99,
            fill=False,
            linewidth=lw,
            color="blue"
        )
        self.axis.add_patch(frame)

    def draw_triangle(self):
        points = self.get_triangle_points()
        triangle = plt.Polygon(
            points,
            fill=False,
            closed=False,
            color="blue",
            lw=2
        )
        self.axis.add_line(triangle)

    def get_triangle_points(self):
        if self.orientacion % 2 == 0:
            self.set_horizontal_orientation()
        else:
            self.set_vertical_orientation()
        points = [
            [self.xmin, self.ymin],
            [self.xmid, self.ymid],
            [self.xmax, self.ymax]
        ]

        return points

    def set_vertical_orientation(self):
        xposition, yposition = self.xy
        self.xmin = xposition
        self.xmid = self.width / 2 + xposition
        self.xmax = self.width + xposition
        if self.orientacion == 1:
            self.set_facing_up()
        elif self.orientacion == 3:
            self.set_facing_down()

    def set_facing_up(self):
        xposition, yposition = self.xy
        self.ymin = yposition
        self.ymid = self.height + yposition
        self.ymax = yposition
    
    def set_facing_down(self):
        xposition, yposition = self.xy
        self.ymin = self.height + yposition
        self.ymid = yposition
        self.ymax = self.height + yposition

    def set_horizontal_orientation(self):
        xposition, yposition = self.xy
        self.ymin = self.height + yposition
        self.ymid = self.height / 2 + yposition
        self.ymax = yposition
        if self.orientacion == 2:
            self.set_facing_right()
        elif self.orientacion == 4:
            self.set_facing_left()

    def set_facing_right(self):
        xposition, yposition = self.xy
        self.xmin = xposition
        self.xmid = self.width + xposition
        self.xmax = xposition

    def set_facing_left(self):
        xposition, yposition = self.xy
        self.xmin = self.width + xposition
        self.xmid = xposition
        self.xmax = self.width + xposition


class Fija(BasicWindow):

    def __init__(self, axis, xy, width, height):
        BasicWindow.__init__(self, axis, xy, width, height)


class Corrediza(BasicWindow):

    def __init__(self, axis, xy, width, height, orientacion, selected=False):
        self.orientacion = orientacion
        self.selected = selected
        BasicWindow.__init__(self, axis, xy, width, height)

    def draw(self):
        BasicWindow.draw(self)
        xposition, _ = self.xy
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
        draw_line(xdata, ydata, self.axis)
        arrow_head = plt.Polygon(
            points,
            fill=False,
            closed=False,
            color="blue",
            lw=2
        )
        self.axis.add_line(arrow_head)


class Guillotina(BasicWindow):

    def __init__(self, axis, xy, width, height):
        BasicWindow.__init__(self, axis, xy, width, height)

    def draw(self):
        BasicWindow.draw(self)
        self.draw_arrow()

    def draw_arrow(self, position):
        xposition, yposition = self.xy
        y1 = position + self.height
        y2 = 0.6 * self.height + yposition
        x = self.width / 2 + xposition
        ydata = (y1, y2)
        xdata = (x, x)
        draw_line(xdata, ydata, self.axis)
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
        self.axis.add_line(arrow_head)


class Abatible(BasicWindow):

    def __init__(self, axis, xy, width, height, orientacion, selected=False):
        self.orientacion = orientacion
        self.selected = selected
        BasicWindow.__init__(self, axis, xy, width, height)

    def draw(self):
        BasicWindow.draw(self)
        self.draw_triangle()
    

class Oscilobatiente(BasicWindow):

    def __init__(self, axis, xy, width, height, orientacion, selected=False):
        self.orientacion = orientacion
        self.selected = selected
        BasicWindow.__init__(self, axis, xy, width, height)

    def draw(self):
        BasicWindow.draw(self)
        self.draw_triangles()

    def draw_triangles(self):
        self.draw_triangle()
        if self.orientacion == 4:
            self.orientacion = 1
        else:
            self.orientacion += 1
        self.draw_triangle()


def draw_line(xdata, ydata, axis=plt):
    line = plt.Line2D(xdata, ydata, lw=2, color="blue")
    axis.add_line(line)