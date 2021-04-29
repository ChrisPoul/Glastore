from flask import (
    Blueprint, render_template, redirect,
    url_for, request
)
import matplotlib.pyplot as plt
from Glastore.models import get_temporary_uri
from Glastore.models.quote import SoldQuote

bp = Blueprint('home', __name__)


@bp.route('/')
def home():
    figure = plt.Figure(dpi=150, figsize=(4, 4))
    axis = figure.subplots()
    sold_quotes = SoldQuote.get_all()
    dates = [sold_quote.date for sold_quote in sold_quotes]
    totals = [sold_quote.total for sold_quote in sold_quotes]
    axis.plot(dates, totals)
    temporary_uri = get_temporary_uri(figure)

    return render_template(
        'home/home.html',
        my_plot=temporary_uri
    )


@bp.route('/sidebar')
def sidebar():
    search_term = request.args["sidebar-search-term"]

    return redirect(
        url_for('home.home')
    )
