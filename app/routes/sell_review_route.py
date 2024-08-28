from flask import Blueprint
from ..controllers import sell_review_controller



app = Blueprint ('sell_review', __name__)

app.route('/sell_review', methods=['GET','POST'])(sell_review_controller.sell_review)


