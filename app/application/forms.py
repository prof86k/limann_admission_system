from flask_wtf import FlaskForm
from wtforms import (SelectField,
                     IntegerField,BooleanField,DateField,
                     FileField, StringField, SubmitField)
from wtforms.validators import DataRequired, InputRequired, Regexp
from flask_wtf.file import FileAllowed
from wtforms_alchemy import QuerySelectField
from ..models import Subject,Programme,Postgradprogramme

class ApplicantForm(FlaskForm):
    GENDER = ((' ','...'),('male','MALE'),('female','FEMALE'),('other','OTHER'))
    MARITAL_STATUS = (('single','SINGLE'),('married','MARRIED'),('divorce','DIVORCE'),('widow','WIDOW'),('other','OTHER'))
    surname = StringField(label='Surname:',validators=[DataRequired(message='Your Surname should be Letters only'),Regexp('^[A-Za-z ]*$')],render_kw={'placeholder':'Enter Your Surname'})
    first_name = StringField(label='First Name:',validators=[DataRequired(message='Your First Name should be Letters only'),Regexp('^[A-Za-z ]*$')],render_kw={'placeholder':'Enter Your First Name'})
    last_name = StringField(label='Last Name:',validators=[DataRequired(message='Your Last Name should be Letters only'),Regexp('^[A-Za-z ]*$')],render_kw={'placeholder':'Enter Your Last Name'})
    gender = SelectField(label='Gender',validators=[DataRequired()],choices=GENDER,)
    date_of_birth = DateField(label='Birth Date:',format='%Y-%m-%d',render_kw={'placeholder':'1990-11-05'})
    home_town = StringField(label='Home Town:',validators=[DataRequired(message='Your Home Town should be Letters only'),Regexp('^[A-Za-z ]*$')],render_kw={'placeholder':'Enter Your Home Town'})
    home_region = StringField(label='Home Region:',validators=[DataRequired(message='Your Home Region should be Letters only'),Regexp('^[A-Za-z ]*$')],render_kw={'placeholder':'Enter Your Home Region'})
    marital_status = SelectField(label='Marital Status:',validators=[DataRequired()],choices=MARITAL_STATUS)
    childrens = IntegerField(label='No. of Children:',default=0,render_kw={'placeholder':'Enter Your No. Children'})
    religion = StringField(label='Religion:',validators=[DataRequired(message='Your Religion should be Letters only'),Regexp('^[A-Za-z ]*$')],render_kw={'placeholder':'Enter Your Religion'})
    sponsorship = StringField(label='Sponsorship:',validators=[DataRequired(message='Your Sponsorship should be Letters only'),Regexp('^[A-Za-z ]*$')],render_kw={'placeholder':'Enter Your Sponsors'})
    passport_picture = FileField(label='Passport Size Picture:',validators=[DataRequired(message='File must be jpg or jpeg or png format'),FileAllowed(['jpg','jpeg','png'])])
    employed = BooleanField(label='Employed:',default=False)
    submit  =  SubmitField('Save')
    
class ContactForm(FlaskForm):
    country = StringField(label='Country:',validators=[DataRequired(),Regexp('^[A-Za-z]*$')])
    contact_number = StringField(label='Phone Number:',validators=[DataRequired(message='Must be phone number type'),Regexp('^[0-9+(-)]')])
    contact_number_2 = StringField(label='Alternative Number:',)
    email   = StringField(label='Email:',validators=[DataRequired()])
    residence_address = StringField(label='Residential Address:',)
    digital_address = StringField(label='Digital Address:',)
    postal_address = StringField(label='Postal Address:',)
    post_town = StringField(label='Post Town:',)
    post_region = StringField(label='Post Region:',)
    submit  =  SubmitField('Save')
    
