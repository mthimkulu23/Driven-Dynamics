from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..controllers import enquire_controller



app = Blueprint ('enquire', __name__)


app.route('/enquire', methods=['GET','POST'])(enquire_controller.enquire)
app.route('/retrieve_seller', methods=['GET','POST'])(enquire_controller.retrieve_seller)
app.route('/seller_message', methods=['GET','POST'])(enquire_controller.seller_message)

