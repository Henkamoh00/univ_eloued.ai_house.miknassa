from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from miknassa.users.forms import (
    JoinForm,
    LoginForm,
    EditProfileForm,
    ChangePasswordForm,
    ForgotPasswordForm,
    ResetPasswordForm,
)
from miknassa.models import User, Municipality, Dayra, Wilaya
from miknassa.users.helper import sendResetEmail
from miknassa.helper import renameImage
from miknassa import db, bcrypt


usersBp = Blueprint("users", __name__)


@usersBp.route("/miknassa", methods=["GET", "POST"])
def login():
    try:
        if current_user.is_authenticated:
            return redirect(url_for("main.home"))

        joinForm = JoinForm()
        loginForm = LoginForm()

        if request.form.get("submit") == "انضمام":
            if joinForm.validate_on_submit():
                hashedPassword = bcrypt.generate_password_hash(
                    joinForm.password.data
                ).decode("utf-8")
                user = User(
                    firstName=joinForm.firstName.data,
                    lastName=joinForm.lastName.data,
                    username=joinForm.username.data,
                    gender=joinForm.gender.data,
                    email=joinForm.email.data,
                    phoneNumber=joinForm.phoneNumber.data,
                    municipalityId=joinForm.municipality.data,
                    userTypeId=1,
                    password=hashedPassword,
                )
                db.session.add(user)
                db.session.commit()
                flash(
                    f"مرحبا بك {joinForm.username.data}، تم انشاء الحساب بنجاح.",
                    "success",
                )
                return redirect(url_for("users.login"))
            else:
                flash(f"تأكّد من صحة الإدخال.", "warning")
    except Exception as e:
        db.session.rollback()
        # raise
        flash(f"يوجد مشكلة فالإتّصال\nحاول مجدّدا في وقت لاحق", 500, "error")

    finally:
        db.session.close()

    try:
        if request.form.get("submit") == "دخـول":
            if loginForm.validate_on_submit():
                user = User.query.filter_by(email=loginForm.email.data).first()

                if user and bcrypt.check_password_hash(
                    user.password, loginForm.password.data
                ):
                    login_user(user, remember=loginForm.remember.data)
                    nextPage = request.args.get("next")
                    flash(f"مرحبا {user.username} تم تسجيل الدخول بنجاح.", "success")
                    if user.userTypeId == 1:
                        return (
                            redirect(nextPage)
                            if nextPage
                            else redirect(url_for("main.home"))
                        )
                    elif user.userTypeId == 2:
                        return (
                            redirect(nextPage)
                            if nextPage
                            else redirect(url_for("application.dashboard"))
                        )
                    elif user.userTypeId == 3:
                        return (
                            redirect(nextPage)
                            if nextPage
                            else redirect(url_for("application.dashboard"))
                        )
                    else:
                        flash(f"يوجد خلل في الحساب", "error")
                else:
                    flash(f"فشل تسجيل الدخول، حاول مجدّدًا.", "error")
    except Exception as e:
        # raise
        flash(f"يوجد مشكلة فالإتّصال\nحاول مجدّدا في وقت لاحق", 500, "error")

    finally:
        db.session.close()

    return render_template("forms/login.html", joinForm=joinForm, loginForm=loginForm)


@usersBp.route("/logout")
def logout():
    logout_user()
    flash(f"تم تسجيل الخروج بنجاح", "success")
    return redirect(url_for("users.login"))


@usersBp.route("/reset password", methods=["GET", "POST"])
def forgotPassword():
    try:
        if current_user.is_authenticated:
            return redirect(url_for("main.home"))
        forgotPasswordForm = ForgotPasswordForm()
        if forgotPasswordForm.validate_on_submit():
            user = User.query.filter_by(email=forgotPasswordForm.email.data).first()
            if user:
                sendResetEmail(user)
            flash(
                "إذا كان هذا الحساب موجود فعلا فستستقبل بريدا إلكترونيًّا لاستعادة كلمة المرور.",
                "info",
            )
            return redirect(url_for("users.login"))
    except Exception as e:
        # raise
        flash(f"يوجد مشكلة فالإتّصال\nحاول مجدّدا في وقت لاحق", 500, "error")

    finally:
        db.session.close()
        return render_template(
            "forms/forgotPassword.html",
            title="Reset Password",
            forgotPasswordForm=forgotPasswordForm,
        )


@usersBp.route("/reset password/<token>", methods=["GET", "POST"])
def resetPassword(token):
    resetPasswordForm = ResetPasswordForm()
    try:
        if current_user.is_authenticated:
            return redirect(url_for("main.home"))

        user = User.verifyResetToken(token)

        if not user:
            flash("الرمز الخاص غير متاح أو منتهي الصلاحية.", "warning")
            return redirect(url_for("users.forgotPassword"))

        if resetPasswordForm.validate_on_submit():
            hashedPassword = bcrypt.generate_password_hash(
                resetPasswordForm.password.data
            ).decode("utf-8")
            user.password = hashedPassword
            db.session.commit()
            flash("تم تحديث كلمة مرورك بنجاح، تستطيع الآن تسجيل الدخول.", "success")
            return redirect(url_for("users.login"))

    except Exception as e:
        db.session.rollback()
        # raise
        flash(f"يوجد مشكلة فالإتّصال\nحاول مجدّدا في وقت لاحق", 500, "error")

    finally:
        db.session.close()
        return render_template(
            "forms/resetPassword.html",
            title="Reset Password",
            resetPasswordForm=resetPasswordForm,
        )


