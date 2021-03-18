from flask import (
    Blueprint, render_template, request, url_for,
    redirect, flash
)
from Glastore.models import Customer

bp = Blueprint('customer', __name__, url_prefix='/customer')

customer_heads = {
    "name": "Nombre del Cliente",
    "email": "Correo electrónico",
    "address": "Dirección",
    "cotizacion": "Cotización"
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
            address=request.form['address'],
            cotizacion=request.form['cotizacion']
        )
        error = customer.add()

        if not error:
            return redirect(
                url_for('customer.customers')
            )

        flash(error)

    return render_template(
        'customer/add.html',
        heads=customer_heads,
        customer=customer
    )


@bp.route('/update_customer/<int:customer_id>', methods=('GET', 'POST'))
def update_customer(customer_id):
    customer = Customer.get(customer_id)

    if request.method == "POST":
        customer.name = request.form['name']
        customer.email = request.form['email']
        customer.address = request.form['address']
        customer.cotizacion = request.form['cotizacion']
        error = customer.update()

        if not error:
            return redirect(
                url_for('customer.customers')
            )
        flash(error)

    return render_template(
        'customer/update.html'
    )
