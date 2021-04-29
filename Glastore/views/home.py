from flask import (
    Blueprint, render_template
)
import matplotlib.pyplot as plt
from Glastore.models import get_temporary_uri

bp = Blueprint('home', __name__)


@bp.route('/')
def home():
    figure = plt.Figure(dpi=150, figsize=(4, 4))
    axis = figure.subplots()
    axis.plot([1, 2, 3], [1, 2, 3])
    temporary_uri = get_temporary_uri(figure)

    return render_template(
        'home/home.html',
        my_plot=temporary_uri
    )
