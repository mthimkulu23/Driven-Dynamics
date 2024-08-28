from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..controllers import review_rating_controller



app = Blueprint ('review', __name__)





app.route('/review', methods=['GET','POST'])(review_rating_controller.review)

app.route('/review_display12', methods=['GET','POST'])(review_rating_controller.review_display12)
app.route('/edit_review', methods=['GET','POST'])(review_rating_controller.edit_review)
app.route('/delete_review', methods=['GET','POST'])(review_rating_controller.delete_review)


