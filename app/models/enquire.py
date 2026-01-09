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
        buyer = enquiry.get('email')
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
    def count_messages_for_user(email):
        """Count conversations where the user is the seller (keeps original semantics).

        Use `fetch_by_user` for retrieving both participants' conversations.
        """
        return mongo.db.enquiry1.count_documents({"SellerEmail": email})