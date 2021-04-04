import matplotlib.pyplot as plt


def draw_frame(xy=(0, 0), width=10, height=10, lw=3):
    frame = plt.Rectangle(
        xy,
        width,
        height,
        fill=False,
        linewidth=lw
    )
    plt.gca().add_patch(frame)


def draw_line(xdata, ydata):
    line = plt.Line2D(xdata, ydata, lw=2, color="blue")
    plt.gca().add_line(line)


def draw_arrow(xdata, ydata):
    x1, x2 = xdata
    y1, y2 = ydata
    draw_line(xdata, ydata)
    arrow_head = plt.Polygon(
        [[x1+3, y1-3], [x1, y1], [x1+3, y1+3]],
        fill=False,
        closed=False,
        color="blue",
        lw=2
    )
    plt.gca().add_line(arrow_head)


class Fija:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.draw_window()

    def draw_window(self):
        draw_frame(
            width=self.width,
            height=self.height
        )


class Corrediza:

    def __init__(self, width, height, cantidad):
        self.width = width
        self.height = height
        self.cantidad = cantidad
        self.draw_windows()

    def draw_windows(self):
        x = 0
        for _ in range(self.cantidad):
            self.draw_frame((x, 0))
            x += self.width
        self.draw_arrow()

    def draw_arrow(self):
        xdata = (self.width-5, self.width)
        ydata = (self.height/2, self.height/2)
        draw_arrow(xdata, ydata)

    def draw_frame(self, xy):
        draw_frame(
            xy,
            self.width,
            self.height
        )


class Guillotina:

    def __init__(self, width, height, cantidad):
        self.width = width
        self.height = height
        self.cantidad = cantidad
        self.draw_windows()

    def draw_windows(self):
        y = 0
        for _ in range(self.cantidad):
            self.draw_frame((0, y))
            y += self.width

    def draw_frame(self, xy):
        draw_frame(
            xy,
            self.width,
            self.height
        )


#fija = Fija(75, 100)
corrediza = Corrediza(50, 50, 2)
#guillotina = Guillotina(50, 50, 2)

plt.axis('scaled')
plt.show()
