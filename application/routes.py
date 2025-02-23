from flask import Blueprint
from flask import render_template, redirect, url_for
from flask_login import current_user, login_required

appBp = Blueprint("application", __name__)


@appBp.route("/dashboard")
@login_required
def dashboard():
    isHomepage = False
    username = current_user.username
    if current_user.userTypeId == 1:
        return redirect(url_for("main.home"))
    else:
        return render_template(
            "pages/dashboard.html", username=username, isHomepage=isHomepage
        )


@appBp.route("/app")
@login_required
def application():
    isHomepage = False
    username = current_user.username
    return render_template("pages/map.html", username=username, isHomepage=isHomepage)
