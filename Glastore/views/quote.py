import base64
import matplotlib.pyplot as plt
from io import BytesIO
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash
)
from Glastore.models import format_date, format_price, get_form
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
    customer_heads = {
        "name": "Cliente",
        "email": "Email",
        "phone": "Tel.",
        "address": "Dirección"
    }
    form = get_form(customer_heads)
    customer_names = []
    customer_emails = []
    customer_phones = []
    customer_addresses = []
    for customer in Customer.get_all():
        customer_names.append(customer.name)
        customer_emails.append(customer.email)
        customer_phones.append(customer.phone)
        customer_addresses.append(customer.address)
    if request.method == "POST":
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
                url_for('quote.edit', quote_id=quote.id)
            )
            for key in customer_heads:
                customer = Customer.search(request.form[key])
                if customer:
                    quote = Quote.new(customer.id)
                    return redirect(
                        url_for('quote.edit', quote_id=quote.id)
                    )
        flash(error)

    return render_template(
        'quote/add.html',
        form=form,
        customer_heads=customer_heads,
        customer_placeholders=customer_placeholders,
        customer_names=customer_names,
        customer_emails=customer_emails,
        customer_phones=customer_phones,
        customer_addresses=customer_addresses
    )


@bp.route("/edit/<int:quote_id>", methods=('GET', 'POST'))
def edit(quote_id):
    quote = Quote.get(quote_id)
    quote.done = False
    if request.method == "POST":
        error = quote.request.edit()
        if error:
            flash(error)

    return render_template(
        'quote/edit.html',
        quote=quote,
        customer_heads=customer_heads,
        product_heads=product_heads,
        product_keys=quote.request.product_keys,
        product_placeholders=product_placeholders,
        format_date=format_date,
        format_price=format_price
    )


@bp.route("/done/<int:quote_id>")
def done(quote_id):
    quote = Quote.get(quote_id)
    qutoe.request.done()
    quote.done = True

    return render_template(
        'quote/done.html',
        quote=quote,
        customer_heads=customer_heads,
        product_heads=product_heads,
        product_keys=quote.request.product_keys,
        product_placeholders=product_placeholders,
        format_date=format_date,
        format_price=format_price,
    )
