from flask import (
    Blueprint, redirect, url_for
)
from Glastore.models.product import Product, product_heads
from Glastore.models.window import Window

bp = Blueprint('product', __name__, url_prefix='/product')


@bp.route('/select_next_window/<int:product_id>')
def select_next_window(product_id):
    product = Product.get(product_id)
    prev_window = product.windows[product.selected_window]
    prev_window.selected = False
    prev_window.update()
    if product.selected_window != len(product.windows) - 1:
        product.selected_window += 1
    else:
        product.selected_window = 0
    product.update()
    window = product.windows[product.selected_window]
    window.selected = True
    window.update()

    return redirect(
        url_for('quote.edit', quote_id=product.quote_id)
    )


@bp.route('/rotate_window/<int:product_id>')
def rotate_window(product_id):
    product = Product.get(product_id)
    window = product.windows[product.selected_window]
    if window.orientacion >= 4:
        window.orientacion = 1
    else:
        window.orientacion += 1
    window.update()

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