class EducationForm(FlaskForm):
    LEVEL = ((' ','...'),('highSchool','HIGH SCHOOL',),('diploma','DIPLOMA/HND'),('undergraduate','UNDERGRADUATE'),('postgraduate','POSTGRADUATE'))
    school_name = StringField(label='School Name:',validators=[DataRequired(),Regexp('^[A-Za-z-_. ]*$',flags=0,message='Field Requires only LETTERS and .')])
    location = StringField(label='School Location:',validators=[DataRequired(),Regexp('^[A-Za-z., ]*$',flags=0,message='Field Requires only LETTERS and .,')])
    date_started = DateField(label='Date Started:',validators=[DataRequired()],format='%Y-%m-%d',render_kw={'placeholder':'1990-11-05'})
    date_completed   = DateField(label='Date Ended:',validators=[DataRequired()],format='%Y-%m-%d',render_kw={'placeholder':'1990-11-05'})
    offered_programme = StringField(label='Programme Offered:',validators=[DataRequired(),Regexp('^[A-Za-z. ]*$',flags=0,message='Field Requires only LETTERS and .')])
    education_type   = SelectField(label='Education Level:',validators=[DataRequired()],choices=LEVEL)
    graduated_class = StringField(label='Graduated Class:')
    graduated_gpa   = StringField(label='Graduated GPA:')
    certificate_file = FileField(label='Certificate File:',validators=[FileAllowed(['jpg','jpeg','png'])])
    transcript_file = FileField(label='Transcript File:',validators=[FileAllowed(['jpg','jpeg','png'])])
    second_graduated_class = StringField(label='Other Graduated Class:')
    second_graduated_gpa   = StringField(label='Other Graduated GPA:')
    second_certificate_file = FileField(label='Other Certificate File:',validators=[FileAllowed(['jpg','jpeg','png'])])
    second_transcript_file = FileField(label='Other Transcript File:',validators=[FileAllowed(['jpg','jpeg','png'])])
    submit  =  SubmitField('Save')
    
    # def validete_graduated_gpa(self,graduated_gpa):
        # if graduated_gpa.data == "":
            # pass
    
class ResultForm(FlaskForm):
    # SUBJECT = ((' ','...'),(subjects[0],subjects[0]))
    GRADES = ((' ','...'),('F9','F9'),('E8','E8'),('D7','D7'),('C6','C6'),('C5','C5'),('C4','C4'),('B3','B3'),('B2','B2'),('A1','A1'))
    RESULTS_TYPE = ((' ','...'),('wassce','WASSCE'),('novdec','NOVDEC'),('other','OTHER'))
    # ============================== core ===========================
    cert_1_index_number = StringField(label='Index No. 1:',validators=[DataRequired()],render_kw={'placeholder':'eg. 0054893221'})
    results_type = SelectField(label='Results Type:',choices=RESULTS_TYPE)
    core_subject_1 = QuerySelectField('Core Subject 1:',validators=[InputRequired()],query_factory=lambda: Subject.query.distinct(Subject.subject_name=='CORE'),get_label="subject_name")
    grade_got_subject_1   = SelectField(label='Grade:',choices=GRADES)
    # 
    core_subject_2 = QuerySelectField('Core Subject 2:',query_factory=lambda:Subject.query.distinct(Subject.subject_name),get_label='subject_name')
    grade_got_subject_2   = SelectField(label='Grade:',choices=GRADES)
    # 
    core_subject_3 = QuerySelectField('Core Subject 3:',query_factory=lambda:Subject.query.distinct(),get_label='subject_name')
    grade_got_subject_3   = SelectField(label='Grade:',choices=GRADES)
    # 
    core_subject_4 = QuerySelectField('Core Subject 4:',query_factory=lambda:Subject.query.distinct(),get_label='subject_name')
    grade_got_subject_4   = SelectField(label='Grade:',choices=GRADES)
    # ============================== elective =========================
    elective_subject_1 = QuerySelectField('Elective Subject 1:',query_factory=lambda:Subject.query.distinct(),get_label='subject_name')
    grade_got_ele_subject_1   = SelectField(label='Grade:',choices=GRADES)
