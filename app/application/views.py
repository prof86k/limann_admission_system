from unicodedata import category
from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.utils import redirect
from flask import request,flash,current_app
import os
import secrets
from PIL import Image
from . import application
from . import models as mdl
from . import logics as lgs
from . import forms as fms
from ..auth import models as authmdl
from .. import models as apmdl
from app import db

# ================================================= applicants dashboard =====================
@application.route('/application-dashboard/<card_id>')
def dashboard(card_id):
    '''The application dashboard for listing all the required options for the application
    if user is None redirect to self(dashboard)
    else redirect to url_for('application.check_admission_status')
    njoona@gmail.com
    kuma@2021
    '''    

    card = authmdl.Card.query.filter_by(pin=card_id).first()
    if card.applicant is not None:
        return render_template('application/application_dashboard.html',applicant=card.applicant)
    return render_template('errors/404.html')

# =========================================== applicants personal information ==============
def save_passport(form_passport_pic):
    random_image_name = secrets.token_hex(8)
    _, file_ext =os.path.splitext(form_passport_pic.filename)
    passport_picname = random_image_name+file_ext
    image_pic = os.path.join(current_app.root_path,'static/images/applicant_passport',passport_picname)
    # resize image
    output_size = (125,125)
    image_size = Image.open(form_passport_pic)
    image_size.thumbnail(output_size)
    image_size.save(image_pic)
    # return created file 
    return passport_picname
    
    
@application.route('/applicant/personal-info/<card_id>',methods=['GET','POST'])
def applicant_personal_info(card_id):
    '''collect The applicants personal information'''
    card = authmdl.Card.query.filter_by(pin=card_id).first()
    if card is not None:
        # ====================================== validate ===================
        # if the applicant login successfully, check the applicant info
        # to see if there is no data inside 
        # if there's data redirect to the next view to all check
        if not card.applicant:
            form = fms.ApplicantForm()
            if form.validate_on_submit():
                if form.passport_picture.data:
                    image_file = save_passport(form.passport_picture.data)
                lgs.process_personal_info_data(form,card_id=card.id,image_file=image_file)
                # process the form in logic
                # return a redirect and message
                return redirect(url_for('application.applicant_contact_info',card_id=card.pin))
            return render_template('application/application_info.html',form=form,card=card)
        else: 
            return redirect(url_for('application.dashboard',card_id=card.pin))    
    return render_template('errors/404.html')

@application.route('/applicant/contact-info/<card_id>',methods=['GET','POST'])
def applicant_contact_info(card_id):
    '''Process the applicant contact info'''
    card = authmdl.Card.query.filter_by(pin=card_id).first()
    if card.applicant is not None:
        if not card.applicant.contact:
            form = fms.ContactForm()
            if form.validate_on_submit():
                lgs.process_contact_info(form,applicant_id=card.applicant.id)
                return redirect(url_for('application.applicant_eductaion_info',card_id=card.pin))
            return render_template('application/applicant_contact.html',form=form) 
        else:
            return redirect(url_for('application.dashboard',card_id=card.pin))
    return render_template('errors/404.html')

@application.route('/applicant/education-details/<card_id>',methods=['GET','POST'])
def applicant_eductaion_info(card_id):
    '''process the applicant eductaion info if there is data already'''
    card = authmdl.Card.query.filter_by(pin=card_id).first()
    try:
        applicant = card.applicant
        if not applicant.education:
            form = fms.EducationForm() 
            if form.validate_on_submit():
                education_type = form.education_type.data
                if applicant.card.buy.application_type=='MATURE' and education_type =='highSchool':
                    flash('High School students can not apply as mature\n This CARD was Bought for {0} application\n Please sellect your current level of education.'.format(applicant.card.buy.application_type),category='warning')
                    return redirect(request.url)
                cert_file = None
                tran_file = None
                second_cert_file = None
                second_trans_file = None
                if form.certificate_file.data and form.transcript_file.data:
                    cert_file = save_passport(form.certificate_file.data)
                    tran_file = save_passport(form.transcript_file.data)
                if form.second_certificate_file.data and form.second_transcript_file.data:
                    second_cert_file = save_passport(form.second_transcript_file.data)
                    second_trans_file = save_passport(form.second_transcript_file.data)
                lgs.process_education_info(form,applicant=applicant,
                                           cert_file=cert_file,tran_file=tran_file
                                           ,second_cert_file=second_cert_file,
                                           second_tran_file=second_trans_file)
                return redirect(url_for('application.applicant_results_info',card_id=card.pin))
            return render_template('application/applicant_education.html',form=form) 
        else:
            return redirect(url_for('application.dashboard',card_id=card.pin))
    except Exception as e:
        return render_template('errors/404.html')

