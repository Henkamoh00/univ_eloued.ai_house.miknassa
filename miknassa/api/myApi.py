from flask import Blueprint, request, jsonify, current_app
from flask_limiter import Limiter
from sqlalchemy import null, desc
from miknassa.models import (
    User,
    Municipality,
    GarbageAlert,
    TruckType,
    Operation,
    Truck,
)
from miknassa import bcrypt, db
from miknassa.helper import (
    renameImage,
    convert_from_coordinates,
    convert_to_coordinates,
)
from datetime import datetime
import qrcode, secrets, os

# from io import BytesIO

apiBp = Blueprint("api", __name__)
limiter = Limiter(apiBp)


# لاستقبال بيانات تسجيل الدخول api
@apiBp.route("/users", methods=["POST"])
@limiter.limit("5 per minute", key_func=lambda: request.remote_addr)
def loginUser():
    try:
        data = request.json

        email = data.get("email")
        password = data.get("password")

        if email is None or email == "" or password is None or password == "":
            return "يوجد خطأ في البيانات المدخلة", 400

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            address = Municipality.query.filter_by(id=user.municipalityId).first()

            if user.location is not None:
                location = convert_to_coordinates(user.location)
            else:
                location = None

            userData = {
                "id": user.id,
                "firstName": user.firstName,
                "lastName": user.lastName,
                "username": user.username,
                "gender": user.gender,
                "email": user.email,
                "phoneNumber": user.phoneNumber,
                "address": address.name,
                "houseNumber": user.houseNumber,
                "location": location,
                "birthDate": user.birthDate.isoformat(),
                "birthPlace": user.birthPlace,
                "userTypeId": user.userTypeId,
                "imageFile": f"{request.host_url}media/{user.imageFile}",
                "joinDate": user.joinDate.isoformat(),
            }
            return (
                jsonify({"message": "تم تسجيل الدخول بنجاح", "userData": userData}),
                200,
            )

        return "خطأ في البريد الالكتروني أو كلمة المرور", 401

    except Exception as e:
        db.session.rollback()
        # raise
        return "يوجد مشكلة فالإتّصال\nحاول مجدّدا في وقت لاحق", 500

    finally:
        db.session.close()


# لاستقبال التنبيه api
@apiBp.route("/garbage_alert", methods=["POST"])
def garbageAlert():
    try:
        data = request.json

        userId = data.get("userId")
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        if (
            userId is None
            or userId == ""
            or latitude is None
            or latitude == ""
            or longitude is None
            or longitude == ""
        ):
            return "توجد مشكلة في تسجيل المعلومات", 400

        userId = int(userId)
        latitude = float(latitude)
        longitude = float(longitude)

        lat_str, lon_str = convert_from_coordinates(latitude, longitude)
        address = f"{lat_str}{lon_str}"

        garbageAlert = GarbageAlert(
            userId=userId,
            location=address,
            date=datetime.utcnow(),
        )
        db.session.add(garbageAlert)
        db.session.commit()

        return "تمّ إرسال التّنبيه", 200

    except Exception as e:
        db.session.rollback()
        # raise
        return "فشل إرسال التّنبيه", 500

    finally:
        db.session.close()


# api لاستقبال التنبيه مع صورة
@apiBp.route("/garbage_alert_with_pic", methods=["POST"])
def garbageAlertPic():
    try:
        picPath = ""

        userId = request.form.get("userId")
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")

        if (
            userId is None
            or userId == ""
            or latitude is None
            or latitude == ""
            or longitude is None
            or longitude == ""
        ):
            return "توجد مشكلة في تسجيل المعلومات", 400

        userId = int(userId)
        latitude = float(latitude)
        longitude = float(longitude)

        lat_str, lon_str = convert_from_coordinates(latitude, longitude)
        address = f"{lat_str}{lon_str}"

        if "image" in request.files:
            image_file = request.files["image"]
            picPath = renameImage(image_file, "media/alert/")
        else:
            return "لا توجد صورة مستلمة", 400

        garbageAlert = GarbageAlert(
            userId=userId,
            location=address,
            date=datetime.utcnow(),
            picture="alert/" + picPath,
        )
        db.session.add(garbageAlert)
        db.session.commit()

        return "تمّ ارسال التنبيه", 200

    except Exception:
        db.session.rollback()
        # raise
        return "فشل إرسال التّنبيه", 500

    finally:
        db.session.close()


# لجلب جميع التنبيهات
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
        return jsonify({"message": "تمّ تحميل البيانات", "alerts": data}), 200

    except Exception:
        db.session.rollback()
        # raise
        return "يوجد مشكلة فالإتّصال\nحاول مجدّدا في وقت لاحق", 500

    finally:
        db.session.close()


