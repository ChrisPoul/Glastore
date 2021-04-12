from flask import (
    Blueprint, redirect, url_for
)
from Glastore.models.product import Product, product_heads
from Glastore.models.window import Window

bp = Blueprint('product', __name__, url_prefix='/product')


@bp.route('/select_next_window/<int:product_id>')
def select_next_window(product_id):
    product = Product.get(product_id)

    return redirect(
        url_for('quote.edit', quote_id=product.quote_id)
    )


def rotate_window(window_id):
    window = Window.get(window_id)
    if window.orientacion >= 4:
        window.orientacion = 1
    else:
        window.orientacion += 1
    window.update()


@bp.route('/delete/<int:product_id>', methods=('POST',))
def delete(product_id):
    product = Product.get(product_id)
    product.delete()

    return redirect(
        url_for('product.products')
    )
