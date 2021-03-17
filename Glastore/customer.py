from flask import (
    Blueprint, render_template, request
)

bp = Blueprint('customer',__name__, url_prefix='/customer')


@bp.route('/customers')
def customers():
    
    return render_template(
        'customer/customers.html'
    )


@bp.route('/add_customer')
def add_customer():

    return render_template(
        'customer/add_customer.html'
    )
