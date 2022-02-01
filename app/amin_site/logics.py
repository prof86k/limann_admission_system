from flask.helpers import flash
from .. import db
from .. import models as mdl
from ..models import Postgradprogramme, Programme,Lengthofgradingsubjects
from ..auth import models as autmd
from ..application.models import Applicant
import time

def create_faculty(form):
    faculty_name = form.faculty_name.data 
    faculty_code = form.faculty_code.data
    new_faculty = mdl.Faculty(faculty_name=faculty_name,faculty_code=faculty_code)
    try:
        db.session.add(new_faculty)
        db.session.commit()
    except Exception as e:
        print(e)
        flash(f'Operation unsuccessful due to {e}')

def process_create_department(form,faculty_id):
    '''process the creation of department aqdd card state so admin can set whether it is free or not and add fees for eachelevel'''
    department_name = form.department_name.data
    new_department = mdl.Department(department_name=department_name)
    new_department.faculty_id = faculty_id
    try:
        db.session.add(new_department)
        db.session.commit()
        flash('Department Created Successfully',category='success')
    except Exception as e:
        db.session.rollback() 
        flash(f'Data unable to save due to {e} error.')
    
def create_run_levels(form,department):
    '''process the creation of a level for the department'''
    appliction_type = form.appliction_type.data
    is_avaliable = form.is_avaliable.data
    new_type = mdl.Type(appliction_type=appliction_type,
                        is_avaliable=is_avaliable)
    new_type.department_id = department.id
    try:
        db.session.add(new_type)
        db.session.commit()
        flash('Level Created Successfully',category='success')
    except Exception as e:
        db.session.rollback()
        flash(f'Degree Or Masters has not been able to create because of {e}') 
        
        
def process_level_programme(form, run_type) -> bool:
    '''process the creation of programmes in the level'''
    programme_name = form.programme_name.data
    programme_duration_direct = form.programme_duration_topup.data
    programme_duration_topup = form.programme_duration_topup.data
    cut_off_point = form.cut_off_point.data
    is_avaliable = form.is_avaliable.data
    min_class = form.min_class.data
    programme_admission_fees = form.programme_admission_fees.data
    
    new_programme = mdl.Programme(programme_name=programme_name,programme_duration_direct=programme_duration_direct,programme_duration_topup=programme_duration_topup,cut_off_point=cut_off_point,
                                 min_class=min_class, is_avaliable=is_avaliable,programme_admission_fees=programme_admission_fees)
    try:
        new_programme.type_id = run_type.id
        db.session.add(new_programme)
        db.session.commit()
        flash('Programe created Successfully',category='success')
    except Exception as e:
        db.session.rollback() 
        flash(f'Unable to add programme due to {e}',category='success')
        
def process_postgrad_level_programme(form, run_type):
    '''process the creation of programmes in the level'''
    programme_title = form.programme_title.data
    programme_duration = form.programme_duration.data
    min_gpa = form.min_gpa.data
    active = form.active.data
    programme_admission_fees = form.programme_admission_fees.data

    new_programme = mdl.Postgradprogramme(programme_title=programme_title,programme_duration=programme_duration,min_gpa=min_gpa,
                                  active=active,programme_admission_fees=programme_admission_fees)
    try:
        new_programme.type_id = run_type.id
        db.session.add(new_programme)
        db.session.commit()
        flash('Programe created Successfully',category='success')
    except Exception as e:
        db.session.rollback() 
        flash(f'Unable to add programme due to {e}',category='success')
    
        
def process_subjects(form) -> bool:
    '''process the creation of subjects recquire for admission'''
    subject_name = form.subject_name.data
    subject_status = form.subject_status.data
    min_grade = form.min_grade.data
    
    new_subject = mdl.Subject(subject_name=subject_name,subject_status=subject_status,
                              min_grade=min_grade)
    try:
        db.session.add(new_subject)
        db.session.commit()
        flash('Subject Created Successfully',category='success')
    except Exception as e:
        db.session.rollback() 
        flash(f'Operation Failed Due to {e}',category='danger')

