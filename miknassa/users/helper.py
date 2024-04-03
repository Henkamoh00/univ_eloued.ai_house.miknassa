from flask_mail import Message
from flask import url_for, render_template
from miknassa import mail
from miknassa.models import Municipality, Dayra, Wilaya


def sendResetEmail(user):
    token = user.getResetToken()
    msg = Message(
        'استعادة كلمة المرور -تطبيق مكنسة-', 
        sender='miknassateam@gmail.com', 
        recipients=[user.email], 
        # body=f'''لاستعادة كلمة المرور، قم بالنّقر على الرابط التالي:
        # {url_for('resetPassword', token=token, _external=True)}
        # إذا لم تقم بهذا الطلب، الرّجاء تجاهل هذا البريد الإلكتروني.''',
        html=render_template('additions/resetMail.html', link=url_for('users.resetPassword', token=token, _external=True))
    )

    mail.send(msg)


# #########////////////////////////////     Query Object To JSON Format     //////////////////////////////////////

# wilayaList = [(0, "الولاية"), (1, "الوادي"), (2, "الجزائر"), (3, "وهران"), (4, "عنابة"), (5, "قسنطينة"), (6, "ورقلة")]
# dayraList = [(0, "الدائرة"), (1, "الوادي"), (2, "المقرن"), (3, "الدبيلة"), (4, "قمار"), (5, "حاسي خليفة"), (6, "الرقيبة")]
# municipalityList = [(0, "البلدية"), (1, "الوادي"), (2, "كوينين"), (3, "البياضة"), (4, "الرباح"), (5, "النخلة"), (6, "العقلة")]
def wilayaList():
    wilayaList = [(obj.id, obj.name) for obj in Wilaya.query.all()]
    return wilayaList

def dayraList():    
    dayraList = [(obj.id, obj.name, {"class": obj.wilayaId}) for obj in Dayra.query.all()]
    return dayraList

def municipalityList():    
    municipalityList = [(obj.id, obj.name, {"class": obj.dayraId}) for obj in Municipality.query.all()]
    return municipalityList

# def wilayaList():
#     wilayas = Wilaya.query.all()
#     wilayaList = []
#     for i in wilayas:
#         wilayaList += [(i.id, i.name)]

#     return wilayaList


# def dayraList():
#     dayras = Dayra.query.all()
#     dayraList = []
#     for i in dayras:
#         dayraList += [(i.id, i.name, {"class": i.wilayaId})]

#     return dayraList


# def municipalityList():
#     municipalities = Municipality.query.all()
#     municipalityList = []
#     for i in municipalities:
#         municipalityList += [(i.id, i.name, {"class": i.dayraId})]

#     return municipalityList
