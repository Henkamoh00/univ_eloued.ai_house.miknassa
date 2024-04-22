# يلزم تكون قاعدة البيانات منشأة
#  استدعاء النماذج من ملف النماذج(مودلز)
from miknassa.models import TruckType, UserType
from miknassa import db
from run import app

with app.app_context():

    # قائمة أنواع حسابات المستخدمين
    userTypesToAdd = [
        UserType(id=1, typeName="regular"),
        UserType(id=2, typeName="admin"),
        UserType(id=3, typeName="driver"),
        UserType(id=4, typeName="noOne"),
    ]

    # قائمة أصناف الشاحنات
    truckTypesToAdd = [
        TruckType(id=1, typeName="truck"),
        TruckType(id=2, typeName="compressor truck"),
        TruckType(id=3, typeName="dump truck"),
    ]

    db.session.add_all(userTypesToAdd)
    db.session.add_all(truckTypesToAdd)

    db.session.commit()