def process_add_require_subjects(form,programme):
    '''add the required subject from the form to the specified subject'''
    subject = form.subject_name.data
    try:
        programme.subjects.append(subject)
        db.session.add(subject)
        db.session.commit() 
    except Exception as e:
        db.session.rollback()
        flash(f'Your operation failed due to {e}')


def process_delete_programme(programme):
    '''delete the required programme from the level and department'''
    try:
        db.session.delete(programme)
        db.session.commit()
        flash(f'Programme Successfully Deleted',category='danger')
    except Exception as e:
        flash(f'Operation Failed Due to {e}',category='danger')

def process_delete_postgrad_programme(programme):
    '''delete the required programme from the level and department'''
    try:
        db.session.delete(programme)
        db.session.commit()
        flash(f'Programme Successfully Deleted',category='danger')
    except Exception as e:
        flash(f'Operation Failed Due to {e}',category='danger')
        
def process_delete_level(level):
    '''delete the require level from the department'''
    try:
        db.session.delete(level)
        db.session.commit()
        flash(f'Your operation was successfull',category='success')
    except Exception as e:
        flash(f'Operation failed due to {e}',category='danger')

def process_delete_department(department):
    '''delete the require department'''
    try:
        db.session.delete(department)
        db.session.commit()
        flash(f'Your Operation Successfull',category='success')
    except Exception as e:
        flash(f'Operation failed due to {e}',category='danger')
        
def process_delete_subject(subject):
    '''delete the require subject'''
    try:
        db.session.delete(subject)
        db.session.commit() 
        flash(f'Your Operation Successfull',category='success')
    except Exception as e:
        flash(f'Operation failed due to {e}',category='danger')

def get_results(applicant,choices):
    '''calculate the minimum grade for 6 subject '''
    try:
        programme = Programme.query.filter_by(programme_name=choices).first()
        courses = programme.subjects
        # length = Lengthofgradingsubjects.query.first()
        if applicant.card.buy.application_type=='MATURE':
            min_class = str(programme.min_class).lower()
            applicant_class= str(applicant.education.graduated_class).lower()
            return applicant_class,min_class
        else:
            results_dic = {}
            grades = []
            total = 0
            for result in applicant.results.all():
                for course in courses:
                    try:
                        if str(course) == str(result.subject_core_1):
                            if not results_dic.get(result.subject_core_1):
                                results_dic[result.subject_core_1]=[result.core_grade_1,int(result.core_grade_1[1])]
                            elif results_dic.get(result.subject_core_1)[1] > int(result.core_grade_1[1]):
                                results_dic[result.subject_core_1]=[result.core_grade_1,int(result.core_grade_1[1])]
                        elif str(course) == str(result.subject_core_2):
                            if not results_dic.get(result.subject_core_2):
                                results_dic[result.subject_core_2]=[result.core_grade_2,int(result.core_grade_2[1])]
                            elif results_dic.get(result.subject_core_2)[1] > int(result.core_grade_2[1]):
                                results_dic[result.subject_core_2]=[result.core_grade_2,int(result.core_grade_2[1])]
                        elif str(course) == str(result.subject_core_3):
                            if not results_dic.get(result.subject_core_3):
                                results_dic[result.subject_core_3]=[result.core_grade_3,int(result.core_grade_3[1])]
                            elif results_dic.get(result.subject_core_3)[1] > int(result.core_grade_3[1]):
                                results_dic[result.subject_core_3]=[result.core_grade_3,int(result.core_grade_3[1])]
                        elif str(course) == str(result.subject_core_4):
                            if not results_dic.get(result.subject_core_4):
                                results_dic[result.subject_core_4]=[result.core_grade_4,int(result.core_grade_4[1])]
                            elif results_dic.get(result.subject_core_4)[1] > int(result.core_grade_4[1]):
                                results_dic[result.subject_core_4]=[result.core_grade_4,int(result.core_grade_4[1])]
                        elif str(course) == str(result.subject_elective_1):
                            if not results_dic.get(result.subject_elective_1):
                                results_dic[result.subject_elective_1]=[result.elective_grade_1,int(result.elective_grade_1[1])]
                            elif results_dic.get(result.subject_elective_1)[1] > int(result.elective_grade_1[1]):
                                results_dic[result.subject_elective_1]=[result.elective_grade_1,int(result.elective_grade_1[1])]
                        elif str(course) == str(result.subject_elective_2):
                            if not results_dic.get(result.subject_elective_2):
                                results_dic[result.subject_elective_2]=[result.elective_grade_2,int(result.elective_grade_2[1])]
                            elif results_dic.get(result.subject_elective_2)[1] > int(result.elective_grade_2[1]):
                                results_dic[result.subject_elective_2]=[result.elective_grade_2,int(result.elective_grade_2[1])]
                        elif str(course) == str(result.subject_elective_3):
                            if not results_dic.get(result.subject_elective_3):
                                results_dic[result.subject_elective_3]=[result.elective_grade_3,int(result.elective_grade_3[1])]
                            elif results_dic.get(result.subject_elective_3)[1] > int(result.elective_grade_3[1]):
                                results_dic[result.subject_elective_3]=[result.elective_grade_3,int(result.elective_grade_3[1])]
                        elif str(course) == str(result.subject_elective_4):
                            if not results_dic.get(result.subject_elective_4):
                                results_dic[result.subject_elective_4]=[result.elective_grade_4,int(result.elective_grade_4[1])]
                            elif results_dic.get(result.subject_elective_4)[1] > int(result.elective_grade_4[1]):
                                results_dic[result.subject_elective_4]=[result.elective_grade_4,int(result.elective_grade_4[1])]
                    except Exception as e:
                        print(f'The Error is {e}')
                        pass
            for value in results_dic.values():
                grades.append(value[1])
            if len(grades) < 6:#length:
                flash(f'Grading subjects are not up to 6 {programme}',category='danger')
            else:
                new_list = sorted(grades)
                total += sum(new_list[0:6])
            return total,programme.cut_off_point
    except AttributeError:
        pass


