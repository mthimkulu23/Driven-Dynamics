from app import mongo
from datetime import datetime
from uuid import uuid4


class car_enquiry:
    """Conversation-based enquiries.

    Documents live in the `enquiry1` collection and have this shape:
      {
        ConversationID: str(uuid4()),
        BuyerEmail: str,
        SellerEmail: str,
        ProductID: str,
        participants: [buyer, seller],
        messages: [ { from, name, message, contact, timestamp } , ... ],
        created_at, updated_at
      }

    This allows both buyer and seller to retrieve the same conversation by querying
    for their email address (no need to exchange raw emails outside the site).
    """

    @staticmethod
    def user_enquire(enquiry):
        """Create a new conversation or append to an existing one.

        Expects enquiry to include at least:
          - email (buyer email)
          - SellerEmail
          - message
          - ProductID (optional)
        """
        # buyer email: prefer explicit 'email' field, fall back to 'sender' if present
        buyer = enquiry.get('email') or enquiry.get('sender')
        seller = enquiry.get('SellerEmail')
        product_id = enquiry.get('ProductID')

        # Determine actual sender: allow caller to specify 'sender' (email) and 'sender_name'
        sender_email = enquiry.get('sender') or buyer
        sender_name = enquiry.get('sender_name') or enquiry.get('name')

        # Basic payload for the message
        message_doc = {
            'from': sender_email,
            'name': sender_name,
            'message': enquiry.get('message'),
            'contact': enquiry.get('contact'),
            'timestamp': datetime.utcnow()
        }

        # Try to find an existing conversation between the same buyer/seller for the product
        query = {'BuyerEmail': buyer, 'SellerEmail': seller}
        if product_id:
            query['ProductID'] = product_id

        existing = mongo.db.enquiry1.find_one(query)
        if existing:
            # append message
            mongo.db.enquiry1.update_one({'_id': existing['_id']}, {'$push': {'messages': message_doc}, '$set': {'updated_at': datetime.utcnow()}})
            return existing

        # create a new conversation document
        conv = {
            'ConversationID': str(uuid4()),
            'BuyerEmail': buyer,
            'SellerEmail': seller,
            'ProductID': product_id,
            'participants': [buyer, seller],
            'messages': [message_doc],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        return mongo.db.enquiry1.insert_one(conv)

    @staticmethod
    def fetch_seller(email):
        """Return conversations where the given email is the SellerEmail."""
        return mongo.db.enquiry1.find({"SellerEmail": email})

    @staticmethod
    def fetch_by_user(email):
        """Return conversations where the given email is a participant (buyer or seller)."""
        return mongo.db.enquiry1.find({'$or': [{'BuyerEmail': email}, {'SellerEmail': email}]})

    @staticmethod
    def append_message_by_conv(conv_id, sender_email, sender_name, message, contact=''):
        """Append a message to conversation identified by ConversationID or ObjectId.

        Returns the update result.
        """
        query = {'$or': [{'ConversationID': conv_id}, {'_id': conv_id}]}
        # If conv_id looks like an ObjectId, try converting
        # Resolve conversation first so we can compute the other participant for unread flags
        try:
            from bson import ObjectId
            query_by_id = {'$or': [{'ConversationID': conv_id}, {'_id': ObjectId(conv_id)}]}
        except Exception:
            query_by_id = {'ConversationID': conv_id}

        conv = mongo.db.enquiry1.find_one(query_by_id)
        if not conv:
            return None

        # Determine the other participant to mark unread
        buyer = conv.get('BuyerEmail')
        seller = conv.get('SellerEmail')
        other = None
        if sender_email and buyer and sender_email.lower() == buyer.lower():
            other = seller
        else:
            other = buyer

        message_doc = {
            'from': sender_email,
            'name': sender_name,
            'message': message,
            'contact': contact,
            'timestamp': datetime.utcnow()
        }

        update = {
            '$push': {'messages': message_doc},
            '$set': {'updated_at': datetime.utcnow()}
        }
        # set unread_by to the other participant (if exists)
        if other:
            update['$addToSet'] = {'unread_by': other}

        return mongo.db.enquiry1.update_one(query_by_id, update)

    @staticmethod
    def archive_conversation(conv_id, user_email):
        """Mark a conversation as archived by adding the user_email to archived_by list."""
        try:
            from bson import ObjectId
            query = {'$or': [{'ConversationID': conv_id}, {'_id': ObjectId(conv_id)}]}
        except Exception:
            query = {'ConversationID': conv_id}

        return mongo.db.enquiry1.update_one(query, {'$addToSet': {'archived_by': user_email}})

    @staticmethod
    def delete_conversation(conv_id):
        """Move a conversation to the trash collection (soft-delete) and remove from active collection.

        This preserves data and enables admin restore.
        """
        try:
            from bson import ObjectId
            query = {'$or': [{'ConversationID': conv_id}, {'_id': ObjectId(conv_id)}]}
        except Exception:
            query = {'ConversationID': conv_id}

        conv = mongo.db.enquiry1.find_one(query)
        if not conv:
            return None

        # copy to trash collection with a deleted_at timestamp
        conv['_deleted_at'] = datetime.utcnow()
        mongo.db.enquiry_trash.insert_one(conv)
        return mongo.db.enquiry1.delete_one({'_id': conv['_id']})

    @staticmethod
    def restore_conversation(conv_id):
        """Restore a conversation from the trash collection back into the active collection."""
        try:
            from bson import ObjectId
            query = {'$or': [{'ConversationID': conv_id}, {'_id': ObjectId(conv_id)}]}
        except Exception:
            query = {'ConversationID': conv_id}

        conv = mongo.db.enquiry_trash.find_one(query)
        if not conv:
            return None

        # remove the _deleted_at marker
        conv.pop('_deleted_at', None)
        # insert back
        mongo.db.enquiry1.insert_one(conv)
        return mongo.db.enquiry_trash.delete_one({'_id': conv['_id']})

    @staticmethod
    def fetch_trash():
        """Return all trashed conversations (admin use)."""
        return mongo.db.enquiry_trash.find()

    @staticmethod
    def count_messages_for_user(email):
        """Count conversations where the user is the seller (keeps original semantics).

        Use `fetch_by_user` for retrieving both participants' conversations.
        """
        return mongo.db.enquiry1.count_documents({"SellerEmail": email})