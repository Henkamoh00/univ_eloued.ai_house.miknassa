from flask import Blueprint, render_template
from flask_login import current_user

mainBp = Blueprint("main", __name__)


@mainBp.route("/")
def home():
    isHomepage = True
    if current_user.is_authenticated:
        username = current_user.username
        return render_template(
            "pages/home.html", username=username, isHomepage=isHomepage
        )

    return render_template("pages/home.html", isHomepage=isHomepage)
