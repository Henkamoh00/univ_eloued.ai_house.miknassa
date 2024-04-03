# يلزم تكون قاعدة البيانات منشأة
#  استدعاء النماذج من ملف النماذج(مودلز)
from miknassa.models import Wilaya, Dayra, Municipality
from miknassa import db
from run import app

app.app_context().push()


# كائنات الولايات
wilayasToAdd = [
    Wilaya(name='الوادي', matricule=39)
]

# كائنات الدوائر
dayrasToAdd = [
    Dayra(name='الوادي', wilayaId=1),
    Dayra(name='البياضة', wilayaId=1),
    Dayra(name='الرباح', wilayaId=1),
    Dayra(name='اميه ونسة', wilayaId=1),
    Dayra(name='قمار', wilayaId=1),
    Dayra(name='الرقيبة', wilayaId=1),
    Dayra(name='المقرن', wilayaId=1),
    Dayra(name='الدبيلة', wilayaId=1),
    Dayra(name='حاسي خليفة', wilayaId=1),
    Dayra(name='الطالب العربي', wilayaId=1)
]

# كائنات البلديات
municipalitiesToAdd = [
    Municipality(name='الوادي', dayraId=1),
    Municipality(name='كوينين', dayraId=1),
    Municipality(name='البياضة', dayraId=2),
    Municipality(name='الرباح', dayraId=3),
    Municipality(name='النخلة', dayraId=3),
    Municipality(name='العقلة', dayraId=3),
    Municipality(name='اميه ونسة', dayraId=4),
    Municipality(name='واد العلندة', dayraId=4),
    Municipality(name='قمار', dayraId=5),
    Municipality(name='تغزوت', dayraId=5),
    Municipality(name='ورماس', dayraId=5),
    Municipality(name='الرقيبة', dayraId=6),
    Municipality(name='الحمراية', dayraId=6),
    Municipality(name='المقرن', dayraId=7),
    Municipality(name='سيدي عون', dayraId=7),
    Municipality(name='الدبيلة', dayraId=8),
    Municipality(name='حساني عبد الكريم', dayraId=8),
    Municipality(name='حاسي خليفة', dayraId=9),
    Municipality(name='الطريفاوي', dayraId=9),
    Municipality(name='الطالب العربي', dayraId=10),
    Municipality(name='دوار الماء', dayraId=10),
    Municipality(name='بن قشة', dayraId=10)
]


db.session.add_all(wilayasToAdd)
db.session.add_all(dayrasToAdd)
db.session.add_all(municipalitiesToAdd)

db.session.commit()
