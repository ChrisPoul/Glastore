import base64
import matplotlib.pyplot as plt
from io import BytesIO
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash
)
from Glastore.models import format_date, format_price
from Glastore.models.quote import Quote, product_keys
from Glastore.models.customer import Customer
from Glastore.models.product.ventanas import Corrediza, Guillotina

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
def edit(quote_id):
    quote = Quote.get(quote_id)
    if request.method == "POST":
        quote.handle_submit()
        if quote.error:
            flash(quote.error)

    return render_template(
        'quote/edit.html',
        quote=quote,
        customer_heads=customer_heads,
        product_heads=product_heads,
        product_keys=product_keys,
        format_date=format_date,
        format_price=format_price
    )


@bp.route("/done/<int:quote_id>")
def done(quote_id):
    quote = Quote.get(quote_id)

    return render_template(
        'quote/done.html',
        quote=quote,
        customer_heads=customer_heads,
        product_heads=product_heads,
        product_keys=product_keys,
        format_date=format_date,
        format_price=format_price,
        done=True
    )


@bp.route("/ventana", methods=('GET', 'POST'))
def ventana():
    fig = plt.Figure(dpi=150)
    ax = fig.subplots()
    corrediza = Guillotina(30, 50, 2, ax=ax)
    corrediza.ax.axis('scaled')

    # Save figure to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    diseño = 'data:image/png;base64,{}'.format(data)

    return render_template(
        'quote/diseño.html',
        diseño=diseño
    )
