from flask import Blueprint, request, jsonify
from flask_limiter import Limiter
from sqlalchemy import null
from miknassa.models import *
from miknassa import bcrypt
from miknassa.helper import renameImage, convert_coordinates

apiBp = Blueprint("api", __name__)
limiter = Limiter(apiBp)


# لاستقبال بيانات تسجيل الدخول api
@apiBp.route("/users", methods=["POST"])
@limiter.limit("5 per minute", key_func=lambda: request.remote_addr)
def loginUser():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    if email is None or password is None:
        return jsonify({"خطأ": "لا توجد بيانات مستلمة"}), 400

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
    if not latitude or not longitude or not userId:
        return "لا توجد بيانات مستلمة" + latitude, 400

    userId = int(userId)
    latitude = float(latitude)
    longitude = float(longitude)

    lat_str, lon_str = convert_coordinates(latitude, longitude)
    address = f"{lat_str}{lon_str}"

    garbageAlert = GarbageAlert(
        userId=userId,
        location=address,
        date=datetime.utcnow(),
        # picture="",
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

    lat_str, lon_str = convert_coordinates(latitude, longitude)
    address = f"{lat_str}{lon_str}"

    if "image" in request.files:
        image_file = request.files["image"]
        picPath = renameImage(image_file, "media/alert")
    else:
        return "لا توجد صورة مستلمة" + latitude, 400

    garbageAlert = GarbageAlert(
        userId=userId,
        location=address,
        date=datetime.utcnow(),
        picture="alert/" + picPath,
    )
    db.session.add(garbageAlert)
    db.session.commit()

    if picPath != "":
        return (
            jsonify({"message": "Image uploaded successfully", "image_path": picPath}),
            200,
        )


@apiBp.route("/get_garbage_alerts", methods=["GET"])
def garbageAlerts():
    try:
        garbageAlerts = GarbageAlert.query.all()

        data = [
            {
                "id": garbageAlert.id,
                "location": garbageAlert.location,
                "status": garbageAlert.status,
            }
            for garbageAlert in garbageAlerts
        ]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@apiBp.route("/new_operation", methods=["POST"])
def newOperation():
    data = request.json

    garbageAlertId = data.get("itemId")
    userId = data.get("userId")
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    oldOperation = Operation.query.filter_by(alertId=garbageAlertId).first()
    if oldOperation != null:
        return "", 200

    if garbageAlertId is None or userId is None:
        return jsonify({"خطأ": "لا توجد بيانات مستلمة"}), 400

    if not latitude or not longitude:
        return "لا توجد احداثيات مستلمة" + latitude, 400

    garbageAlertId = int(garbageAlertId)
    userId = int(userId)
    latitude = float(latitude)
    longitude = float(longitude)

    lat_str, lon_str = convert_coordinates(latitude, longitude)
    address = f"{lat_str}{lon_str}"

    truck = Truck.query.filter_by(userId=userId).first()

    garbageAlert = GarbageAlert.query.filter_by(id=garbageAlertId).first()
    garbageAlert.status = True

    newOperation = Operation(
        truckId=truck.id,
        alertId=garbageAlertId,
        location=address,
        date=datetime.utcnow(),
    )

    db.session.add(newOperation)
    db.session.commit()

    return "", 200


@apiBp.route("/get_all_users", methods=["GET"])
def allUsers():
    try:
        users = User.query.all()

        data = [
            {
                "id": user.id,
                "firstName": user.firstName,
                "lastName": user.lastName,
                "username": user.username,
                "role": (
                    "عادي"
                    if user.userTypeId == 1
                    else ("سائق" if user.userTypeId == 2 else "مدير")
                ),
            }
            for user in users
        ]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@apiBp.route("/role_changing", methods=["POST"])
def roleChanging():
    try:
        data = request.json

        userId = data.get("itemId")
        adminId = data.get("userId")

        if userId is None or adminId is None:
            return jsonify({"خطأ": "لا توجد بيانات مستلمة"}), 400

        userId = int(userId)
        adminId = int(adminId)

        user = User.query.filter_by(id=userId).first()

        if user.userTypeId < 3:
            user.userTypeId = user.userTypeId + 1
        else:
            user.userTypeId = 1

        db.session.commit()

        return "تم تغيير الدور", 200

    except Exception as e:
        return "فشل تغيير الدّور", 500


@apiBp.route("/add_truck", methods=["POST"])
def addTruck():
    try:
        data = request.json

        matricule = data.get("matricule")
        userId = data.get("userId")
        truckTypeId = data.get("matricule")
        qr_code = data.get("qr_code")

        if (
            matricule is None
            or userId is None
            or truckTypeId is None
            or qr_code is None
        ):
            return jsonify({"خطأ": "لا توجد بيانات مستلمة"}), 400

        matricule = int(matricule)
        userId = int(userId)
        truckTypeId = int(truckTypeId)

        newOperation = Operation(
            matricule=matricule,
            userId=userId,
            truckTypeId=truckTypeId,
            qr_code=qr_code,
        )

        db.session.commit()

        return "تمّ إدراج شاحنة جديدة", 200

    except Exception as e:
        return "", 500


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
