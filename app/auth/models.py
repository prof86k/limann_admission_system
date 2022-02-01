from datetime import datetime

from .. import db
from secrets import token_hex

from flask_login import AnonymousUserMixin
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .. import db


class Registrar(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    registrar_name = db.Column(db.String(200))
    registrar_signature = db.Column(db.Text())

    def __repr__(self) -> str:
        return f'{self.registrar_name}'


class PageAnonymousUserMixin(AnonymousUserMixin):
    def __init__(self) -> None:
        super().__init__()
        self.username = 'Guest'


roles = db.Table('role_users',
                 db.Column('admin_id', db.Integer(), db.ForeignKey('admin.id')),
                 db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
                 )


class Admin(UserMixin, db.Model):
    '''class for admin information
        md.Admin(username='admin086',email='kkumasampson@gmail.com',password='86byadmin')
    '''

    id = db.Column(db.Integer(),primary_key=True)
    email = db.Column(db.String(100))
    username = db.Column(db.String(50),index=True)
    password = db.Column(db.String(50),index=True)
    last_login = db.Column(db.Date(),default =datetime.utcnow())
    roles = db.relationship('Role',secondary=roles,backref=db.backref('admin',lazy='dynamic'))
    sales = db.relationship('Buy',backref='admin',lazy='dynamic',cascade='all,delete,delete-orphan')
    # def __init__(self,username='') -> None:
    #     default = Role.query.filter_by(name='card_seller').first()
    #     self.roles.append(default='card_seller')
    #     self.username = username

    def has_role(self, name):
        '''check whether a user has role'''
        for role in self.roles:
            if role.name == name:
                return True
        return False

    def set_password_to_hash(self, password):
        '''set the entered password to has admin086 086byadmin'''
        self.password = generate_password_hash(password)

    def check_hashed_password(self, password):
        '''check the password hashed entered return true if password is corrrect'''
        return check_password_hash(self.password, password)

    # def get_id(self):
    # return int(self.id)

    @property
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False


class Role(db.Model):
    '''add roles of every user of the system'''
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200))

    def __init__(self, name) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f'{self.name} Role'


class Cardstate(db.Model):
    '''admin set the state of the card to either FREE OR PAID
    set the price for a card if it is undergraduate or postgraduate'''
    id = db.Column(db.Integer(), primary_key=True)
    state = db.Column(db.String(200))  # free or paid by selection
    card_type = db.Column(db.String(200))  # undergraduate or postgraduate by selection
    amount = db.Column(db.Float(), default=0.0)
    date_created = db.Column(db.Date(), default=datetime.utcnow())

    def __repr__(self) -> str:
        return f'{self.card_type}'


class Buy(db.Model):
    '''the applicant buys makes their payments here
    after the applicant pays a serial and pin is generated and store in the
    Card for login into the application for application
    '''
    id = db.Column(db.Integer(), primary_key=True)
    applicants_full_name = db.Column(db.String(200))
    applicants_email = db.Column(db.String(200))
    applicants_contact = db.Column(db.String(200))
    application_type = db.Column(db.String(200))
    payment_mode = db.Column(db.String(200))
    transaction_id = db.Column(db.String(200), default=(lambda x: x)(token_hex(13)))
    amount = db.Column(db.Float(), default=0.0)
    admin_id = db.Column(db.Integer(), db.ForeignKey('admin.id', ondelete='cascade'))
    cards = db.relationship('Card', backref='buy', lazy='dynamic', cascade='all,delete,delete-orphan')
    date_bought = db.Column(db.Date(), default=datetime.utcnow())

    def __repr__(self) -> str:
        return self.applicants_full_name

    def generate_serial_pin(self):
        date_bought = datetime.date(datetime.utcnow())
        if self.application_type.lower() != '':
            return {
                'serial number': str(date_bought.year) + self.application_type + str(token_hex(3)).upper(),
                'pin': token_hex(5).upper(),
            }


class Card(db.Model):
    '''after the aplicant pays then generated serial and pin
    is use as login for the application'''
    id = db.Column(db.Integer(), primary_key=True)
    serial_number = db.Column(db.String(200))
    pin = db.Column(db.String(200))
    buy_id = db.Column(db.Integer(), db.ForeignKey('buy.id', ondelete='cascade'))
    date_bought = db.Column(db.Date(), default=datetime.utcnow())
    applicant = db.relationship('Applicant', backref='card', uselist=False)

    def __repr__(self) -> str:
        return self.serial_number

    def is_active(self):
        '''only cards bought this year are valid for login
        else prompt for card expired'''
        return datetime.date(datetime.utcnow()).year - 1 < self.date_bought.year < datetime.date(
            datetime.utcnow()).year + 1


class Bank(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    bank_name = db.Column(db.String(100))
    transaction_mode = db.Column(db.String(100))
    date_created = db.Column(db.DateTime(), default=datetime.utcnow())

    def __repr__(self) -> str:
        return f'{self.bank_name}'
