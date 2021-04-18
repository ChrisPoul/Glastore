from flask import (
    Blueprint, redirect, url_for
)
from Glastore.models.product import Product, product_heads
from Glastore.models.window import Window

bp = Blueprint('product', __name__, url_prefix='/product')


@bp.route('/select_next_window/<int:product_id>')
def select_next_window(product_id):
    product = Product.get(product_id)
    product.select_next_window()

    return redirect(
        url_for('quote.edit', quote_id=product.quote_id)
    )


@bp.route('/rotate_window/<int:product_id>')
def rotate_window(product_id):
    product = Product.get(product_id)
    product.rotate_window()

    return redirect(
        url_for('quote.edit', quote_id=product.quote_id)
    )


@bp.route('/delete/<int:product_id>')
def delete(product_id):
    product = Product.get(product_id)
    quote_id = product.quote.id
    product.delete()

    return redirect(
        url_for('quote.edit', quote_id=quote_id)
    )
