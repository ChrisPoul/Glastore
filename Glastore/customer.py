from flask import (
    Blueprint, render_template, request, url_for,
    redirect, flash
)
from Glastore.models import Customer
from Glastore import get_form

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


@bp.route('/add', methods=('GET', 'POST'))
def add():
    form = get_form(customer_heads)

    if request.method == 'POST':
        form = get_form(customer_heads)
        customer = Customer(
            name=form['name'],
            email=form['email'],
            address=form['address'],
            cotizacion=form['cotizacion']
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
        form=form
    )


@bp.route('/update/<int:customer_id>', methods=('GET', 'POST'))
def update(customer_id):
    customer = Customer.get(customer_id)

    if request.method == "POST":
        form = get_form(customer_heads)
        customer.name = form['name']
        customer.email = form['email']
        customer.address = form['address']
        customer.cotizacion = form['cotizacion']
        error = customer.update()

        if not error:
            return redirect(
                url_for('customer.customers')
            )

        flash(error)

    return render_template(
        'customer/update.html',
        heads=customer_heads,
        customer=customer
    )


@bp.route('/delete/<int:customer_id>', methods=('POST',))
def delete(customer_id):
    customer = Customer.get(customer_id)
    customer.delete()

    return redirect(
        url_for('customer.customers')
    )
