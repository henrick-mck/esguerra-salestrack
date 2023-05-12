from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from .models import Product, Order, OrderItem, Customer
from . import db
import json
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String


views = Blueprint('views', __name__)


############################ CUSTOMER VIEWS##############################################

# customer list


@views.route('/customer', methods=['GET', 'POST'])
def customer():
    result = Customer.query.all()

    return render_template("customer.html", result=result)

# Add customer


@views.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        customerName = request.form.get('customerName')
        contactNum = request.form.get('contactNum')
        address = request.form.get('address')
        email = request.form.get('email')

        new_customer = Customer(
            name=customerName, contactNum=contactNum, address=address, email=email)

        db.session.add(new_customer)
        db.session.commit()

        flash('New Customer Added', category='success')
        return redirect(url_for('views.customer'))

    return render_template("new_customer.html")

# edit customer


@views.route('/edit_customer/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    name_to_update = Customer.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form.get('customerName')
        name_to_update.contactNum = request.form.get('contactNum')
        name_to_update.address = request.form.get('address')
        name_to_update.email = request.form.get('email')
        try:
            db.session.commit()
            flash('User Updated Successfuly', category='success')
            return redirect(url_for('views.customer'))
        except:
            print("Here")
            flash('Error! Looks like there was a problem', category="error")
            return redirect(url_for('views.customer'))

    else:
        return render_template("edit_customer.html", name_to_update=name_to_update)


# delete customer
@views.route('/delete-customer', methods=["POST"])
def delete_customer():
    customer = json.loads(request.data)
    customerId = customer['rowId']
    customer = Customer.query.get(customerId)
    if customer:
        db.session.delete(customer)
        db.session.commit()

    return jsonify({})


################################## PRODUCT VIEWS#######################################

# product list
@views.route('/product_list', methods=['GET', 'POST'])
def productList():
    result = Product.query.all()

    return render_template("product_list.html", result=result)

# new product


@views.route('/new_product', methods=['GET', 'POST'])
def new_product():
    if request.method == 'POST':
        name = request.form.get('productName')
        price = request.form.get('price')
        description = request.form.get('description')

        new_product = Product(
            name=name, price=price, description=description)

        db.session.add(new_product)
        db.session.commit()

        flash('New Product Added', category='success')
        return redirect(url_for('views.productList'))

    return render_template("new_product.html")

# edit product


@views.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product_to_update = Product.query.get_or_404(id)
    if request.method == "POST":
        product_to_update.name = request.form.get('productName')
        product_to_update.price = request.form.get('price')
        product_to_update.description = request.form.get('description')
        try:
            db.session.commit()
            flash('Product Updated Successfuly', category='success')
            return redirect(url_for('views.productList'))
        except:
            flash('Error! Looks like there was a problem', category="error")
            return redirect(url_for("views.productList"))

    else:
        return render_template("edit_product.html", product_to_update=product_to_update)


# delete product
@views.route('/delete-product', methods=["POST"])
def delete_product():
    product = json.loads(request.data)
    productID = product['rowId']
    product = Product.query.get(productID)
    if product:
        db.session.delete(product)
        db.session.commit()

    return jsonify({})

#################################### ORDER VIEWS #######################################


@views.route('/new_order')
def new_order_redir():
    newest_order = Order.query.order_by(Order.orderID.desc()).first()
    return redirect(url_for('views.new_order', orderID=newest_order.orderID+1))

# add new item to order


@views.route('/new_order/<int:orderID>', methods=['GET', 'POST'])
def new_order(orderID):
    productList = Product.query.all()
    # orderItemList = OrderItem.query.filter(OrderItem.orderID == orderID).all()
    exists = Order.query.get(orderID)

    if not exists:
        exists = Order(orderID=orderID, totalPrice=0)

        db.session.add(exists)
        db.session.commit()

    if request.method == "POST":
        # create orderItem
        productID = request.form.get('productItemID')
        qty = request.form.get('qty')

        product_in_order = OrderItem.query.filter_by(
            productID=productID, orderID=orderID).first()
        if (product_in_order):

            product_in_order.qty = qty
            db.session.commit()

            flash('Product Quantity Edited', category='success')

        else:

            new_orderItem = OrderItem(
                productID=productID, qty=qty, orderID=exists.orderID)

            db.session.add(new_orderItem)
            db.session.commit()

            flash('New Product Added', category='success')

        # computing total price of orders
        total = 0
        for items in exists.orderItem:
            total = total + items.product.price * items.qty

        exists.totalPrice = total
        db.session.commit()

        # return render_template("new_order.html", orderID=orderID, orderItemID=orderItemID, productList=productList)
        return render_template("new_order.html", exists=exists, productList=productList)

    # computing total price of orders
    total = 0
    for items in exists.orderItem:
        total = total + items.product.price*items.qty

    exists.totalPrice = total
    db.session.commit()

    return render_template("new_order.html", exists=exists, productList=productList)

# delete orderItem


@views.route('/delete-orderItem', methods=["POST"])
def delete_orderItem():
    orderItem = json.loads(request.data)
    orderItemID = orderItem['orderItemID']
    orderItem = OrderItem.query.get(orderItemID)
    print(orderItem)
    if orderItem:
        db.session.delete(orderItem)
        db.session.commit()

    return jsonify({})

############################### SALES LIST ##########################
# sales list


@views.route('/', methods=['GET', 'POST'])
def sales_list():
    sales = Order.query.all()
    productList = Product.query.all()
    itemList = OrderItem.query.all()

    # values for number of orders
    total_orders = 0
    for row in sales:
        total_orders = total_orders + 1

    # Sales revenue

    return render_template("sales_list.html", sales=sales, total_orders=total_orders, productList=productList, itemList=itemList)

# finish order


@views.route('/finish_order/<int:orderID>')
def finish_order(orderID):
    # deletes order if empty
    finishOrder = Order.query.get(orderID)
    print(finishOrder.orderItem)
    if not finishOrder.orderItem:
        db.session.delete(finishOrder)
        db.session.commit()

    return redirect(url_for('views.sales_list'))


@views.route('/delete_order/<int:orderID>')
def delete_order(orderID):
    # deletes order if empty
    deleteOrder = Order.query.get(orderID)
    db.session.delete(deleteOrder)
    db.session.commit()

    return redirect(url_for('views.sales_list'))
