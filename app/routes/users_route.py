from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..controllers import users_controller

# Create ONE blueprint for all user-related routes
app = Blueprint('users', __name__)

app.route('/')(users_controller.index)

app.route('/signup', methods=['GET','POST'])(users_controller.signup)

app.route('/login', methods=['GET','POST'])(users_controller.login)

app.route('/signup_buyer', methods=['GET','POST'])(users_controller.signup_buyer)

app.route('/login_buyer', methods=['GET','POST'])(users_controller.login_buyer)

app.route('/landing', methods=['GET','POST'])(users_controller.landing)
app.route('/about', methods=['GET','POST'])(users_controller.about)
app.route('/google_login', methods=['GET','POST'])(users_controller.google_login)
app.route('/authorize/google', methods=['GET','POST'])(users_controller.google_authorize)


