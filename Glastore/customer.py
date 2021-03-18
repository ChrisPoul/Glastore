from flask import (
    Blueprint, render_template, request, url_for,
    redirect
)
from Glastore.models import Customer, add_to_db

bp = Blueprint('customer', __name__, url_prefix='/customer')


@bp.route('/customers')
def customers():
    customers = Customer.query.all()

    return render_template(
        'customer/customers.html',
        customers=customers
    )


@bp.route('/add_customer', methods=('GET', 'POST'))
def add_customer():

    if request.method == 'POST':
        customer = Customer(
            name=request.form['name'],
            email=request.form['email'],
            address=request.form['address']
        )
        add_to_db(customer)

        return redirect(
            url_for('customer.customers')
        )

    return render_template(
        'customer/add_customer.html'
    )
