import matplotlib.pyplot as plt


def draw_frame(xy=(0, 0), width, height, lw=3):
    frame = plt.Rectangle(
        xy,
        width,
        height,
        fill=False,
        linewidth=lw
    )
    plt.gca().add_patch(frame)
