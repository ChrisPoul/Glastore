from flask import (
    Blueprint, render_template, request, url_for,
    redirect, flash
)
from Glastore.models import Customer

bp = Blueprint('customer', __name__, url_prefix='/customer')

customer_heads = {
    "name": "Nombre del Cliente",
    "email": "Correo electrónico",
    "address": "Dirección"
}


@bp.route('/customers')
def customers():
    customers = Customer.query.all()

    return render_template(
        'customer/customers.html',
        customers=customers,
        heads=customer_heads
    )


@bp.route('/add_customer', methods=('GET', 'POST'))
def add_customer():

    if request.method == 'POST':
        customer = Customer(
            name=request.form['name'],
            email=request.form['email'],
            address=request.form['address']
        )
        error = customer.add()

        if not error:
            return redirect(
                url_for('customer.customers')
            )
        flash(error)

    return render_template(
        'customer/add_customer.html',
        heads=customer_heads
    )
