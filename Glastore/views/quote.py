import base64
import matplotlib.pyplot as plt
from io import BytesIO
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash
)
from Glastore.models import format_date, format_price
from Glastore.views import get_form
from Glastore.models.quote import Quote
from Glastore.models.product import Product
from Glastore.models.customer import Customer, customer_heads
from Glastore.views.auth import login_required

bp = Blueprint("quote", __name__, url_prefix="/quote")

quote_customer_heads = {
    "name": "Cliente",
    "email": "Email",
    "address": "Dirección"
}
customer_placeholders = {
    "name": "Nombre del cliente...",
    "email": "Corréo electrónico...",
    "phone": "Teléfono del cliente...",
    "address": "Dirección de facturación..."
}
product_heads = {
    "cantidad": "Cant.",
    "description": "Descripción",
    "diseño": "Diseño",
    "unit_price": "P.Unidad",
    "total": "Total"
}
product_placeholders = {
    "name": "nombre de la pieza...",
    "material": "material...",
    "acabado": "acabado...",
    "cristal": "cristal o vidrio...",
    "medidas": "medidas..."
}


@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    form = get_form(customer_heads)
    if request.method == "POST":
        error = None
        customer = search_for_customer(form)
        if not customer:
            customer = Customer(
                name=form['name'],
                email=form['email'],
                phone=form['phone'],
                address=form['address']
            )
            error = customer.request.add()
        if not error:
            quote = Quote.new(customer.id)
            return redirect(
                url_for('quote.edit', id=quote.id)
            )
        flash(error)

    return render_template(
        'quote/add.html',
        form=form,
        customer_heads=customer_heads,
        customer_placeholders=customer_placeholders,
    )


def search_for_customer(form):
    for key in customer_heads:
        customer = Customer.search(form[key])
        if customer:
            return customer

    return None


@bp.route("/edit/<int:id>", methods=('GET', 'POST'))
def edit(id):
    quote = Quote.get(id)
    quote.done = False
    if request.method == "POST":
        error = quote.request.edit()
        if error:
            flash(error)

    return render_template(
        'quote/edit.html',
        quote=quote,
        customer_heads=quote_customer_heads,
        product_heads=product_heads,
        product_keys=quote.request.product_keys,
        product_placeholders=product_placeholders,
        format_date=format_date,
        format_price=format_price
    )


@bp.route("/done/<int:id>")
def done(id):
    quote = Quote.get(id)
    quote.request.done()
    quote.done = True

    return render_template(
        'quote/done.html',
        quote=quote,
        customer_heads=quote_customer_heads,
        product_heads=product_heads,
        product_keys=quote.request.product_keys,
        product_placeholders=product_placeholders,
        format_date=format_date,
        format_price=format_price,
    )