# لاستقبال عمليات اتمام المهام
@apiBp.route("/new_operation", methods=["POST"])
def newOperation():
    try:
        data = request.json

        garbageAlertId = data.get("itemId")
        userId = data.get("userId")
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        if (
            garbageAlertId is None
            or garbageAlertId == ""
            or userId is None
            or userId == ""
        ):
            return "تأكّد من المدخلات", 400

        if latitude is None or latitude == "" or longitude is None or longitude == "":
            return "فشل في تحديد موقعك", 400

        oldOperation = Operation.query.filter_by(alertId=garbageAlertId).first()
        if oldOperation:
            return "هذه المهمّة منجزة فعلاً", 200

        garbageAlertId = int(garbageAlertId)
        userId = int(userId)
        latitude = float(latitude)
        longitude = float(longitude)

        lat_str, lon_str = convert_from_coordinates(latitude, longitude)
        address = f"{lat_str}{lon_str}"

        truck = Truck.query.filter_by(userId=userId).first()

        newOperation = Operation(
            userId=userId,
            truckId=truck.id,
            alertId=garbageAlertId,
            location=address,
            date=datetime.utcnow(),
        )

        garbageAlert = GarbageAlert.query.filter_by(id=garbageAlertId).first()
        garbageAlert.status = True

        db.session.add(newOperation)
        db.session.commit()

        return "تمّ تأكيد إتمام المهمّة", 200

    except Exception:
        db.session.rollback()
        # raise
        return "فشل تأكيد إتمام المهمّة\nحاول مجدّدا في وقت لاحق", 500

    finally:
        db.session.close()


# لجلب جميع المستخدمين
@apiBp.route("/get_all_users", methods=["GET"])
def getAllUsers():
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
        return jsonify({"message": "تمّ تحميل البيانات", "users": data}), 200

    except Exception:
        db.session.rollback()
        # raise
        return "يوجد مشكلة فالإتّصال\nحاول مجدّدا في وقت لاحق", 500

    finally:
        db.session.close()


# لتغيير أدوار المستخدمين
@apiBp.route("/role_changing", methods=["POST"])
def roleChanging():
    try:
        data = request.json

        userId = data.get("itemId")
        adminId = data.get("userId")

        if userId is None or userId == "" or adminId is None or adminId == "":
            return "تأكّد من المدخلات", 400

        userId = int(userId)
        adminId = int(adminId)

        user = User.query.filter_by(id=userId).first()

        if user.userTypeId < 3:
            user.userTypeId = user.userTypeId + 1
        else:
            user.userTypeId = 1

        db.session.commit()

        return "تم تغيير الدّور", 200

    except Exception:
        db.session.rollback()
        # raise
        return "فشل تغيير الدّور", 500

    finally:
        db.session.close()


# لإدراج شاحنة
@apiBp.route("/add_truck", methods=["POST"])
def addTruck():
    try:
        data = request.json

        matricule = data.get("matricule")
        username = data.get("username")
        typeName = data.get("typeName")
        municipalityName = data.get("municipality")

        if (
            matricule is None
            or matricule == ""
            or municipalityName is None
            or municipalityName == ""
            or username is None
            or username == ""
            or typeName is None
            or typeName == ""
        ):
            return "تأكّد من المدخلات", 400

        truck = Truck.query.filter_by(matricule=matricule).first()
        if truck:
            return "لوحة الترقيم هذه مدرجة من قبل", 400

        last_row = Truck.query.order_by(desc(Truck.id)).first()

        if last_row:
            id = last_row.id + 1
        else:
            id = 1

        qr_data = f"id: {id}, matricule: {data['matricule']}, userId: {data['username']}, truckTypeId: {data['typeName']}"
        random_hex = secrets.token_hex(8)

        qr_code = qrcode.make(qr_data)
        qrCodePath = (
            os.path.join(current_app.root_path, "static/media/qrCodes/", random_hex)
            + ".jpg"
        )
        qr_code.save(qrCodePath)

        # عند الحاجة الى ارسالها كتسلسل بايتات او تخزينها في قاعدة البيانات
        # qr_bytes = BytesIO()
        # qr_image.save(qr_bytes, format='PNG')
        # qr_bytes.seek(0)

        if qr_code is None:
            return "يوجد مشكلة في إنشاء QR Code", 400

        user = User.query.filter_by(username=username).first()
        truckType = TruckType.query.filter_by(typeName=typeName).first()
        municipality = Municipality.query.filter_by(name=municipalityName).first()

        truck = Truck(
            matricule=matricule,
            userId=user.id,
            truckTypeId=truckType.id,
            addressId=municipality.id,
            qr_codePath="qrCodes/" + random_hex + ".jpg",
        )

        db.session.add(truck)
        db.session.commit()

        return "تمّ إدراج شاحنة جديدة", 200

    except Exception as e:
        db.session.rollback()
        # raise
        return "يوجد مشكلة فالإتّصال\nحاول مجدّدا في وقت لاحق ", 500

    finally:
        db.session.close()


