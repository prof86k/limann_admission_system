from flask_wtf import FlaskForm
from wtforms import (SelectField,FloatField,BooleanField, PasswordField,
                     StringField, SubmitField)
from wtforms.fields.core import IntegerField
from wtforms.fields.simple import FileField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired, InputRequired, Regexp
from wtforms_alchemy import QuerySelectField
from ..models import Subject

class AdminLoginForm(FlaskForm):
    username = StringField(label='Username:',validators=[InputRequired()])
    password = PasswordField(label='Password:',validators=[InputRequired(message='You Must Enter A Valid Password')])
    submit   = SubmitField('Login')
    
class FacultyForm(FlaskForm):
    faculty_name = StringField('School/Faculty Name:',validators=[InputRequired(),Regexp('^[A-Za-z][A-Za-z0-9/ ]*$',flags=0,message='Field requires letters and or integers')])
    faculty_code =StringField(label='School/Faculty Code:',validators=[InputRequired(),Regexp('^[A-Za-z][A-Za-z0-9/ ]*$',flags=0,message='Field requires letters integers and only / eg fms/0090/23')])
    submit = SubmitField('Create')
    
class CreateDepartment(FlaskForm):
    department_name = StringField(label='Department:',validators=[InputRequired(),Regexp('^[A-Za-z. ]*$',flags=0,message='Field requires letters and only . eg DEPART. COMPUTER SCIENCE')])
    submit = SubmitField('Add')
    
class CreateLevelTypeForm(FlaskForm):
    appliction_type = StringField(label='Run Level:',validators=[InputRequired()])
    is_avaliable = BooleanField(label='Active:',default=False)
    submit = SubmitField('Add')
    
    
class AddProgrammeRunForm(FlaskForm):
    programme_name = StringField(label='Programme Name:',validators=[InputRequired()],render_kw={'placeholder':'eg. BSC. COMPUTER SCIENCE'})
    programme_duration_direct = StringField(label='Programme Duration Direct:',validators=[InputRequired()],render_kw={'placeholder':'eg. 4-years'})
    programme_duration_topup = StringField(label='Programme Duration Topup:',validators=[InputRequired()],render_kw={'placeholder':'eg. 2-years'})

    cut_off_point = IntegerField(label='Cut Off Point:',validators=[DataRequired()],render_kw={'placeholder':'eg.SHS or Any 20'})
    min_class = StringField(label='Min Class',validators=[DataRequired()],render_kw={'placeholder':'eg. FIRST CLASS'})
    is_avaliable = BooleanField(label='Active:',default=False)
    programme_admission_fees = FloatField(label='Admission Fees:',validators=[DataRequired()],render_kw={'placeholder':'eg. 180.00'})
    submit         = SubmitField('Add')
    
class AddPostGradProgrammeForm(FlaskForm):
    programme_title = StringField(label='Programme Name:',validators=[InputRequired()],render_kw={'placeholder':'eg. BSC. COMPUTER SCIENCE'})
    programme_duration = StringField(label='Programme Duration:',validators=[InputRequired()],render_kw={'placeholder':'eg. 4-years'})
    min_gpa = FloatField(label='Min GPA:',validators=[DataRequired()],render_kw={'placeholder':'eg. degree or any 4.5 / SHS or Any 20'})
    active = BooleanField(label='Active:',default=False)
    programme_admission_fees = FloatField(label='Admission Fees:',validators=[DataRequired()],render_kw={'placeholder':'eg. 180.00'})
    submit         = SubmitField('Add')
    
class RequireAddmissonSubjectForm(FlaskForm):
    SUBJECT_STATUS = (('core','CORE'),('elective','ELECTIVE'))
    subject_name = StringField(label='Programme Name:',validators=[InputRequired(),Regexp('^[A-Za-z. ]*$',flags=0,message='Field requires letters and only . eg INTER. SCIENCE or BSC. COMPUTER SCIENCE ')])
    subject_status = SelectField(label='Subject Status:',choices=SUBJECT_STATUS)
    min_grade = StringField(label='Minimum Grade/GPA',validators=[DataRequired(),Regexp('^[A-Za-z0-9.]*$',flags=0,message='Letters Float Numbers')])
    submit = SubmitField('Add') 

class LoadRequireSubjectsForm(FlaskForm):
    subject_name = QuerySelectField('Subject Title:',query_factory=lambda:Subject.query.distinct(Subject.subject_name))
    submit = SubmitField('add')
    
    
class Subjects4GradesForm(FlaskForm):
    subject_name = QuerySelectField('Subject Title:',query_factory=lambda:Subject.query.distinct(Subject.subject_name),allow_blank=True)
    subject_status = StringField(label='Subject Status:')
    min_grade = StringField(label='Minimum Grade/GPA',validators=[DataRequired(),Regexp('^[A-Za-z0-9.]*$',flags=0,message='Letters Float Numbers')])
    submit = SubmitField('add')

class SrcForm(FlaskForm):
    amount = FloatField(label='Due Amount:',render_kw={'placeholder':'Eg. 180.00'})
    submit = SubmitField('add')
    
class SubjectsLengthForm(FlaskForm):
    number = IntegerField(label='Number:',render_kw={'placeholder':' positive integers Eg. 6'})
    submit = SubmitField('add')
    
class RegistrarForm(FlaskForm):
    registrar_name = StringField(label='Registrar Name:',validators=[DataRequired()],render_kw={'placeholder':'eg. Some Name'})
    registrar_signature = FileField(label='Signature',validators=[DataRequired(),FileAllowed(['png','jpeg','jpg'])],render_kw={'placeholder':'eg. Registrar signature pic'})
    submit = SubmitField(label='Add')

class BankForm(FlaskForm):
    bank_name = StringField('Bank Name:',validators=[DataRequired()],render_kw={'placeholder':'eg. GCB'})
    transaction_mode = StringField('Transaction Mode:',validators=[DataRequired()],render_kw={'placeholder':'transflow'})
    submit = SubmitField('add')