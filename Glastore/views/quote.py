import base64
import matplotlib.pyplot as plt
from io import BytesIO
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash
)
from Glastore.models import format_date, format_price
from Glastore.models.quote import Quote
from Glastore.models.product import Product
from Glastore.models.customer import Customer
from Glastore.views.auth import login_required

bp = Blueprint("quote", __name__, url_prefix="/quote")
customer_heads = {
    "name": "Cliente",
    "email": "Email",
    "address": "Dirección"
}
product_heads = {
    "cantidad": "Cant.",
    "description": "Descripción",
    "diseño": "Diseño",
    "unit_price": "P.Unidad",
    "total": "Total"
}


@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    autocomplete = [customer.name for customer in Customer.get_all()]
    if request.method == "POST":
        customer = Customer.get(request.form["search_term"])
        if customer:
            quote = Quote.new(customer.id)
            return redirect(
                url_for('quote.edit', quote_id=quote.id)
            )
        flash("No se encontro un cliente con ese termino de busqueda")

    return render_template(
        'quote/add.html',
        autocomplete=autocomplete
    )


@bp.route("/edit/<int:quote_id>", methods=('GET', 'POST'))
@login_required
def edit(quote_id):
    quote = Quote.get(quote_id)
    if request.method == "POST":
        error = quote.request.handle()
        if error:
            flash(error)

    return render_template(
        'quote/edit.html',
        quote=quote,
        customer_heads=customer_heads,
        product_heads=product_heads,
        product_keys=quote.request.product_keys,
        format_date=format_date,
        format_price=format_price
    )


@bp.route("/done/<int:quote_id>")
def done(quote_id):
    quote = Quote.get(quote_id)
    quote.done = True

    return render_template(
        'quote/done.html',
        quote=quote,
        customer_heads=customer_heads,
        product_heads=product_heads,
        product_keys=quote.request.product_keys,
        format_date=format_date,
        format_price=format_price,
    )