@application.route('/applicant/results-info/<card_id>',methods=['GET','POST'])
def applicant_results_info(card_id):
    '''process the applicant results info'''
    card = authmdl.Card.query.filter_by(pin=card_id).first()
    try:
        applicant = card.applicant
        try:
            if applicant.education.education_type == 'highSchool':
                form = fms.ResultForm() 
                if form.validate_on_submit():
                    lgs.process_results_info(form,applicant_id=applicant.id)
                    return redirect(request.url)
                return render_template('application/applicant_results.html',form=form,card_id=card.pin,applicant=applicant) 
            else:
                return redirect(url_for('application.applicant_employment_info',card_id=card.pin))
        except AttributeError:
            return redirect(url_for('application.applicant_eductaion_info',card_id=card.pin))
    except Exception as e:
        print(e)
    return render_template('errors/404.html')

@application.route('/applicant/new/results-info/<card_id>',methods=['GET','POST'])
def applicant_new_results_info(card_id):
    '''process the applicant results info'''
    card = authmdl.Card.query.filter_by(pin=card_id).first()
    try:
        applicant = card.applicant
        try:
            if applicant.education.education_type == 'highSchool':
                form = fms.ResultForm() 
                if form.validate_on_submit():
                    lgs.process_results_info(form,applicant_id=applicant.id)
                    return redirect(url_for('application.dashboard',card_id=card.pin))
                return render_template('application/add_new_result.html',form=form,card_id=card.pin,applicant=applicant) 
            else:
                return redirect(url_for('application.dashboard',card_id=card.pin))
        except AttributeError:
            return redirect(url_for('application.applicant_eductaion_info',card_id=card.pin))
    except Exception as e:
        print(e)
    return render_template('errors/404.html')
     
@application.route('/applicant/employment-info/<card_id>',methods=['GET','POST'])
def applicant_employment_info(card_id):
    '''process the applicant employment information'''
    card = authmdl.Card.query.filter_by(pin=card_id).first()
    try:
        applicant = card.applicant
        if applicant.employed:
            form = fms.EmploymentForm() 
            if form.validate_on_submit():
                lgs.process_employment_info(form,applicant_id=applicant.id)
                return redirect(url_for('application.applicant_refeeres_info',card_id=card.pin))
            return render_template('application/applicant_employment.html',form=form)
        return redirect(url_for('application.applicant_refeeres_info',card_id=card.pin))    
    except Exception as e:
        return render_template('errors/404.html')

@application.route('/applicant/refeeres-info/<card_id>',methods=['GET','POST'])
def applicant_refeeres_info(card_id):
    '''process the applicant refeeres information'''
    card = authmdl.Card.query.filter_by(pin=card_id).first()
    try:
        applicant = card.applicant
        if not applicant.referee:
            form = fms.RefereesForm() 
            if form.validate_on_submit():
                lgs.proccess_refeeres_guardian_info(form,applicant_id=applicant.id)
                if applicant.education.education_type == 'highSchool' or applicant.education.education_type=='diploma':
                    return redirect(url_for('application.applicant_choices_info',card_id=card.pin))
                else:
                    return redirect(url_for('application.applicant_postgrad_choices_info',card_id=card.pin))
            return render_template('application/applicant_refeere_info.html',form=form) 
        else:
            return redirect(url_for('application.dashboard',card_id=card.pin))
    except Exception as e:
        return render_template('errors/404.html')

