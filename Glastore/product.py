from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash
)
from Glastore.models import Product, get_form

bp = Blueprint('product', __name__, url_prefix='/product')

product_heads = {
    "name": "Nombre",
    "material": "Material",
    "cristal": "Cristal",
    "medidas": "Medidas"
}


@bp.route('/products')
def products():
    products = Product.get_all()

    return render_template(
        'product/products.html',
        heads=product_heads,
        products=products
    )


@bp.route('/add', methods=('GET', 'POST'))
def add():
    form = get_form(product_heads)

    if request.method == "POST":
        form = get_form(product_heads)
        product = Product(
            name=form["name"],
            material=form["material"],
            cristal=form["cristal"],
            medidas=form["medidas"]
        )
        error = product.add()

        if not error:
            return redirect(
                url_for('product.products')
            )
        flash(error)

    return render_template(
        'product/add.html',
        heads=product_heads,
        form=form
    )


@bp.route('/update/<int:product_id>', methods=('POST', 'GET'))
def update(product_id):
    product = Product.get(product_id)

    if request.method == 'POST':
        form = get_form(product_heads)
        error = product.update(form)

        if not error:
            return redirect(
                url_for('product.products')
            )
        flash(error)

    return render_template(
        'product/update.html',
        heads=product_heads,
        product=product
    )


@bp.route('/delete/<int:product_id>', methods=('POST',))
def delete(product_id):
    product = Product.get(product_id)
    product.delete()

    return redirect(
        url_for('product.products')
    )
