from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, EmailField, DateField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms.validators import Optional, NumberRange
from flask_login import current_user
from miknassa.models import User
from miknassa.users.helper import wilayaList, dayraList, municipalityList

class JoinForm(FlaskForm):
    firstName = StringField("الاسم الأول", validators=[DataRequired(), Length(min=2, max=25)])
    lastName = StringField("اسم العائلة", validators=[DataRequired(), Length(min=2, max=25)])
    username = StringField("اسم المستخدم", validators=[DataRequired(), Length(min=2, max=25)])
    gender = SelectField("الجنس", validators=[DataRequired()], choices=[('male', 'ذكـر'), ('female', 'أنثـى')])
    email = EmailField("البريد الإلكتروني", validators=[DataRequired(), Email()])
    phoneNumber = StringField("رقم الهاتف", validators=[DataRequired()])


    wilaya = SelectField("الولاية", validators=[DataRequired()], choices=wilayaList)
    dayra = SelectField("الدائرة", validators=[DataRequired()], choices=dayraList)
    municipality = SelectField("البلدية", validators=[DataRequired()], choices=municipalityList)


    password = PasswordField("كلمة المرور", 
                            validators=[DataRequired(), 
                            Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_])[A-Za-z\d@$!%*?&_]{8,32}$"),],)
    confirmPassword = PasswordField("تأكيد كلمة المرور", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("انضمام")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("اسم المستخدم هذا موجود بالفعل! اختر واحدًا مختلفًا رجاءًا.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("عنوان البريد الالكتروني هذا موجود بالفعل! اختر واحدًا مختلفًا رجاءًا.")


class LoginForm(FlaskForm):
    email = EmailField("البريد الالكتروني", validators=[DataRequired(), Email()])
    password = PasswordField(
        "كلمة المرور",
        validators=[
            DataRequired(),
        ],
    )
    remember = BooleanField("تذكرني")
    submit = SubmitField("دخـول")

class ForgotPasswordForm(FlaskForm):
    email = EmailField("البريد الإلكتروني", validators=[DataRequired(), Email()])
    submit = SubmitField("استعادة")

class ResetPasswordForm(FlaskForm):
    password = PasswordField("كلمة المرور الجديدة", 
                            validators=[DataRequired(), 
                            Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_])[A-Za-z\d@$!%*?&_]{8,32}$"),],)
    confirmPassword = PasswordField("تأكيد كلمة المرور", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("تحديث")


class ChangePasswordForm(FlaskForm):
    oldPassword = PasswordField("كلمة المرور القديمة", 
                            validators=[DataRequired(), 
                            Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_])[A-Za-z\d@$!%*?&_]{8,32}$"),])
    newPassword = PasswordField("كلمة المرور الجديدة", 
                            validators=[DataRequired(), 
                            Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_])[A-Za-z\d@$!%*?&_]{8,32}$"),])
    confirmNewPassword = PasswordField("تأكيد كلمة المرور الجديدة", validators=[DataRequired(), EqualTo("newPassword")])
    submit = SubmitField("تغيير")


class EditProfileForm(FlaskForm):
    firstName = StringField("الاسم الأول", validators=[DataRequired(), Length(min=2, max=25)])
    lastName = StringField("اسم العائلة", validators=[DataRequired(), Length(min=2, max=25)])
    username = StringField("اسم المستخدم", validators=[DataRequired(), Length(min=2, max=30)])
    gender = SelectField("الجنس", validators=[DataRequired()], choices=[('male', 'ذكـر'), ('female', 'أنثـى')])
    email = EmailField("البريد الإلكتروني", validators=[DataRequired(), Email(), Length(min=6, max=120)])
    phoneNumber = StringField("رقم الهاتف", validators=[DataRequired(), Length(min=8, max=15)])

    wilaya = SelectField("الولاية", validators=[DataRequired()], choices=wilayaList)
    dayra = SelectField("الدائرة", validators=[DataRequired()], choices=dayraList)
    municipality = SelectField("البلدية", validators=[DataRequired()], choices=municipalityList)

    houseNumber = IntegerField("رقم الدار", validators=[Optional(), NumberRange(min=00)])
    location = StringField("العنوان الجغرافي", validators=[Optional(), Length(max=120)])
    birthDate = DateField("تاريخ الميلاد", validators=[Optional()])
    birthPlace = StringField("مكان الميلاد", validators=[Optional(), Length(min=2, max=20)])
    imageFile = FileField("تغيير الصورة", validators=[FileAllowed(['png', 'jpg'])])

    submit = SubmitField("تعديـل")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            if username.data != current_user.username:
                raise ValidationError("اسم المستخدم هذا موجود بالفعل! اختر واحدًا مختلفًا رجاءًا.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            if email.data != current_user.email:
                raise ValidationError("عنوان البريد الالكتروني هذا موجود بالفعل! اختر واحدًا مختلفًا رجاءًا.")
