from flask import (
    Blueprint, render_template, request, url_for,
    redirect, flash
)
from Glastore.models import get_form
from Glastore.models.customer import Customer, customer_heads
from Glastore.views.auth import login_required

bp = Blueprint('customer', __name__, url_prefix='/customer')


@bp.route('/customers', methods=('POST', 'GET'))
def customers():
    customers = Customer.get_all()
    autocomplete_data = [customer.name for customer in customers]
    placeholder = "Escribe el nombre o el email del cliente que buscas..."
    if request.method == "POST":
        search_term = request.form["search_term"]
        customer = Customer.search(search_term)
        if customer:
            return redirect(
                url_for('customer.profile', customer_id=customer.id)
            )
        else:
            flash("No se encontró ningún cliente")

    return render_template(
        'customer/customers.html',
        customers=customers,
        heads=customer_heads,
        autocomplete_data=autocomplete_data,
        placeholder=placeholder
    )


@bp.route('/profile/<int:customer_id>', methods=('POST', 'GET'))
@login_required
def profile(customer_id):
    customer = Customer.get(customer_id)

    return render_template(
        'customer/profile.html', customer=customer
    )


@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    form = get_form(customer_heads)

    if request.method == 'POST':
        form = get_form(customer_heads)
        customer = Customer(
            name=form['name'],
            email=form['email'],
            address=form['address']
        )
        error = customer.request.add()

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
@login_required
def update(customer_id):
    customer = Customer.get(customer_id)

    if request.method == "POST":
        error = customer.request.update()

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
@login_required
def delete(customer_id):
    customer = Customer.get(customer_id)
    customer.delete()

    return redirect(
        url_for('customer.customers')
    )
