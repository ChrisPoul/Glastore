from flask import (
    Blueprint, redirect, url_for
)
from Glastore.models.product import Product, product_heads

bp = Blueprint('product', __name__, url_prefix='/product')


@bp.route('/delete/<int:product_id>', methods=('POST',))
def delete(product_id):
    product = Product.get(product_id)
    product.delete()

    return redirect(
        url_for('product.products')
    )
