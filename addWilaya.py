# يلزم تكون قاعدة البيانات منشأة
#  استدعاء النماذج من ملف النماذج(مودلز)
from miknassa.models import Wilaya, Dayra, Municipality
from miknassa import db
from run import app

app.app_context().push()


# كائنات الولايات
wilayasToAdd = [Wilaya(id=1, name="الوادي", matricule=39)]

# كائنات الدوائر
dayrasToAdd = [
    Dayra(id=1, name="الوادي", wilayaId=1),
    Dayra(id=2, name="البياضة", wilayaId=1),
    Dayra(id=3, name="الرباح", wilayaId=1),
    Dayra(id=4, name="اميه ونسة", wilayaId=1),
    Dayra(id=5, name="قمار", wilayaId=1),
    Dayra(id=6, name="الرقيبة", wilayaId=1),
    Dayra(id=7, name="المقرن", wilayaId=1),
    Dayra(id=8, name="الدبيلة", wilayaId=1),
    Dayra(id=9, name="حاسي خليفة", wilayaId=1),
    Dayra(id=10, name="الطالب العربي", wilayaId=1),
]

# كائنات البلديات
municipalitiesToAdd = [
    Municipality(id=1, name="الوادي", dayraId=1),
    Municipality(id=2, name="كوينين", dayraId=1),
    Municipality(id=3, name="البياضة", dayraId=2),
    Municipality(id=4, name="الرباح", dayraId=3),
    Municipality(id=5, name="النخلة", dayraId=3),
    Municipality(id=6, name="العقلة", dayraId=3),
    Municipality(id=7, name="اميه ونسة", dayraId=4),
    Municipality(id=8, name="واد العلندة", dayraId=4),
    Municipality(id=9, name="قمار", dayraId=5),
    Municipality(id=10, name="تغزوت", dayraId=5),
    Municipality(id=11, name="ورماس", dayraId=5),
    Municipality(id=12, name="الرقيبة", dayraId=6),
    Municipality(id=13, name="الحمراية", dayraId=6),
    Municipality(id=14, name="المقرن", dayraId=7),
    Municipality(id=15, name="سيدي عون", dayraId=7),
    Municipality(id=16, name="الدبيلة", dayraId=8),
    Municipality(id=17, name="حساني عبد الكريم", dayraId=8),
    Municipality(id=18, name="حاسي خليفة", dayraId=9),
    Municipality(id=19, name="الطريفاوي", dayraId=9),
    Municipality(id=20, name="الطالب العربي", dayraId=10),
    Municipality(id=21, name="دوار الماء", dayraId=10),
    Municipality(id=22, name="بن قشة", dayraId=10),
]


db.session.add_all(wilayasToAdd)
db.session.add_all(dayrasToAdd)
db.session.add_all(municipalitiesToAdd)

db.session.commit()