@application.route('/applicant/choices-info/<card_id>',methods=['GET','POST'])
def applicant_choices_info(card_id):
    '''process the applicant programme choices information'''
    card = authmdl.Card.query.filter_by(pin=card_id).first()
    try:
        applicant = card.applicant
        if not applicant.choice:
            if applicant.card.buy.application_type!='PDG':
                form = fms.ChoiceForm() 
                if form.validate_on_submit():
                    lgs.process_choices_info(form,applicant_id=applicant.id)
                    return redirect(url_for('application.submit_application_confirmation',card_id=card.pin))
                return render_template('application/applicant_program_choices.html',form=form)
            else:
                return redirect(url_for('application.applicant_postgrad_choices_info',card_id=card.pin))
        else:
            return redirect(url_for('application.dashboard',card_id=card.pin))
    except Exception as e:
        return render_template('errors/404.html')

@application.route('/applicant/postgrad/choices-info/<card_id>',methods=['GET','POST'])
def applicant_postgrad_choices_info(card_id):
    '''process the applicant programme choices information'''
    card = authmdl.Card.query.filter_by(pin=card_id).first()
    try:
        applicant = card.applicant
        form = fms.PostGradChoiceForm() 
        if form.validate_on_submit():
            lgs.process_postgrad_choices_info(form,applicant_id=applicant.id)
            return redirect(url_for('application.submit_application_confirmation',card_id=card.pin))
        return render_template('application/postgrad_choice.html',form=form)
    except Exception as e:
        return render_template('errors/404.html')

@application.route('/confirm/submit-application/<card_id>',methods=['GET','POST'])
def submit_application_confirmation(card_id):
    try:
        card = authmdl.Card.query.filter_by(pin=card_id).first()
        applicant = card.applicant
        form = fms.AgreementForm()
        if form.validate_on_submit():
            agreed = form.agreed.data
            admission_type = form.admission_type.data
            agreement = mdl.Agreement(agreed=agreed,admission_type=admission_type)
            agreement.applicant_id = applicant.id 
            db.session.add(agreement)
            db.session.commit()
            return redirect(request.url)
        if applicant.agreed and applicant.agreed.agreed == True:
            flash('You have submited application \n You can not edit the application.\n Contact the administrator for access.',category='info')
        return render_template('application/application_confirmation.html',applicant=applicant,form=form)
    except Exception as e:
        print(e)
        return render_template('errors/404.html')


@application.route('/check-admission-status/<card_id>')
def check_admission_status(card_id):
    '''return the admission status of the applicant
    if applicant is admitted the print the admission letter.
    
    '''
    card = authmdl.Card.query.filter_by(pin=card_id).first()
    if card is not None:
        if not card.applicant:
            return redirect(url_for('application.applicant_personal_info',card_id=card.pin))
        return render_template('application/admission_status.html',card=card)
    return render_template('errors/404.html')

#============================ view applicant employment details ==========================================
@application.route('/view-applicant-employment/details/<card_id>')
def view_employment_details(card_id):
    '''veiw all applicant employment details and edit any'''
    card = authmdl.Card.query.filter_by(pin=card_id).first()
    try:
        applicant = card.applicant
        if applicant is not None:
            return render_template('application/view_applicant_emplo_details.html',applicant=applicant)
    except Exception as e:
        return render_template('errors/404.html')
# ===========================================Edit applicants information =================================

@application.route('/edit-personal/info/<card_id>',methods=['GET','POST'])
def edit_personel_info(card_id):
    '''Edit the information of the applicant if they are avaliable'''
    card = authmdl.Card.query.filter_by(pin=card_id).first()
    try:
        applicant = card.applicant
        form = fms.ApplicantForm(obj=applicant)
        if form.validate_on_submit():
            if form.passport_picture.data:
                image = save_passport(form.passport_picture.data)
                form.populate_obj(applicant)
                applicant.passport_picture = image
                db.session.add(applicant)
                db.session.commit()
            return redirect(url_for('application.dashboard',card_id=card.pin))
        return render_template('application/edit_personal_info.html',form=form,applicant=applicant)
    except Exception as e:
        print(e)
        return render_template('errors/404.html')

