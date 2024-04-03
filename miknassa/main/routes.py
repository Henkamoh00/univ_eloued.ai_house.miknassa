from flask import Blueprint
from flask import render_template

mainBp = Blueprint('main', __name__)

@mainBp.route('/')
def home():
    return render_template('pages/home.html')
