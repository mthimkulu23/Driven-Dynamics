from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..controllers import enquire_controller



app = Blueprint ('enquire', __name__)


app.route('/enquire', methods=['GET','POST'])(enquire_controller.enquire)
app.route('/retrieve_seller', methods=['GET','POST'])(enquire_controller.retrieve_seller)
app.route('/seller_message', methods=['GET','POST'])(enquire_controller.seller_message)
app.route('/conversation/<conv_id>', methods=['GET','POST'])(enquire_controller.conversation_view)
app.route('/conversation/<conv_id>/dismiss', methods=['POST'])(enquire_controller.dismiss_conversation)
app.route('/terms_condition_apply')(enquire_controller.terms_condition)
app.route('/admin/trash', methods=['GET'])(enquire_controller.trash_list)
app.route('/admin/trash/<conv_id>/restore', methods=['POST'])(enquire_controller.restore_conversation)

