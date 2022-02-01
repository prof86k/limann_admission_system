from sqlalchemy.orm import backref
from .. import db
from datetime import datetime
from secrets import token_hex

class Applicant(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    surname = db.Column(db.String(200),)
    first_name = db.Column(db.String(200),)
    last_name = db.Column(db.String(200),)
    gender = db.Column(db.String(200),)
    date_of_birth = db.Column(db.Date(),)
    home_town = db.Column(db.String(200),)
    home_region = db.Column(db.String(200),)
    marital_status = db.Column(db.String(200),)
    childrens = db.Column(db.Integer())
    religion = db.Column(db.String(200),)
    sponsorship = db.Column(db.String(200),)
    passport_picture = db.Column(db.Text())
    employed = db.Column(db.Boolean(),default=False)
    date_applied = db.Column(db.Date(),default =datetime.utcnow() )
    card_id = db.Column(db.Integer(),db.ForeignKey('card.id'))
    contact = db.relationship('Contact',backref='applicant',uselist=False)
    education = db.relationship('Education',backref='applicant',uselist=False)
    admission = db.relationship('Admission',backref='applicant',uselist=False)
    results = db.relationship('Result',backref='applicant',lazy='dynamic',cascade='all,delete,delete-orphan')
    employments = db.relationship('Employment',backref='applicant',lazy='dynamic',cascade='all,delete,delete-orphan')
    referee = db.relationship('Referees',backref='applicant',uselist=False)
    choice = db.relationship('Choice',backref='applicant',uselist=False)
    postgradchoice = db.relationship('Postgradchoice',backref='applicant',uselist=False)
    agreed = db.relationship('Agreement',backref='applicant',uselist=False)
    
    
    def __repr__(self) -> str:
        return f'{self.surname} {self.first_name} {self.last_name}'
    
class Contact(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    country = db.Column(db.String(200))
    contact_number = db.Column(db.String(200))
    contact_number_2 = db.Column(db.String(200))
    email   = db.Column(db.String(200))
    residence_address = db.Column(db.String(200))
    digital_address = db.Column(db.String(200))
    postal_address = db.Column(db.String(200))
    post_town = db.Column(db.String(200))
    post_region = db.Column(db.String(200))
    date_applied = db.Column(db.Date(),default =datetime.utcnow())
    applicant_id = db.Column(db.Integer(),db.ForeignKey('applicant.id'))
    
    def __repr__(self) -> str:
        return f'{self.email}'
    
    
class Education(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    school_name = db.Column(db.String(200))
    location = db.Column(db.String(200))
    date_started = db.Column(db.Date())
    date_completed   = db.Column(db.Date())
    offered_programme = db.Column(db.String(200))
    education_type   = db.Column(db.String(200))
    graduated_class = db.Column(db.String(200))
    graduated_gpa   =  db.Column(db.String(10))
    certificate_file = db.Column(db.String(200))
    transcript_file = db.Column(db.String(200))
    second_graduated_class = db.Column(db.String(200))
    second_graduated_gpa   =  db.Column(db.String(200))
    second_certificate_file = db.Column(db.String(200))
    second_transcript_file = db.Column(db.String(200))
    date_applied = db.Column(db.Date(),default =datetime.utcnow())
    applicant_id = db.Column(db.Integer(),db.ForeignKey('applicant.id'))
    
    def __repr__(self) -> str:
        return f'{self.school_name }'
    
class Result(db.Model):
    id = db.Column(db.Integer(),primary_key=True,unique=True)
    cert_1_number = db.Column(db.String(200))
    results_type = db.Column(db.String(200))
    subject_core_1 = db.Column(db.String(200))
    core_grade_1   = db.Column(db.String(200))
    subject_core_2 = db.Column(db.String(200))
    core_grade_2   = db.Column(db.String(200))
    subject_core_3 = db.Column(db.String(200))
    core_grade_3   = db.Column(db.String(200))
    subject_core_4 =  db.Column(db.String(200))
    core_grade_4   =  db.Column(db.String(200))
    subject_elective_1 = db.Column(db.String(200))
    elective_grade_1   =  db.Column(db.String(200))
    subject_elective_2 = db.Column(db.String(200))
    elective_grade_2   = db.Column(db.String(200))
    subject_elective_3 = db.Column(db.String(200))
    elective_grade_3   = db.Column(db.String(200))
    subject_elective_4 = db.Column(db.String(200))
    elective_grade_4   = db.Column(db.String(200))
    date_applied = db.Column(db.Date(),default =datetime.utcnow())
    applicant_id = db.Column(db.Integer(),db.ForeignKey('applicant.id',ondelete='cascade'))
    
    def __repr__(self) -> str:
        return f'{self.cert_1_number}'
    

    
class Employment(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    organisation_name = db.Column(db.String(200))
    organisation_address = db.Column(db.String(200))
    organisation_contact = db.Column(db.String(200))
    position_held   = db.Column(db.String(200))
    date_started    =   db.Column(db.Date())
    date_ended      =   db.Column(db.Date())
    date_applied = db.Column(db.Date(),default =datetime.utcnow())
    applicant_id = db.Column(db.Integer(),db.ForeignKey('applicant.id',ondelete='cascade'))
    
    def __repr__(self) -> str:
        return f'{self.organisation_name}'
    
    
    def years_of_work_experience(self):
        years_of_experience = self.date_ended.year - self.date_started.year
        return f'{years_of_experience}'    
    
class Referees(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    referees_name = db.Column(db.String(200))
    referees_work_place = db.Column(db.String(200))
    referees_address = db.Column(db.String(200))
    referees_email = db.Column(db.String(200))
    referees_contact = db.Column(db.String(200))
    date_applied = db.Column(db.Date(),default =datetime.utcnow())
    applicant_id = db.Column(db.Integer(),db.ForeignKey('applicant.id'))
    
    def __repr__(self) -> str:
        return self.referees_name
    
    
class Choice(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    first_choice = db.Column(db.String(200))
    second_choice = db.Column(db.String(200))
    third_choice = db.Column(db.String(200))
    date_applied = db.Column(db.Date(),default =datetime.utcnow())
    applicant_id = db.Column(db.Integer(),db.ForeignKey('applicant.id'))
    
    def __repr__(self) -> str:
        return f'{self.first_choice}, {self.second_choice}, {self.third_choice}'

class Postgradchoice(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    first_choice = db.Column(db.String(200))
    second_choice = db.Column(db.String(200))
    third_choice = db.Column(db.String(200))
    date_applied = db.Column(db.Date(),default =datetime.utcnow())
    applicant_id = db.Column(db.Integer(),db.ForeignKey('applicant.id'))
    
    def __repr__(self) -> str:
        return f'{self.first_choice}, {self.second_choice}, {self.third_choice}'
    
class Agreement(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    admission_type = db.Column(db.String(200),default="direct")
    agreed = db.Column(db.Boolean(),default=False)
    applicant_id = db.Column(db.Integer(),db.ForeignKey('applicant.id'))
    
    def __repr__(self) -> str:
        return f'{self.agreed}'
