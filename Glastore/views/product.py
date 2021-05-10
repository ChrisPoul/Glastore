from flask import (
    Blueprint, redirect, url_for
)
from Glastore.models.product import Product, product_heads
from Glastore.models.window import Window
from Glastore.views.auth import login_required

bp = Blueprint('product', __name__, url_prefix='/product')


@bp.route('/select_next_window/<int:id>')
@login_required
def select_next_window(id):
    product = Product.get(id)
    product.orientation.select_next_window()

    return redirect(
        url_for('quote.edit', id=product.quote_id)
    )


@bp.route('/rotate_window/<int:id>')
@login_required
def rotate_window(id):
    product = Product.get(id)
    product.orientation.rotate_window()

    return redirect(
        url_for('quote.edit', id=product.quote_id)
    )


@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    product = Product.get(id)
    quote_id = product.quote.id
    product.delete()

    return redirect(
        url_for('quote.edit', id=quote_id)
    )
