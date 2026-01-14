from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..controllers import catelog_controller

app = Blueprint ('catelog_buyer', __name__)

app.route('/catelog', methods=['GET'])(catelog_controller.catelog)
app.route('/viewproduct', methods=['GET','POST'])(catelog_controller.viewproduct)
app.route('/edit_product', methods=['GET','POST'])(catelog_controller.update)
app.route('/confirm_update', methods=['GET','POST'])(catelog_controller.confirm_update)
app.route('/delete_product', methods=['POST'])(catelog_controller.delete_product)
app.route('/catelog_buyer', methods=['GET','POST'])(catelog_controller.catelog_buyer)
app.route('/buyer_message', methods=['GET','POST'])(catelog_controller.buyer_message)
app.route('/seller/my_cars', methods=['GET'])(catelog_controller.seller_my_cars)
app.route('/admin/pending', methods=['GET'])(catelog_controller.admin_pending)
app.route('/admin/approve/<product_id>', methods=['POST'])(catelog_controller.admin_approve)
