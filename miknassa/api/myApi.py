from flask import Blueprint, request, jsonify
from flask_limiter import Limiter
from miknassa.models import *
from miknassa import bcrypt
from miknassa.helper import renameImage, convert_coordinates_to_address

apiBp = Blueprint("api", __name__)
limiter = Limiter(apiBp)


# لاستقبال بيانات تسجيل الدخول api
@apiBp.route("/users", methods=["POST"])
# @limiter.limit('5 per minute', key_func=lambda: request.remote_addr)
def loginUser():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    if email is None or password is None:
        return jsonify({"error": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return (
            jsonify(
                {"email": user.email, "fName": user.firstName, "lName": user.lastName}
            ),
            200,
        )

    return jsonify({"error": "User not found"}), 404


# لاستقبال التنبيه api
@apiBp.route("/garbage_alert", methods=["POST"])
def garbageAlert():
    picPath = ""

    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")
    
    if not latitude or not longitude:
        return "", 400

    latitude = float(latitude)
    longitude = float(longitude)

    address = convert_coordinates_to_address(latitude, longitude)

    if "image" in request.files:
        image_file = request.files["image"]
        picPath = renameImage(image_file.filename, "media/alert")

    garbageAlert = GarbageAlert(
        userId=1,
        location=address,
        date=datetime.utcnow(),
        picture=picPath,
    )
    db.session.add(garbageAlert)
    db.session.commit()

    if picPath != "":
        return jsonify({"message": "Image uploaded successfully", "image_path": picPath}), 200
    

    return "", 200




# # لاستقبال صورة القمامة api
# @apiBp.route("/rubbish_pic", methods=["POST"])
# def rubbishPic():
#     if "image" not in request.files:
#         return jsonify({"error": "No image part in the request"}), 400

#     image = request.files["image"]

#     if image.filename == "":
#         return jsonify({"error": "No selected image"}), 400

#     if image:
#         image = renameImage(image.filename, "media/alert")
#         # user.imageFile = image
#         return jsonify({"message": "Image uploaded successfully", "image_path": image.filename}), 200

#     return jsonify({"error": "Unknown error occurred"}), 500
