# import sys
# print(sys.path)
# sys.path.remove('/home/henka/Desktop/memoire/miknassaProject/project/miknassa')
# sys.path.append('/home/henka/Desktop/memoire/miknassaProject/project')
# print(sys.path)

# from datetime import date
from miknassa.models import *

# db.drop_all()
db.create_all()


# w = Wilaya(name='eloued', matricule=39)
# t = UserType(typeName='admin')
# d = Dayra(name='eloued', wilayaId=1)
# m = Municipality(name='eloued', dayraId=1)
# # u1 = User(firstName='moh', lastName='mehdi', username='moha', gender='male', email='moh@g.com', phoneNumber='0666555333', municipalityId=1, houseNumber=12, location='d5fd16fx6fxs6x6cdxf56', birthDate=date(1990, 5, 15), password='PacrgbFg14587522cl!@#!', userTypeId=1)
# # u2 = User(firstName='John', lastName='Doe', username='johndoe', gender='male', email='johndoe@example.com', phoneNumber='123456789', municipalityId=1,  houseNumber=123, location='Somewhere', birthDate=date(1990, 5, 15),  password='hashed_password',  userTypeId=1)
# db.session.add(t)
# db.session.add(w)
# db.session.add(d)
# db.session.add(m)
# # db.session.add(u1)
# # db.session.add(u2)
# db.session.commit()




# User.query.all()
# User.query.first()
# User.query.filter_by(id=1).all()
# User.query.get(1)



# لاضافة مسار الحزمة الى متغيرات البيئة باستخدام ملف باش
# nano ~/.bashrc
# source ~/.bashrc
# export PYTHONPATH="/home/henka/Desktop/memoire/miknassaProject/project:${PYTHONPATH}"

# لاضافة مسار الحزمة الى متغيرات البيئة باستخدام باثون
# import sys
# sys.path.append('/home/henka/Desktop/memoire/miknassaProject/project')
# print(sys.path)