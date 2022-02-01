from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField,FloatField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, Regexp
from wtforms_alchemy import QuerySelectField
from .models import Cardstate

class BuyCardForm(FlaskForm):
    PAYMENT_MODE     = ((' ','...'),('mobileMoney','Mobile Money'),('cash','CASH'))
    applicants_full_name = StringField(label='Applicant Full Name:',validators=[Regexp('^[A-Za-z ]*$',flags=0,message='Your Name Must Be Letters Only')
                                                                                ,DataRequired()],render_kw={'placeholder':"eg. JOHN DOE"})
    applicants_email    =  StringField(label='Applicant Email:',validators=[DataRequired()],render_kw={'placeholder':"eg. something@gmail.com"})
    applicants_contact  =  StringField(label='Apllicant Contact:',validators=[Regexp('^[0-9+]*$',flags=0,message='Phone must be a + and numbers'),DataRequired()],
                                       render_kw={'placeholder':"eg. +233245873649"})
    application_type    =  QuerySelectField(label='Application Type:',query_factory=lambda:Cardstate.query.all())
    payment_mode        =  StringField(label='Payment Mode:')
    amount              =  FloatField(label='Enter Amount:',render_kw={'placeholder':"eg.180.00",'readonly':True})
    submit              =  SubmitField(label='Create')
    
    
class CardApplyForm(FlaskForm):
    '''the bought card serial number and the pin are use as login details'''
    serial = StringField(label='Serial:',validators=[DataRequired(message='serial number must be entered correctly')],render_kw={'placeholder':"eg. AASCE892BDH"})
    pin     = StringField(label='Pin:',validators=[DataRequired(message='please enter the provided pin.')],render_kw={'placeholder':"eg. 88923B3DIE"})
    submit  = SubmitField('Login')
    
class CardStateForm(FlaskForm):
    '''set card state to paid,free,
    undergraduate,or postgraduate'''
    STATE = (('','...'),('free','FREE'),('paid','PAID'))
    CARD_TYPE=(('','...'),('DIRECT','DIRECT'),('MATURE','MATURE'))
    state = SelectField('Card State:',validate_choice=[DataRequired(message='Field Must Not Be Empty')],choices=STATE)
    card_type = SelectField('Card Type:',validators=[DataRequired()],choices=CARD_TYPE)
    amount = FloatField('Amount:',render_kw={'placeholder':'eg. 180.00'})
    submit = SubmitField('Set')
    
    
class AdminCreationForm(FlaskForm):
    username = StringField(label='Username',validators=[DataRequired()],render_kw={'placeholder':'eg. abc_card/seller'})
    email = StringField(label='Email',validators=[DataRequired()],render_kw={'placeholder':'eg.abc@gmail.com'})
    password = PasswordField(label='Password',validators=[DataRequired()])
    submit = SubmitField('Create')