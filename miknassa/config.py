from dotenv import load_dotenv
import os
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/miknassa' # يستخدم مكتبية مختلفة للاتصال بقاعدة البيانات
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # لحماية الكوكيز
    SESSION_COOKIE_SAMESITE = 'None'
    SESSION_COOKIE_SECURE = True


    # لربط الاتصال بالايميل
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")





