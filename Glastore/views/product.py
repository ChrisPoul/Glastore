from flask import (
    Blueprint, redirect, url_for
)
from Glastore.models.product import Product, product_heads

bp = Blueprint('product', __name__, url_prefix='/product')


@bp.route("/rotate_window/<int:product_id>")
def rotate_window(product_id):
    product = Product.get(product_id)
    if product.orientacion >= 4:
        product.orientacion = 1
    else:
        product.orientacion += 1
    product.update()
    
    return redirect(
        url_for('quote.edit', quote_id=product.quote_id)
    )


@bp.route('/delete/<int:product_id>', methods=('POST',))
def delete(product_id):
    product = Product.get(product_id)
    product.delete()

    return redirect(
        url_for('product.products')
    )