@application.route('/edit-confrim/info/<card_id>',methods=['GET','POST'])
def edit_personel_confirm(card_id):
    '''Edit the information of the applicant if they are avaliable'''
    try:
        card = authmdl.Card.query.filter_by(pin=card_id).first()
        applicant = card.applicant
        if applicant is not None:
            form = fms.AgreementForm(obj=applicant)
            if form.validate_on_submit():
                applicant.agreed.agreed = form.agreed.data
                applicant.agreed.admission_type = form.admission_type.data
                db.session.add(applicant)
                db.session.commit()
                return redirect(url_for('application.submit_application_confirmation',card_id=card.pin))
    except Exception as e:
        print(e)
        return render_template('errors/404.html')

@application.route('/edit-personal/contact/info/<card_id>',methods=['GET','POST'])
def edit_personel_contact_info(card_id):
    '''Edit the information of the applicant if they are avaliable'''
    card = authmdl.Card.query.filter_by(pin=card_id).first()
    try:
        applicant = card.applicant
        if applicant is not None:
            contact_info = applicant.contact
            form = fms.ContactForm(obj=contact_info)
            if form.validate_on_submit():
                form.populate_obj(contact_info)
                db.session.add(contact_info)
                db.session.commit()
                return redirect(url_for('application.dashboard',card_id=card.pin))
            return render_template('application/edit_contact_info.html',form=form,applicant=applicant)
    except Exception as e:

        return render_template('errors/404.html')

@application.route('/edit-education/info/<card_id>',methods=['GET','POST'])
def edit_personel_education_info(card_id):
    '''Edit the information of the applicant if they are avaliable'''
    card = authmdl.Card.query.filter_by(pin=card_id).first()
    try:
        applicant = card.applicant
        if applicant is not None:
            education_info = applicant.education
            form = fms.EducationForm(obj = education_info)
            if form.validate_on_submit():
                form.populate_obj(education_info)
                cert_file = None
                tran_file = None
                second_cert_file = None
                second_trans_file = None
                if form.certificate_file.data and form.transcript_file.data:
                    cert_file = save_passport(form.certificate_file.data)
                    tran_file = save_passport(form.transcript_file.data)
                    education_info.certificate_file = cert_file
                    education_info.transcript_file = tran_file
                    if applicant.results:
                        for result in applicant.results.all():
                            db.session.delete(result)
                    db.session.add(education_info)
                    db.session.commit()
                if form.second_certificate_file.data and form.second_transcript_file.data:
                    second_cert_file = save_passport(form.second_transcript_file.data)
                    second_trans_file = save_passport(form.second_transcript_file.data)
                    education_info.certificate_file = cert_file
                    education_info.transcript_file = tran_file
                    education_info.second_certificate_file = second_cert_file
                    education_info.second_transcript_file = second_trans_file
                    if applicant.results:
                        for result in applicant.results.all():
                            db.session.delete(result)
                    db.session.add(education_info)
                    db.session.commit()
                return redirect(url_for('application.dashboard',card_id=card.pin))
            return render_template('application/edit_education_info.html',form=form,applicant=applicant)
    except Exception as e:
        print(e)
        return render_template('errors/404.html')

@application.route('/edit-personal/info/<int:employment_id>',methods=['GET','POST'])
def edit_employment__info(employment_id):
    '''Edit the information of the applicant if they are avaliable'''
    '''  
    '''
    employment = mdl.Employment.query.get(employment_id)
    if employment is not None:
        form = fms.EmploymentForm(obj=employment)
        if form.validate_on_submit():
            form.populate_obj(employment)
            db.session.add(employment)
            db.session.commit()
            return redirect(url_for('application.dashboard',employment_id=employment.id))
        return render_template('application/edit_employment_info.html',form=form,employment=employment)
    return render_template('errors/404.html')

