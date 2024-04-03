# يلزم تكون قاعدة البيانات منشأة
#  استدعاء النماذج من ملف النماذج(مودلز)
from contextvars import copy_context
from miknassa.models import TruckType, UserType
from miknassa import db
from run import app

with app.app_context():

# قائمة أنواع حسابات المستخدمين
    userTypesToAdd = [
        UserType(typeName='regular'),
        UserType(typeName='admin'),
        UserType(typeName='driver'),
        UserType(typeName='noOne')
    ]

    # قائمة أصناف الشاحنات
    truckTypesToAdd = [
        TruckType(typeName='truck'),
        TruckType(typeName='compressor truck'),
        TruckType(typeName='dump truck')
    ]


    db.session.add_all(userTypesToAdd)
    db.session.add_all(truckTypesToAdd)

    db.session.commit()
