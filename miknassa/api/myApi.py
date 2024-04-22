from flask import Blueprint, request, jsonify
from flask_limiter import Limiter
from miknassa.models import *
from miknassa import bcrypt
from miknassa.helper import renameImage, convert_coordinates_to_address

apiBp = Blueprint("api", __name__)
limiter = Limiter(apiBp)


# لاستقبال بيانات تسجيل الدخول api
@apiBp.route("/users", methods=["POST"])
@limiter.limit('5 per minute', key_func=lambda: request.remote_addr)
def loginUser():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    if email is None or password is None:
        return jsonify({"error": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()
    address = Municipality.query.filter_by(id=user.municipalityId).first()

    if user and bcrypt.check_password_hash(user.password, password):
        return (
    jsonify(
        {
            "id": user.id,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "username": user.username,
            "gender": user.gender,
            "email": user.email,
            "phoneNumber": user.phoneNumber,
            "address": address.name,
            "houseNumber": user.houseNumber,
            "location": user.location,
            # "birthDate": user.birthDate,
            "birthPlace": user.birthPlace,
            "userTypeId": user.userTypeId,
            "imageFile": f"{request.host_url}media/{user.imageFile}",
            # "joinDate": user.joinDate,
        }
    ),
    200,
)

    return jsonify({"error": "User not found"}), 404


# لاستقبال التنبيه api
@apiBp.route("/garbage_alert", methods=["POST"])
def garbageAlert():

    data = request.json
    userId = data.get("userId")
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    if not latitude or not longitude:
        return "لا توجد بيانات مستلمة"+latitude, 400

    userId = int(userId)
    latitude = float(latitude)
    longitude = float(longitude)

    # address = convert_coordinates_to_address(latitude, longitude)
    address = location = f"{latitude}, {longitude}"
    garbageAlert = GarbageAlert(
        userId=userId,
        location=address,
        date=datetime.utcnow(),
        picture="",
    )
    db.session.add(garbageAlert)
    db.session.commit()

    return "", 200


# api لاستقبال التنبيه مع صورة
@apiBp.route("/garbage_alert_with_pic", methods=["POST"])
def garbageAlertPic():
    picPath = ""

    userId = request.form.get("userId")
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")
    if not latitude or not longitude or not userId:
        return "لا توجد بيانات مستلمة", 400

    userId = int(userId)
    latitude = float(latitude)
    longitude = float(longitude)

    # address = convert_coordinates_to_address(latitude, longitude)
    address = location = f"{latitude}, {longitude}"

    if "image" in request.files:
        image_file = request.files["image"]
        picPath = renameImage(image_file, "media/alert")
    else:
        return "لا توجد صورة مستلمة"+latitude, 400

    garbageAlert = GarbageAlert(
        userId=userId,
        location=address,
        date=datetime.utcnow(),
        picture="alert/" + picPath,
    )
    db.session.add(garbageAlert)
    db.session.commit()

    if picPath != "":
        return jsonify({"message": "Image uploaded successfully", "image_path": picPath}), 200



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
