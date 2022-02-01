from .. import db 
from flask import flash
from . import models as mdl


def process_personal_info_data(form,card_id,image_file):
    surname = form.surname.data
    first_name = form.first_name.data
    last_name = form.last_name.data
    gender = form.gender.data
    date_of_birth = form.date_of_birth.data
    home_town = form.home_town.data
    home_region = form.home_region.data
    marital_status = form.marital_status.data
    childrens = form.childrens.data
    religion = form.religion.data
    sponsorship = form.sponsorship.data
    passport = image_file
    employed = form.employed.data
    # save the data into the database.
    personal_info = mdl.Applicant(
      surname=surname,first_name=first_name,last_name=last_name,
      gender=gender,date_of_birth=date_of_birth,home_town=home_town,home_region=home_region,
      marital_status=marital_status,childrens=childrens,
      religion=religion,sponsorship=sponsorship,
      passport_picture= passport,employed=employed
    )
    try:
      personal_info.card_id = card_id
      db.session.add(personal_info)
      db.session.commit()
    except Exception as e:
      db.session.rollback() 
      print(e)
      flash(f'Your operation was not successfull due to {e}',category='danger')
      

def process_contact_info(form,applicant_id):
  country = form.country.data
  contact_number = form.contact_number.data
  contact_number_2 = form.contact_number_2.data 
  email   = form.email.data
  residence_address = form.residence_address.data 
  digital_address = form.digital_address.data 
  postal_address = form.postal_address.data
  post_town = form.post_town.data 
  post_region = form.post_region.data
  # the applicant model id
  contact_info = mdl.Contact( country=country,contact_number=contact_number,
                             contact_number_2=contact_number_2,email=email,
                             residence_address=residence_address,digital_address=digital_address,
                             postal_address=postal_address,post_town=post_town,
                             post_region=post_region
                             )
  contact_info.applicant_id = applicant_id
  try:
    db.session.add(contact_info)
    db.session.commit() 
    return applicant_id
  except Exception as e:
    db.session.rollback()
    flash(f'Operation was unsuccessfull due to {e}',category='danger')
  
def process_education_info(form,applicant,cert_file,tran_file,second_cert_file,second_tran_file):
  school_name = form.school_name.data
  location = form.location.data
  date_started = form.date_started.data
  date_completed = form.date_completed.data
  offered_programme =form.offered_programme.data
  education_type  =form.education_type.data
  graduated_class =form.graduated_class.data
  graduated_gpa   = form.graduated_gpa.data
  certificate_file = cert_file
  transcript_file = tran_file
  second_graduated_gpa   = form.second_graduated_gpa.data
  second_graduated_class = form.second_graduated_class.data
  second_certificate_file = second_cert_file
  second_transcript_file = second_tran_file
  education_info = mdl.Education( 
                                school_name = school_name,location=location, date_started = date_started,date_completed = date_completed,
                                offered_programme=offered_programme,education_type  = education_type,
                                graduated_class = graduated_class,graduated_gpa= graduated_gpa,certificate_file= certificate_file, 
                                transcript_file = transcript_file,second_graduated_gpa=second_graduated_gpa,
                                second_graduated_class=second_graduated_class,second_certificate_file=second_certificate_file,
                                second_transcript_file=second_transcript_file
                                 )
  education_info.applicant_id = applicant.id
  try:
    db.session.add(education_info)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    print(f'the data was unable to save due to {e}')  
  
