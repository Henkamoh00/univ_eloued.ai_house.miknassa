import os
from miknassa import db
from run import app

app.app_context()

project_folder = os.path.expanduser("~/Desktop/memoire1/projectDeployment")
migrations_folder = os.path.join(project_folder, "migrations")

exists = os.path.exists(migrations_folder)
success = "False"

try:
    db.reflect()
    db.drop_all()

    if exists:

        os.system(f"rm -rf {migrations_folder}")
        print("************************************************")
        os.system("flask db init")
        print("************************************************")
        os.system("flask db migrate")
        print("************************************************")
        os.system("flask db upgrade")
        print("************************************************")

        os.system("python3 addWilaya.py")
        print("add Wilaya *************************************")
        os.system("python3 addTypes.py")
        print("add Types **************************************")
        success = "Direct True"

    else:

        os.system("flask db init")
        print("************************************************")
        os.system("flask db migrate")
        print("************************************************")
        os.system("flask db upgrade")
        print("************************************************")

        os.system("python3 addWilaya.py")
        print("add Wilaya *************************************")
        os.system("python3 addTypes.py")
        print("add Types **************************************")
        success = "المجلد لم يكن موجود!!!"


except Exception as error:
    success = f"False after throw exception    {error}"

finally:
    print(success)



# حذف مجلد migrations مالمشروع

# تفرغ قاعدة البيانات من جميع الجداول لي فيها
# SET FOREIGN_KEY_CHECKS = 0;
# DROP TABLE IF EXISTS table_name1, table_name2, ...;
# SET FOREIGN_KEY_CHECKS = 1;

# رفع الجداول على قاعدة البيانات من جديد
# flask db init
# flask db migrate
# flask db upgrade

# ملء بعض الجداول الاساسيين
# python3 addWilaya.py
# python3 addTypes.py
# كذلك توجد جداول مثل جدول الشاحنات وغيره يجب ان يحتووا على صف على الاقل