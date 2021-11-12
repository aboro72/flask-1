from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        abbreviation = request.form.get('abbreviation')
        password = request.form.get('password')

        user = User.query.filter_by(abbreviation=abbreviation).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successsfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again!', category='error')
        else:
            flash('Abbreviation does not exits', category='error')
    return render_template("login.html")


@auth.route('/logout')
def logout():
    return render_template("logout.html")


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        abbreviation = request.form.get('abbreviation')
        firstname = request.form.get('firstName')
        lastname = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(abbreviation=abbreviation).first()

        if user:
            flash('Abbreviation already exit', category='error')
        elif len(abbreviation) > 4:
            flash('abbreviation must 4 charaters', category='error')
        elif len(firstname) < 2:
            flash('First Name must be greater than 2 charaters', category='error')
        elif len(lastname) < 4:
            flash('FLast Name must be greater than 2 charaters', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(password1) < 7:
            flash('Password is less than 7 characters', category='error')
        else:
            # add user to database
            new_user = User(abbreviation=abbreviation, firstname=firstname, lastname=lastname, password=generate_password_hash(password1, method='sha256' ))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html")