def process_results_info(form,applicant_id):
  cert_1_number  = form.cert_1_index_number.data
  results_type = form.results_type.data 
  subject_core_1 = str(form.core_subject_1.data)
  core_grade_1   = str(form.grade_got_subject_1.data)
  
  subject_core_2 = str(form.core_subject_2.data)
  core_grade_2   =  str(form.grade_got_subject_2.data)
  
  subject_core_3  = str(form.core_subject_3.data)
  core_grade_3 = str(form.grade_got_subject_3.data)
  
  subject_core_4   = str(form.core_subject_4.data)
  core_grade_4  = str(form.grade_got_subject_4.data)
  
  subject_elective_1 = str(form.elective_subject_1.data)
  elective_grade_1   = str(form.grade_got_ele_subject_1.data)
  
  subject_elective_2  = str(form.elective_subject_2.data)
  elective_grade_2 = str(form.grade_got_ele_subject_2.data)
  
  subject_elective_3   = str(form.elective_subject_3.data)
  elective_grade_3  = str(form.grade_got_ele_subject_3.data)
  
  subject_elective_4   = str(form.elective_subject_4.data)
  elective_grade_4  = str(form.grade_got_ele_subject_4.data)

  
  results_info = mdl.Result(
    cert_1_number=cert_1_number,results_type=results_type,subject_core_1=subject_core_1,core_grade_1=core_grade_1,
    subject_core_2=subject_core_2,core_grade_2=core_grade_2,subject_core_3=subject_core_3,
    core_grade_3=core_grade_3,subject_core_4=subject_core_4,core_grade_4=core_grade_4,
    subject_elective_1=subject_elective_1,elective_grade_1=elective_grade_1,subject_elective_2=subject_elective_2,
    elective_grade_2=elective_grade_2,subject_elective_3=subject_elective_3,elective_grade_3=elective_grade_3,
    subject_elective_4=subject_elective_4,elective_grade_4=elective_grade_4
    )
  results_info.applicant_id = applicant_id
  try:
    db.session.add(results_info)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    print(f'Operation Failed Due To {e}')
  
def process_employment_info(form,applicant_id):
  organisation_name = form.organisation_name.data
  organisation_address = form.organisation_address.data
  organisation_contact = form.organisation_contact.data
  position_held   = form.position_held.data
  date_started    =   form.date_started.data
  date_ended      =   form.date_ended.data
  
  employment_info = mdl.Employment(organisation_name=organisation_name,organisation_address=organisation_address,
                                   organisation_contact=organisation_contact,position_held=position_held,
                                   date_started=date_started,date_ended=date_ended
                                   )
  employment_info.applicant_id = applicant_id
  try:
    db.session.add(employment_info)
    db.session.commit() 
  except Exception as e:
    db.session.rollback() 
    print(f'operation failed due to {e}')
  
def proccess_refeeres_guardian_info(form,applicant_id):
  referees_name = form.referees_name.data
  referees_work_place = form.referees_work_place.data
  referees_address = form.referees_address.data
  referees_email = form.referees_email.data
  referees_contact = form.referees_contact.data
  
  refeeres_info = mdl.Referees( referees_name=referees_name,referees_work_place=referees_work_place,
                               referees_address=referees_address,referees_email=referees_email,
                               referees_contact=referees_contact
                               ) 
  refeeres_info.applicant_id = applicant_id
  try:
    db.session.add(refeeres_info)
    db.session.commit() 
  except Exception as e:
    db.session.rollback() 
    flash(f'operation failed because of {e}',category='danger')
  
def process_choices_info(form,applicant_id):
  first_choice = str(form.first_choice.data)
  second_choice =str(form.second_choice.data)
  third_choice = str(form.third_choice.data)
  
  choices_info = mdl.Choice(first_choice =first_choice,second_choice =second_choice,third_choice = third_choice )
  choices_info.applicant_id = applicant_id
  try:
    db.session.add(choices_info)
    db.session.commit() 
    flash('saved successfully',category='success')
  except Exception as e:
    db.session.rollback() 
    flash(f'Operation Failed due to {e}',category='danger')
  
def process_postgrad_choices_info(form,applicant_id):
  first_choice = str(form.first_choice.data)
  second_choice =str(form.second_choice.data)
  third_choice = str(form.third_choice.data)
  
  choices_info = mdl.Postgradchoice(first_choice =first_choice,second_choice =second_choice,third_choice = third_choice )
  choices_info.applicant_id = applicant_id
  try:
    db.session.add(choices_info)
    db.session.commit() 
    flash('saved successfully',category='success')
  except Exception as e:
    db.session.rollback() 
    flash(f'Operation Failed due to {e}',category='danger')
    

  