# لجلب معلومات المستخدمين و انواع الشاحنات والولايات لملء كومبوبوكس
@apiBp.route("/get_combobox_data", methods=["GET"])
def getComboboxData():
    try:
        users = User.query.all()
        usersList = [user.username for user in users if user.userTypeId == 2]

        truckTypes = TruckType.query.all()
        truckTypesList = [truckType.typeName for truckType in truckTypes]

        municipalities = Municipality.query.all()
        municipalitiesList = [municipality.name for municipality in municipalities]

        return (
            jsonify(
                {
                    "message": "تمّ تحميل البيانات",
                    "truckTypesList": truckTypesList,
                    "usersList": usersList,
                    "municipalitiesList": municipalitiesList,
                }
            ),
            200,
        )

    except Exception:
        db.session.rollback()
        # raise
        return "يوجد مشكلة فالإتّصال\nحاول مجدّدا في وقت لاحق", 500

    finally:
        db.session.close()


# لتحديد مواقع الشاحنات على الخريطة
@apiBp.route("/truck_locations", methods=["POST"])
def truckLocations():
    try:
        data = request.json

        municipalityName = data.get("municipality")

        if municipalityName is None or municipalityName == "":
            return "توجد مشكلة في تحديد العنوان المطلوب", 400

        municipality = Municipality.query.filter_by(name=municipalityName).first()
        trucks = Truck.query.filter_by(addressId=municipality.id).all()

        data = [
            {
                "id": truck.id,
                "location": convert_to_coordinates(truck.lastLocation),
                "locationDate": truck.lastLocationDate,
            }
            for truck in trucks
            if truck.lastLocation is not null and truck.isActive == True
        ]

        if trucks is not None:
            print(data)
            return (
                jsonify({"message": "تمّ تحديد مواقع الشّاحنات", "truckLocations": data}),
                200,
            )
        else:
            return "فشل في تحديد مواقع الشاحنات.", 202

    except Exception as e:
        db.session.rollback()
        # raise
        return "فشل في تحديد مواقع الشاحنات", 500

    finally:
        db.session.close()


# لتغيير حالة الشاحنة من أجل ايقاف جلب معلومات الموقع الخاصة بها
@apiBp.route("/truck_tracking_state", methods=["POST"])
def truckTrackingState():
    try:
        data = request.json

        userId = data.get("userId")
        state = data.get("state")

        if userId is None or userId == "" or state is None or state == "":
            return "توجد مشكلة في استلام البيانات", 400

        userId = int(userId)

        truck = Truck.query.filter_by(userId=userId).first()

        if state == "close":
            truck.isActive = False
        elif state == "open":
            truck.isActive = True

        db.session.commit()

        return "تم تجاهل الشاحنة", 200

    except Exception as e:
        db.session.rollback()
        # raise
        return "فشل تجاهل الشاحنة", 500

    finally:
        db.session.close()


# لإدراج مواقع الشاحنات
@apiBp.route("/set_truck_location_updates", methods=["POST"])
def setTruckLocationUpdates():
    try:
        data = request.json

        userId = data.get("userId")
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        if (
            userId is None
            or userId == ""
            or latitude is None
            or latitude == ""
            or longitude is None
            or longitude == ""
        ):
            return "توجد مشكلة في استلام البيانات", 400

        userId = int(userId)
        latitude = float(latitude)
        longitude = float(longitude)

        lat_str, lon_str = convert_from_coordinates(latitude, longitude)
        address = f"{lat_str}{lon_str}"

        truck = Truck.query.filter_by(userId=userId).first()

        truck.userId = userId
        truck.lastLocation = address
        truck.lastLocationDate = datetime.utcnow()

        db.session.commit()

        return "تم ارسال الموقع", 200

    except Exception as e:
        db.session.rollback()
        # raise
        return "فشل ارسال الموقع", 500

    finally:
        db.session.close()


# لتحديد الموقع الحالي للمستخدم
@apiBp.route("/set_user_location", methods=["POST"])
def setUserLocation():
    try:
        data = request.json

        userId = data.get("userId")
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        if (
            userId is None
            or userId == ""
            or latitude is None
            or latitude == ""
            or longitude is None
            or longitude == ""
        ):
            return "توجد مشكلة في استلام البيانات", 400

        userId = int(userId)
        latitude = float(latitude)
        longitude = float(longitude)

        lat_str, lon_str = convert_from_coordinates(latitude, longitude)
        address = f"{lat_str}{lon_str}"

        user = User.query.filter_by(id=userId).first()

        user.id = userId
        user.location = address

        db.session.commit()

        return "تم تحديد موقعك بنجاح", 200

    except Exception as e:
        db.session.rollback()
        # raise
        return "فشل في تحديد موقعك", 500

    finally:
        db.session.close()