# 
    elective_subject_2 = QuerySelectField('Elective Subject 2:',query_factory=lambda:Subject.query.distinct(),get_label='subject_name')
    grade_got_ele_subject_2   = SelectField(label='Grade:',choices=GRADES)
    
    elective_subject_3 = QuerySelectField('Elective Subject 3:',query_factory=lambda:Subject.query.distinct(),get_label='subject_name')
    grade_got_ele_subject_3   = SelectField(label='Grade:',choices=GRADES)
    
    elective_subject_4 = QuerySelectField('Elective Subject 4:',query_factory=lambda:Subject.query.distinct(),get_label='subject_name')
    grade_got_ele_subject_4   = SelectField(label='Grade:',choices=GRADES)
    submit  =  SubmitField('Save and Add New')
    
class EmploymentForm(FlaskForm):
    organisation_name = StringField(label='Organisation Name:',validators=[DataRequired()],render_kw={'placeholder':"Organisation's name"})
    organisation_address = StringField(label='Organisation Address:',validators=[DataRequired()],render_kw={'placeholder':'Address'})
    organisation_contact = StringField(label='Phone Number:',validators=[DataRequired(),Regexp('^[0-9+(-)]')],render_kw={'placeholder':"Phone number eg. 0541423984"})
    position_held   = StringField(label='Position Held:',validators=[DataRequired(),Regexp('^[A-Za-z ]*$')],render_kw={'placeholder':"Position Held"})
    date_started    =   DateField('Date Started:',validators=[DataRequired()],format='%Y-%m-%d',render_kw={'placeholder':'1990-11-05'})
    date_ended      =   DateField('Date Ended:',validators=[DataRequired()],format='%Y-%m-%d',render_kw={'placeholder':'1990-11-05'})
    submit  =  SubmitField('Save')
    
class RefereesForm(FlaskForm):
    referees_name = StringField(label='Referees Name:',validators=[DataRequired(),Regexp('^[A-Za-z ]*$')],render_kw={'placeholder':'Enter Guidian/Referee\'s Name'})
    referees_work_place = StringField(label='Referees Work Place:',validators=[DataRequired()],render_kw={'placeholder':'Enter Guidian/Referee\'s Occupation'})
    referees_address = StringField(label='Referees Address:',validators=[DataRequired()],render_kw={'placeholder':'Enter Guidian/Referee\'s Address'})
    referees_email = StringField(label='Referees Email:',validators=[DataRequired()],render_kw={'placeholder':'Enter Guidian/Referee\'s Email Address'})
    referees_contact = StringField(label='Referees Contact:',validators=[DataRequired(),Regexp('^[0-9+(-)]')],render_kw={'placeholder':'Enter Phone Number eg. 0247843904'})
    submit  =  SubmitField('Save')
    
class ChoiceForm(FlaskForm):
    first_choice = QuerySelectField('First Choice:',validators=[DataRequired() ],query_factory=lambda:Programme.query.all(),get_label='programme_name')
    second_choice = QuerySelectField('Second Choice:',validators=[DataRequired()],query_factory=lambda:Programme.query.all(),get_label='programme_name')
    third_choice = QuerySelectField('Third Choice:',validators=[DataRequired()],query_factory=lambda:Programme.query.all(),get_label='programme_name')
    submit  =  SubmitField('Save')
    
class AgreementForm(FlaskForm):
    ADMISSION_TYPE = (('','...'),('mature_topup','MATURE TOPUP'))
    agreed = BooleanField('Agree',default=False)
    admission_type   = SelectField(label='Application Type:',choices=ADMISSION_TYPE)
    submit = SubmitField('Submit')
    
class PostGradChoiceForm(FlaskForm):
    first_choice = QuerySelectField('First Choice:',validators=[DataRequired() ],query_factory=lambda:Postgradprogramme.query.all(),get_label='programme_title')
    second_choice = QuerySelectField('Second Choice:',validators=[DataRequired()],query_factory=lambda:Postgradprogramme.query.all(),get_label='programme_title')
    third_choice = QuerySelectField('Third Choice:',validators=[DataRequired()],query_factory=lambda:Postgradprogramme.query.all(),get_label='programme_title')
    submit  =  SubmitField('Save')