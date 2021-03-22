from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash
)
from Glastore.models import Quote, Customer

bp = Blueprint("quote", __name__, url_prefix="/quote")


@bp.route('/add', methods=('GET', 'POST'))
def add():
    autocomplete_data = ["Pene", "Vagina"]
    if request.method == "POST":
        search_term = request.form["search_term"]
        customer = Customer.get(search_term)
        if customer:
            quote = Quote.new(customer.id)
            return redirect(
                url_for('quote.edit', quote_id=quote.id)
            )
        flash("No se encontro un cliente con ese termino de busqueda")

    return render_template(
        'quote/add.html',
        autocomplete_data=autocomplete_data
    )


@bp.route("/edit/<int:quote_id>", methods=('GET', 'POST'))
def edit(quote_id):
    quote = Quote.get(quote_id)
    if request.method == "POST":
        pass

    return render_template(
        'quote/edit.html',
        quote=quote
    )
