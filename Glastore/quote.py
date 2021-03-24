from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash
)
from Glastore.models import (
    Quote, Customer, Product, format_date,
    get_form
)

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
product_keys = {
    "name": ["Suministro y colocación de ", "nombre de pieza..."],
    "material": ["en ", "material..."],
    "cristal": ["con ", "cristal o vidrio..."],
    "medidas": [". Dimenciones", "medidas..."]
}


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
    form = get_form(product_keys)
    new_product = Product(
        name=form['name'],
        material=form['material'],
        cristal=form['cristal'],
        medidas=form['medidas']
    )
    if request.method == "POST":
        product = Product.get(request.form['name'])
        if product:
            quote.add_product(product)

    return render_template(
        'quote/edit.html',
        quote=quote,
        customer_heads=customer_heads,
        product_heads=product_heads,
        product_keys=product_keys,
        format_date=format_date,
        new_product=new_product
    )
