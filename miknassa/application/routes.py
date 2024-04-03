from flask import Blueprint
from flask import render_template, redirect, url_for
from flask_login import current_user, login_required

appBp = Blueprint('application', __name__)

@appBp.route('/dashboard')
@login_required
def dashboard():
    if current_user.userTypeId == 1:
        return redirect(url_for('main.home'))
    else:
        return render_template('pages/dashboard.html')


@appBp.route('/app')
@login_required
def application():
    return render_template('pages/map.html')
