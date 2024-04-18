from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
from datetime import datetime, date
from miknassa import db, loginManager
from flask import current_app

@loginManager.user_loader
def load_user(userId):
    return User.query.get(int(userId))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    # __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(25), nullable=False)
    lastName = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(30), nullable=False, unique=True)
    gender = db.Column(db.Enum('male', 'female'), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phoneNumber = db.Column(db.String(15), nullable=False)
    municipalityId = db.Column(db.Integer, db.ForeignKey('municipalities.id'), nullable=False)
    houseNumber = db.Column(db.Integer, nullable=True) 
    location = db.Column(db.String(120), nullable=True) 
    birthDate = db.Column(db.Date, nullable=True, default=date(1990, 1, 1)) 
    birthPlace = db.Column(db.String(20), nullable=True) 
    password = db.Column(db.String(60), nullable=False)
    userTypeId = db.Column(db.Integer, db.ForeignKey('userTypes.id'), nullable=False) 
    imageFile = db.Column(db.String(50), nullable=False, default="default.png") 
    joinDate = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)  

    r_trucksReport = db.relationship('TrucksReport', backref='reporter', lazy=True, cascade="all, delete-orphan")
    r_truck = db.relationship('Truck', backref='driver', lazy=True, cascade="all, delete-orphan")
    r_garbageAlert = db.relationship('GarbageAlert', backref='alerter', lazy=True, cascade="all, delete-orphan")

    def getResetToken(self):
        s = Serializer(current_app.config['SECRET_KEY'], salt='pw-reset')
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verifyResetToken(token, age=3600):
        s = Serializer(current_app.config['SECRET_KEY'], salt='pw-reset')
        try:
            user_id = s.loads(token, max_age=age)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"{{'firstName': {self.firstName}, 'lastName': {self.lastName}, 'username': {self.username}, 'email': {self.email}}}"


class Wilaya(db.Model):
    __tablename__ = 'wilayas'
    # __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    matricule = db.Column(db.Integer, nullable=False)

    r_dayra = db.relationship("Dayra", backref="dayraIn", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"{{'id': {self.id}, 'name': {self.name}, 'matricule': {self.matricule}}}"



class Dayra(db.Model):
    __tablename__ = 'dayras'
    # __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    wilayaId = db.Column(db.Integer, db.ForeignKey('wilayas.id'), nullable=False)

    r_municipality = db.relationship("Municipality", backref="municipalityIn", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"{{'id': {self.id}, 'name': {self.name}, 'wilayaId': {self.wilayaId}}}"

class Municipality(db.Model):
    __tablename__ = 'municipalities'
    # __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    dayraId = db.Column(db.Integer, db.ForeignKey('dayras.id'), nullable=False)

    r_user = db.relationship("User", backref="address", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"{{'id': {self.id}, 'name': {self.name}, 'dayraId': {self.dayraId}}}"


class UserType(db.Model):
    __tablename__ = 'userTypes'
    # __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    typeName = db.Column(db.String(20), nullable=False)

    r_user = db.relationship("User", backref="accountType", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"{{'id': {self.id}, 'typeName': {self.typeName}}}"


class Truck(db.Model):
    __tablename__ = 'trucks'
    
    id = db.Column(db.Integer, primary_key=True)
    matricule = db.Column(db.Integer, unique=True, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    truckTypeId = db.Column(db.Integer, db.ForeignKey('truckTypes.id'), nullable=False)
    
    r_trucksReport = db.relationship('TrucksReport', backref='reportOn', lazy=True, cascade="all, delete-orphan")
    r_operation = db.relationship('Operation', backref='performer', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"{{'id': {self.id}, 'matricule': {self.matricule}, 'userId': {self.userId}, 'truckTypeId': {self.truckTypeId}}}"


class TruckType(db.Model):
    __tablename__ = 'truckTypes'
    
    id = db.Column(db.Integer, primary_key=True)
    typeName = db.Column(db.String(20), nullable=False)

    r_truck = db.relationship('Truck', backref='truckType', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"{{'id': {self.id}, 'typeName': {self.typeName}}}"


class TrucksReport(db.Model):
    __tablename__ = 'trucksReports'
    
    id = db.Column(db.Integer, primary_key=True)
    truckId = db.Column(db.Integer, db.ForeignKey('trucks.id'), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"{{'id': {self.id}, 'truckId': {self.truckId}, 'userId': {self.userId}, 'location': {self.location}, 'date': {self.date}, 'content': {self.content}}}"
    

class GarbageAlert(db.Model):
    __tablename__ = 'garbageAlerts'
    
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    picture = db.Column(db.String(50), nullable=True) 

    r_operation = db.relationship('Operation', backref='taskAlert', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"{{'id': {self.id}, 'userId': {self.userId}, 'location': {self.location}, 'date': {self.date}, 'picture': {self.picture}}}"
    

class Operation(db.Model):
    __tablename__ = 'operations'
    
    id = db.Column(db.Integer, primary_key=True)
    truckId = db.Column(db.Integer, db.ForeignKey('trucks.id'), nullable=False)
    alertId = db.Column(db.Integer, db.ForeignKey('garbageAlerts.id'), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"{{'id': {self.id}, 'truckId': {self.truckId}, 'alertId': {self.alertId}, 'location': {self.location}, 'date': {self.date}}}"
    