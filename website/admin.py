from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

admin = Blueprint('admin', __name__)


@admin.route('/admin')
def adminseite():
    return '<h1> ADMIN Seite </h1>'