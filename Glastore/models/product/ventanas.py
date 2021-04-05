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
        for i in range(self.cantidad):
            self.draw_frame((x, 0))
            x += self.width
            if i % 2 == 0:
                self.draw_arrow(x)

    def draw_arrow(self, position):
        x1 = position - 5
        x2 = position
        y = self.height / 2
        xdata = (x1, x2)
        ydata = (y, y)
        draw_line(xdata, ydata)
        arrow_head = plt.Polygon(
            [[x1+3, y-3], [x1, y], [x1+3, y+3]],
            fill=False,
            closed=False,
            color="blue",
            lw=2
        )
        plt.gca().add_line(arrow_head)

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
        self.draw_arrow(self.height)

    def draw_frame(self, xy):
        draw_frame(
            xy,
            self.width,
            self.height
        )

    def draw_arrow(self, position):
        y1 = position
        y2 = position + 5
        x = self.height / 2
        ydata = (y1, y2)
        xdata = (x, x)
        draw_line(xdata, ydata)
        arrow_head = plt.Polygon(
            [[x-3, y2-3], [x, y2], [x+3, y2-3]],
            fill=False,
            closed=False,
            color="blue",
            lw=2
        )
        plt.gca().add_line(arrow_head)


#fija = Fija(75, 100)
#corrediza = Corrediza(50, 50, 2)
guillotina = Guillotina(50, 50, 2)

plt.axis('scaled')
plt.show()