@usersBp.route("/profile")
@login_required
def profile():
    try:
        userData = User.query.filter_by(id=current_user.id).first()
        municipality = Municipality.query.filter_by(id=userData.municipalityId).first()
        dayra = Dayra.query.filter_by(id=municipality.dayraId).first()
        wilaya = Wilaya.query.filter_by(id=dayra.wilayaId).first()
        address = {
            "wilaya": wilaya.name,
            "dayra": dayra.name,
            "municipality": municipality.name,
        }
        image = url_for("static", filename=f"media/{userData.imageFile}")
        gender = current_user.gender
        return render_template(
            "pages/profile.html", userData=userData, address=address, image=image
        )
    except Exception as e:
        # raise
        flash(f"يوجد مشكلة فالإتّصال\nحاول مجدّدا في وقت لاحق", 500, "error")

    finally:
        db.session.close()
        return redirect(url_for("users.login"))


@usersBp.route("/edit profile", methods=["GET", "POST"])
@login_required
def editProfile():
    try:
        user = User.query.filter_by(id=current_user.id).first()
        municipality = Municipality.query.filter_by(id=user.municipalityId).first()
        dayra = Dayra.query.filter_by(id=municipality.dayraId).first()
        wilaya = Wilaya.query.filter_by(id=dayra.wilayaId).first()
        address = {
            "wilaya": wilaya.name,
            "dayra": dayra.name,
            "municipality": municipality.name,
        }
        editProfileForm = EditProfileForm()
        image = url_for("static", filename=f"media/{current_user.imageFile}")

        if editProfileForm.validate_on_submit():
            if editProfileForm.imageFile.data:
                image = renameImage(editProfileForm.imageFile.data)
                user.imageFile = image

            user.firstName = (
                editProfileForm.firstName.data
                if editProfileForm.firstName.data
                else user.firstName
            )
            user.lastName = (
                editProfileForm.lastName.data
                if editProfileForm.lastName.data
                else user.lastName
            )
            user.username = (
                editProfileForm.username.data
                if editProfileForm.username.data
                else user.username
            )
            user.gender = (
                editProfileForm.gender.data
                if editProfileForm.gender.data
                else user.gender
            )
            user.email = (
                editProfileForm.email.data if editProfileForm.email.data else user.email
            )
            user.phoneNumber = (
                editProfileForm.phoneNumber.data
                if editProfileForm.phoneNumber.data
                else user.phoneNumber
            )
            user.municipalityId = (
                editProfileForm.municipality.data
                if editProfileForm.municipality.data
                else user.municipality
            )
            user.houseNumber = editProfileForm.houseNumber.data
            user.location = editProfileForm.location.data
            user.birthDate = (
                editProfileForm.birthDate.data
                if editProfileForm.birthDate.data
                else user.birthDate
            )
            user.birthPlace = editProfileForm.birthPlace.data

            db.session.commit()
            flash(f"تم تعديل الحساب بنجاح.", "success")
            return redirect(url_for("users.profile"))

        elif request.method == "GET":
            editProfileForm.firstName.data = current_user.firstName
            editProfileForm.lastName.data = current_user.lastName
            editProfileForm.username.data = current_user.username
            editProfileForm.gender.data = current_user.gender
            editProfileForm.email.data = current_user.email
            editProfileForm.phoneNumber.data = current_user.phoneNumber
            editProfileForm.houseNumber.data = current_user.houseNumber
            editProfileForm.location.data = current_user.location
            editProfileForm.birthDate.data = current_user.birthDate
            editProfileForm.birthPlace.data = current_user.birthPlace

        else:
            flash(f"تأكّد من صحة الإدخال.", "warning")
    except Exception as e:
        db.session.rollback()
        # raise
        flash(f"يوجد مشكلة فالإتّصال\nحاول مجدّدا في وقت لاحق", 500, "error")

    finally:
        db.session.close()
        return render_template(
            "forms/editProfile.html",
            editProfileForm=editProfileForm,
            userData=user,
            address=address,
            image=image,
        )


@usersBp.route("/change password", methods=["GET", "POST"])
@login_required
def changePassword():
    try:
        changePasswordForm = ChangePasswordForm()
        user = User.query.filter_by(id=current_user.id).first()
        if changePasswordForm.validate_on_submit():
            if user and bcrypt.check_password_hash(
                user.password, changePasswordForm.oldPassword.data
            ):
                hashednewPassword = bcrypt.generate_password_hash(
                    changePasswordForm.newPassword.data
                ).decode("utf-8")
                user.password = hashednewPassword
                db.session.commit()
                flash(
                    "تم تغيير كلمة المرور بنجاح، يمكنك الدخول مجددًّا بكلمة المرور الجديدة.",
                    "success",
                )
                return redirect(url_for("users.logout"))
            else:
                flash("تأكد من صحة كلمة المرور.", "error")
    except Exception as e:
        db.session.rollback()
        # raise
        flash(f"يوجد مشكلة فالإتّصال\nحاول مجدّدا في وقت لاحق", 500, "error")

    finally:
        db.session.close()
        return render_template(
            "forms/changePassword.html",
            title="Change Password",
            changePasswordForm=changePasswordForm,
        )
