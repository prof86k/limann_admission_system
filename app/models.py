from sqlalchemy.orm import backref
from . import db 
from datetime import datetime
from secrets import token_hex

'''models of the admin activities'''
    
class Faculty(db.Model):
    '''create new faculty or school to host department'''
    id = db.Column(db.Integer(),primary_key=True)
    faculty_name = db.Column(db.String(200),nullable=False)
    faculty_code = db.Column(db.String(200),nullable=False)
    departments = db.relationship('Department',backref='faculty',lazy='dynamic',cascade='all,delete,delete-orphan')
    date_created = db.Column(db.DateTime(),default=datetime.utcnow())
    
    def __repr__(self) -> str:
        return f'{self.faculty_name}'

class Department(db.Model):
    '''stores the departments that are in the school'''
    id = db.Column(db.Integer(),primary_key=True)
    department_name = db.Column(db.String(200),nullable=False)
    types = db.relationship('Type',backref='department',lazy='dynamic',cascade='all,delete,delete-orphan')
    date_created = db.Column(db.DateTime(),default=datetime.utcnow())
    faculty_id = db.Column(db.Integer(),db.ForeignKey('faculty.id',ondelete='cascade'))

    def __repr__(self) -> str:
        return f'{self.department_name}'
    
class Type(db.Model):
    '''return the application type(degree,diploma,HND,masters,phd,'''
    id = db.Column(db.Integer(),primary_key=True)
    appliction_type = db.Column(db.String(200),default='Diploma')
    is_avaliable = db.Column(db.Boolean(),default=False)
    department_id = db.Column(db.Integer(),db.ForeignKey('department.id',ondelete='cascade'))
    programmes    = db.relationship('Programme',backref='type',lazy='dynamic',cascade='all,delete,delete-orphan')
    postgrad_programmes    = db.relationship('Postgradprogramme',backref='type',lazy='dynamic',cascade='all,delete,delete-orphan')
    admissions    = db.relationship('Admission',backref='type',lazy='dynamic',cascade='all,delete,delete-orphan')
    date_created = db.Column(db.DateTime(),default=datetime.utcnow())
    
    
    def __repr__(self) -> str:
        return self.appliction_type

courses = db.Table('courses',
    db.Column('programme_id',db.Integer,db.ForeignKey('programme.id')),
    db.Column('subject_id',db.Integer,db.ForeignKey('subject.id'))
)
    
class Programme(db.Model):
    '''return the programmes under a particular application type'''
    id = db.Column(db.Integer(),primary_key=True)
    programme_name = db.Column(db.String(200),nullable=False)
    programme_duration_direct = db.Column(db.String(200))
    programme_duration_topup = db.Column(db.String(200))
    cut_off_point = db.Column(db.Integer(),nullable=True)
    min_class = db.Column(db.String(200))
    is_avaliable = db.Column(db.Boolean(),default=False)
    programme_admission_fees = db.Column(db.Integer(),nullable=False)
    type_id = db.Column(db.Integer(),db.ForeignKey('type.id',ondelete='cascade'))
    date_created = db.Column(db.DateTime(),default=datetime.utcnow())
    # subjects_for_admission = db.relationship('Subject',backref='programme',lazy='dynamic',cascade='all,delete,delete-orphan')
    subjects = db.relationship('Subject',secondary=courses,backref=db.backref('course',lazy='dynamic'),cascade='all,delete')
    
    def __repr__(self) -> str:
        return self.programme_name
    
    
class Subject(db.Model):
    '''admin add the subjects pertaining their programmes offereds
    these subjects grade points are use to commpare with the cutoff point 
    to shortlist applicants to a programme for addmission
    
    the admin provides the only to be used in applicant page for corresponding
    grades'''
    id = db.Column(db.Integer(),primary_key=True)
    subject_name = db.Column(db.String(200),nullable=False)
    subject_status = db.Column(db.String(200),default='core')
    min_grade = db.Column(db.String(200),nullable=False)
    date_created = db.Column(db.DateTime(),default=datetime.utcnow())
    # programme_id = db.Column(db.Integer(),db.ForeignKey('programme.id',ondelete='cascade'))

    def __repr__(self) -> str:
        return f'{self.subject_name}'
    
class Postgradprogramme(db.Model):
    '''post graduate progammmes'''
    id = db.Column(db.Integer(),primary_key=True)
    programme_title = db.Column(db.String(200),nullable=False)
    programme_duration = db.Column(db.String(200))
    min_gpa = db.Column(db.String(200),nullable=True)
    active = db.Column(db.Boolean(),default=False)
    programme_admission_fees = db.Column(db.Integer(),nullable=False)
    type_id = db.Column(db.Integer(),db.ForeignKey('type.id',ondelete='cascade'))
    date_created = db.Column(db.DateTime(),default=datetime.utcnow())
    
    def __repr__(self) -> str:
        return self.programme_title
    
class Admission(db.Model):
    '''shortlisted people
    javascript will help in saving the GENERATED people into the database.
    options=(('shortlisted','SHORTLISTED'),('admit','ADMIT'),('pending','PENDING'),('approval','APPROVAL'))
    '''
    id = db.Column(db.Integer(),primary_key=True)
    student_id = db.Column(db.String(200))
    person_full_name = db.Column(db.String(200),nullable=False)
    programme_listed = db.Column(db.String(200),nullable=False)
    admission_status = db.Column(db.String(200))
    level_id = db.Column(db.Integer(),db.ForeignKey('type.id',ondelete='cascade'))
    applicant_id = db.Column(db.Integer(),db.ForeignKey('applicant.id',ondelete='cascade'))
    date_created = db.Column(db.DateTime(),default=datetime.utcnow())
    
    def __repr__(self) -> str:
        return f'{self.student_id}'
    
class Srcdues(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    amount = db.Column(db.Float(),default=0.0)
    date_added = db.Column(db.DateTime(),default=datetime.utcnow())

    def __repr__(self) -> str:
        return f'{self.amount}'
    
class Coreforgrades(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    subject_name = db.Column(db.String(200))
    subject_status = db.Column(db.String(200))
    min_grade = db.Column(db.String(200))
    date_created = db.Column(db.DateTime(),default=datetime.utcnow())
    
    def __repr__(self) -> str:
        return f'{self.subject_name}'
    
class Lengthofgradingsubjects(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    number = db.Column(db.Integer(),default=6)
    date_added = db.Column(db.DateTime(),default=datetime.utcnow())

    def __repr__(self) -> str:
        return f'{self.number}'
