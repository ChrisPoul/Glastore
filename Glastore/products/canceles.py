import matplotlib.pyplot as plt


class Cancel:

    def __init__(self, width, height):
        self.current_axis = plt.gca()
        self.width = width
        self.height = height
        self.draw_frame()

    def draw_frame(self):
        frame = plt.Rectangle(
            (0, 0),
            self.width,
            self.height,
            fill=False,
            linewidth=3
        )
        self.current_axis.add_patch(frame)


cancel = Cancel(75, 100)

plt.axis('scaled')
plt.show()