@application.route('/edit-referee/info/<card_id>',methods=['GET','POST'])
def edit_referee_info(card_id):
    '''Edit the information of the applicant if they are avaliable'''
    card = authmdl.Card.query.filter_by(pin=card_id).first()
    try:
        applicant = card.applicant
        if applicant is not None:
            referee_info = applicant.referee
            form = fms.RefereesForm(obj = referee_info)
            if form.validate_on_submit():
                form.populate_obj(referee_info)
                db.session.add(referee_info)
                db.session.commit()
                return redirect(url_for('application.dashboard',card_id=card.pin))
            return render_template('application/edit_referee.html',form=form,applicant=applicant)
    except Exception as e:

        return render_template('errors/404.html')

@application.route('/edit-choice/info/<card_id>',methods=['GET','POST'])
def edit_choices_info(card_id):
    '''Edit the information of the applicant if they are avaliable
    db.session.query(md.Choice).delete()
    '''
    card = authmdl.Card.query.filter_by(pin=card_id).first()
    try:
        applicant = card.applicant
        if applicant is not None:
            choice_info = applicant.choice
            form = fms.ChoiceForm()
            if form.validate_on_submit():
                try:
                    db.session.delete(choice_info)
                    db.session.commit()
                    lgs.process_choices_info(form=form,applicant_id=applicant.id)
                    return redirect(url_for('application.dashboard',card_id=card.pin))
                except Exception as e:
                    db.session.rollback()
                    flash('You couldn\'t edit your programme of choice contact the admission office for appropriate action',category='warning')
                    return redirect(url_for('application.dashboard',card_id=card.pin))
            return render_template('application/edit_choice.html',form=form,applicant=applicant)
    except Exception as e:
        return render_template('errors/404.html')

@application.route('/print-application/letter/<card_id>')
def print_application_letter(card_id):
    card = authmdl.Card.query.filter_by(pin=card_id).first()
    try:
        applicant = card.applicant
        applicant_image = url_for('static',filename = 'images/applicant_passport/'+applicant.passport_picture)

        if applicant is not None:
            if applicant.choice is not None:
                first_ch_programme = apmdl.Programme.query.filter_by(programme_name=applicant.choice.first_choice).first()
                second_ch_programme = apmdl.Programme.query.filter_by(programme_name=applicant.choice.second_choice).first()
                third_ch_programme = apmdl.Programme.query.filter_by(programme_name=applicant.choice.third_choice).first()
            else:
                first_ch_programme = apmdl.Postgradprogramme.query.filter_by(programme_title=applicant.postgradchoice.first_choice).first()
                second_ch_programme = apmdl.Postgradprogramme.query.filter_by(programme_title=applicant.postgradchoice.second_choice).first()
                third_ch_programme = apmdl.Postgradprogramme.query.filter_by(programme_title=applicant.postgradchoice.third_choice).first() 
            return render_template('/application/application_letter.html',
                                   applicant=applicant,applicant_image=applicant_image
                                    ,first_ch_programme=first_ch_programme,
                                second_ch_programme=second_ch_programme,third_ch_programme=third_ch_programme
                               )
    except Exception as e:
        return render_template('errors/404.html')

@application.route('/print-postgrad-application/letter/<card_id>')
def print_postgrad_application_letter(card_id):
    card = authmdl.Card.query.filter_by(pin=card_id).first()
    try:
        applicant = card.applicant
        if applicant is not None:
            return render_template('/application/postgrad_application_letter.html',
                                   applicant=applicant,
                                   )
    except Exception as e:
        return render_template('errors/404.html')

@application.route('/print-admission/letter/<card_id>')
def print_admission_letter(card_id):
    card = authmdl.Card.query.filter_by(pin=card_id).first()
    try:
        applicant = card.applicant
        dues = apmdl.Srcdues.query.order_by(apmdl.Srcdues.date_added.desc()).first()
        registrar = authmdl.Registrar.query.first()
        banks = authmdl.Bank.query.all()
        applicant_image = url_for('static',filename = 'images/applicant_passport/'+applicant.passport_picture)
        registrar_sign = url_for('static',filename='images/admin_img/'+registrar.registrar_signature)
        if applicant is not None:
            return render_template('/application/print_admission_letter.html',applicant=applicant,
                                   dues=dues,banks=banks,applicant_image=applicant_image,
                                   registrar=registrar,registrar_sign=registrar_sign)
    except Exception as e:
        print(e)
        return render_template('errors/404.html')