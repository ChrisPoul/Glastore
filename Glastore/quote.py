from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash
)
from Glastore.models import (
    Quote, Customer, Product, format_date,
    get_form, commit_to_db, obj_as_dict
)

bp = Blueprint("quote", __name__, url_prefix="/quote")
customer_heads = {
    "name": "Cliente",
    "email": "Email",
    "address": "Dirección"
}
products_heads = {
    "cant": "Cant.",
    "description": "Descripción",
    "diseño": "Diseño",
    "retail_price": "P.Unidad",
    "total": "Total"
}
product_heads = [
    "name",
    "material",
    "cristal",
    "medidas"
]


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
    new_product = Product(name="")
    if request.method == "POST":
        form = get_form(product_heads)
        product = Product.get(form['name'])
        if product:
            quote.add_product(product)

    return render_template(
        'quote/edit.html',
        quote=quote,
        customer_heads=customer_heads,
        products_heads=products_heads,
        format_date=format_date,
        new_product=new_product
    )
