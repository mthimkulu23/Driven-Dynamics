from flask import jsonify, request, flash, redirect, url_for, render_template, session  
from ..models.enquire import car_enquiry
from .. import mongo  
from bson.objectid import *
from ..utils.auth import login_required, role_required
from flask import abort

def enquire():
    # If buyer arrives from a product page, seller_email and product_id will be in query params
    if request.method == 'GET':
        seller_email = request.args.get('seller_email', '')
        product_id = request.args.get('product_id', '')
        return render_template('enquire.html', seller_email=seller_email, product_id=product_id)

    # POST: store the enquiry and ensure it's tagged with the intended seller
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        contact = request.form.get('contact')
        seller_email = request.form.get('seller_email')
        product_id = request.form.get('product_id')

        enquiry = {
            'name': name,
            'email': email,
            'message': message,
            'contact': contact,
            'SellerEmail': seller_email,
            'ProductID': product_id
        }

        car_enquiry.user_enquire(enquiry)

        return redirect(url_for('catelog_buyer.catelog_buyer'))


@login_required
def retrieve_seller():
    # Show all conversations where the logged-in user is a participant.
    # This makes the inbox symmetric: buyers and sellers see the same threads.
    email = session.get('user_email')

    inquiries = car_enquiry.fetch_by_user(email)
    inquiries_list = list(inquiries)

    return render_template('retrieve_seller.html', inquiries=inquiries_list)


@login_required
def seller_message():
    # If GET: optionally prefill recipient info from query params
    if request.method == 'GET':
        recipient_email = request.args.get('email', '')
        recipient_name = request.args.get('name', '')
        product_id = request.args.get('product_id', '')
        return render_template('seller_message.html', recipient_email=recipient_email, recipient_name=recipient_name, product_id=product_id)

    # POST: seller replying to a buyer — reuse user_enquire to append/create the conversation
    if request.method == 'POST':
        name = request.form.get('name')
        message = request.form.get('message')
        recipient_email = request.form.get('recipient_email')
        product_id = request.form.get('product_id')

        seller_email = session.get('user_email')

        if not recipient_email:
            return render_template('seller_message.html', error="No recipient specified")

        # Build an enquiry where 'email' is the buyer's email so user_enquire will find/append the right conversation
        enquiry = {
            # email here is the buyer's email (recipient)
            'name': name,
            'email': recipient_email,
            'message': message,
            'contact': '',
            'SellerEmail': seller_email,
            'ProductID': product_id,
            # explicitly mark the sender as the seller so messages show correct sender
            'sender': seller_email,
            'sender_name': name
        }

        try:
            res = car_enquiry.user_enquire(enquiry)
            # Treat success if no exception was raised
            return redirect(url_for('enquire.retrieve_seller'))
        except Exception as e:
            print(f"Error saving seller_message: {e}")
            return render_template('seller_message.html', error="Failed to save message")


def terms_condition():
    return render_template('conditions.html')


@login_required
def conversation_view(conv_id):
    """Show a conversation thread and allow the logged-in user to reply."""
    email = session.get('user_email')
    # try to find conversation by ConversationID or _id
    try:
        from bson import ObjectId
        query = {'$or': [{'ConversationID': conv_id}, {'_id': ObjectId(conv_id)}]}
    except Exception:
        query = {'ConversationID': conv_id}

    conv = mongo.db.enquiry1.find_one(query)
    if not conv:
        abort(404)

    # ensure user is a participant
    if email not in [conv.get('BuyerEmail'), conv.get('SellerEmail')]:
        abort(403)

    # mark as read for this user (remove from unread_by)
    try:
        mongo.db.enquiry1.update_one({'_id': conv.get('_id')}, {'$pull': {'unread_by': email}})
    except Exception:
        try:
            mongo.db.enquiry1.update_one({'ConversationID': conv_id}, {'$pull': {'unread_by': email}})
        except Exception:
            pass

    if request.method == 'POST':
        # reply in-thread
        message = request.form.get('message')
        sender_name = request.form.get('name') or session.get('user_name') or ''
        sender_email = email
        if not message:
            return render_template('conversation.html', conversation=conv, error='Message required')

        from ..models.enquire import car_enquiry
        car_enquiry.append_message_by_conv(conv.get('ConversationID') or str(conv.get('_id')), sender_email, sender_name, message)
        # reload thread
        conv = mongo.db.enquiry1.find_one(query)
        return render_template('conversation.html', conversation=conv, success=True)

    return render_template('conversation.html', conversation=conv)


@login_required
def dismiss_conversation(conv_id):
    # Soft-delete: move conversation to trash so admins can restore it later
    from ..models.enquire import car_enquiry
    try:
        res = car_enquiry.delete_conversation(conv_id)
        return redirect(url_for('enquire.retrieve_seller'))
    except Exception as e:
        print(f"Error deleting conversation {conv_id}: {e}")
        return redirect(url_for('enquire.retrieve_seller'))


@role_required('admin')
def trash_list():
    """Admin: list trashed conversations."""
    from ..models.enquire import car_enquiry
    items = list(car_enquiry.fetch_trash())
    return render_template('trash_list.html', items=items)


@role_required('admin')
def restore_conversation(conv_id):
    from ..models.enquire import car_enquiry
    car_enquiry.restore_conversation(conv_id)
    return redirect(url_for('enquire.trash_list'))