def process_admit_appicant(datum,app):
    with app.app_context():
        for data in datum.values():
            applicant_id = int(data['applicant id'])
            applicant_name = data['applicant name']
            applicant_option = data['applicant option']
            applicant_status = data['admission status']
            programme = Programme.query.filter_by(programme_name=applicant_option).first()
            
            if programme is None:
                programme = Postgradprogramme.query.filter_by(programme_title=applicant_option).first()
            
            try:
                year_digits = time.strftime('%Y',time.localtime())
                admit = mdl.Admission(person_full_name=applicant_name,
                          programme_listed=applicant_option,
                          admission_status=applicant_status)
                admit.applicant_id = applicant_id
                admit.level_id = programme.type.id
                admission = mdl.Admission.query.count()
                admit.student_id = str(year_digits)+'{0:04}'.format(int(admission)+1)
                db.session.add(admit)
                db.session.commit() 
            except Exception as e:
                db.session.rollback()
                flash(f'Data not saved due to {e}',category='danger')  
                
# ============================ process card and related issues==============================
def process_set_cards(form):
    state = form.state.data
    card_type = form.card_type.data
    amount = form.amount.data
    
    new_card_type = autmd.Cardstate(card_type=card_type,state=state,amount=amount)
    try:
        db.session.add(new_card_type)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        flash(f'Operation failed Due To {e}')
        
# ====================== create users ===================================
def process_user_creation(form):
    username = form.username.data
    email = form.email.data
    password = form.password.data
    new_user = autmd.Admin(username=username)
    new_user.email = email
    new_user.set_password_to_hash(password)
    new.roles.append('card_seller')
    try:
        db.session.add(new_user)
        db.session.commit()
        flash('User save successfully',category='success')
    except Exception as e:
        db.session.rollback()
        flash(f'User could not be created due error',category='danger')
        print(e)