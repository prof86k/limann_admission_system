from flask import render_template,redirect,request,jsonify,current_app
from flask.helpers import flash, url_for
from . import admin_panel
from . import logics as lgs
from .. import models as mdl
from ..auth import models as authmdl
from ..auth import forms as authfms
from ..application import models as appmdl
from . import forms as fms
from .. import db, excel,create_app
import csv
import os
from threading import Thread
from flask_login import login_required
from ..auth.decorators import has_role

# ======================== admin dashboard ==========================
@admin_panel.route('/dashbord',methods=['GET','POST'])
@login_required
@has_role('admin')
def admin_dashboard():
    '''display the admin dashboard give option for adding a department'''
    departments_number = mdl.Department.query.count()
    types = mdl.Type.query.count()
    programmes = mdl.Programme.query.count()
    cards = authmdl.Card.query.count() 
    agreed_applicants = appmdl.Agreement.query.filter_by(agreed=True).all()
    direct_applicants = 0
    mature_applicants = 0
    for applicants in agreed_applicants:
        if applicants.applicant.card is None:
            db.session.delete(applicants.applicant.contact)
            db.session.delete(applicants.applicant.education)
            db.session.delete(applicants.applicant.referee)
            db.session.delete(applicants.applicant.agreed)
            db.session.delete(applicants.applicant.choice)
            db.session.delete(applicants.applicant)
            db.session.commit()
        else:
            if applicants.applicant.card.buy.application_type == 'DIRECT':
                direct_applicants += 1
            else:
                mature_applicants += 1
    admitted_number = mdl.Admission.query.count()
    type_levels = mdl.Type.query.distinct(mdl.Type.appliction_type) 
    faculty_number = mdl.Faculty.query.count()
    form = fms.FacultyForm() 
    if form.validate_on_submit():
        lgs.create_faculty(form)
        return redirect(url_for('admin_panel.view_faculty'))
    return render_template('admin_site/admin_dashboard.html',
                           form=form,programmes=programmes,cards=cards,faculty_number=faculty_number,
                           types=types,departments_number=departments_number,
                           direct_applicants=direct_applicants,mature_applicants=mature_applicants,admitted_number=admitted_number,
                           type_levels=type_levels
                           )

# ============================= admin actions ==============================================================
@admin_panel.route('/view/department')
@login_required
@has_role('admin')
def view_departments():    

    faculties = mdl.Faculty.query.all()
    form = fms.CreateDepartment()
    return render_template('admin_site/view_departments.html',faculties=faculties,form=form)


@admin_panel.route('/view-faculty')
@login_required
@has_role('admin')
def view_faculty():

    '''return the list of departments eg. DEPARTMENT OF COMPUTER SCIENCE and give option for adding academic levels
    eg. DIPLOMA'''
    form = fms.FacultyForm() 
    faculties = mdl.Faculty.query.all()
    return render_template('admin_site/view_faculty.html',faculties=faculties,form=form)

@admin_panel.route('/create-departments/<faculty_id>',methods=['GET','POST'])
@login_required
@has_role('admin')
def create_department(faculty_id):

    form = fms.CreateDepartment()
    faculty = mdl.Faculty.query.filter_by(id=faculty_id).first()
    if form.validate_on_submit():
        lgs.process_create_department(form,faculty_id)
        return redirect(request.url)
    return render_template('admin_site/add_department.html',faculty=faculty,form=form)


@admin_panel.route('/veiw-levels/')
@login_required
@has_role('admin')
def view_runned_levels():

    departments = mdl.Department.query.all()
    form = fms.CreateLevelTypeForm()
    return render_template('admin_site/view_levels.html',departments=departments,form =form)

@admin_panel.route('/create-level/<int:department_id>',methods=['GET','POST'])
@login_required
@has_role('admin')
def create_level(department_id):

    '''View all the academic levels eg. DIPLOMA,DEGREE in a department and give option for adding programme to the level 
    eg. DIPLOMA IN COMPUTER SCIENCE'''
    department = mdl.Department.query.get(department_id)
    form = fms.CreateLevelTypeForm()
    if form.validate_on_submit():
        lgs.create_run_levels(form,department)
        return redirect(url_for('admin_panel.create_level',department_id=department.id))
    return render_template('admin_site/create_levels.html',form=form,department=department)

@admin_panel.route('/create-postgrad-programme/<int:level_id>',methods=['GET','POST'])
@login_required
@has_role('admin')
def create_postgrad_level_programme(level_id):
    run_type = mdl.Type.query.get(level_id)
    form = fms.AddPostGradProgrammeForm() 
    if form.validate_on_submit():
        lgs.process_postgrad_level_programme(form,run_type)
        return redirect(request.url)
    return render_template('admin_site/add_postgrad_programme.html',form=form,run_type=run_type)

@admin_panel.route('/create-programme/<int:level_id>',methods=['GET','POST'])
@login_required
@has_role('admin')
def create_level_programme(level_id):
    run_type = mdl.Type.query.get(level_id)
    form = fms.AddProgrammeRunForm() 
    if form.validate_on_submit():
        lgs.process_level_programme(form,run_type)
        return redirect(request.url)
    return render_template('admin_site/view_level_programmes.html',form=form,run_type=run_type)

@admin_panel.route('/create-subject/',methods=['GET','POST'])
@login_required
@has_role('admin')
def create_subject():
    subjects = mdl.Subject.query.all()
    form = fms.RequireAddmissonSubjectForm()
    if form.validate_on_submit():
        lgs.process_subjects(form)
        return redirect(request.url)
    return render_template('admin_site/load_require_subjects.html',form=form,subjects=subjects) 

@admin_panel.route('/add-require-subjets/<int:programme_id>',methods=['GET','POST'])
@login_required
@has_role('admin')
def load_require_subjects(programme_id):
    programme = mdl.Programme.query.get(programme_id)
    form = fms.LoadRequireSubjectsForm()
    if form.validate_on_submit():
        lgs.process_add_require_subjects(form,programme)
    return render_template('admin_site/add_require_subjects.html',form=form,programme=programme)

@admin_panel.route('/programmes')
@login_required
@has_role('admin')
def view_level_programmes():
    programmes = mdl.Department.query.all()
    '''list all programmes in a level eg. DIPLOMA IN COMPUTER SCIENCE and give option for adding a 
    subject require for admission to a programme eg. ENGLISH or BSC. COMPUTER SCIENCE for masters level'''
    return render_template('admin_site/view_all_programmes.html',programmes=programmes)

@admin_panel.route('/postgraduate/programmes')
@login_required
@has_role('admin')
def view_post_graduate_programmes():
    departments = mdl.Department.query.all()
    return render_template('admin_site/postgrad_programmes.html',programmes=departments)

@admin_panel.route('/subjects')
@login_required
@has_role('admin')
def view_require_subjects():
    '''list all subjects require by a programme for admission eg..
    DIPLOMA COMPUTER needs english, maths science'''
    
    return render_template('admin_site/view_admission_require_subjects.html')


# =============================================== applicants and related ==========================
@admin_panel.route('/admit-applicants')
@login_required
@has_role('admin')
def view_and_admin_applicants():
    #page = request.args.get("page",1,int)
    '''view and admit applicants who are shortlistes'''
    applicants = appmdl.Applicant.query.all()#.paginate(page,1)
    return render_template('admin_site/admit_applicants.html',applicants=applicants)

@admin_panel.route('/mature-applicants')
@login_required
@has_role('admin')
def view_admit_mature_applicants():
    #page = request.args.get("page",1,int)
    '''view and admit applicants who are shortlistes'''
    applicants = appmdl.Applicant.query.all()#.paginate(page,1)
    return render_template('admin_site/admit_mature.html',applicants=applicants)

# ================================ ajax request ============================
@admin_panel.route('/admit',methods=['POST'])
@login_required
@has_role('admin')
def admit_applicant():
    if request.method == 'POST':
        datum = request.get_json()
        app=create_app()
        thread = Thread(target=lgs.process_admit_appicant,args=[datum,app])
        thread.start()
        return redirect(url_for('admin_panel.view_and_admin_applicants'))
    
@admin_panel.route('/all-admitted/students/')
@login_required
@has_role('admin')
def view_all_admitted_students():
    '''show all admitted applicants'''
    page = request.args.get('page',1,int)
    admitted = appmdl.Applicant.query.paginate(page,15)
    return render_template('admin_site/view_undergrade_students.html',admitted=admitted)


@admin_panel.route('/view-applicant-details/<int:applicant_id>')
@login_required
@has_role('admin')
def view_applicant_details(applicant_id):
    '''view the details of the listed applicant'''
    applicant = appmdl.Applicant.query.get(applicant_id)
    return render_template('admin_site/view_applicant_details.html',applicant=applicant)

@admin_panel.route('/get-grade/<int:applicant_id>/<choice>')
def get_grade(applicant_id,choice):
    '''androapana@gmail.com'''
    applicant = appmdl.Applicant.query.get(applicant_id)
    results = {}
    grade,cutoff = lgs.get_results(applicant,choice)
    results['grade'] = grade
    results['cutoff'] = cutoff
    return jsonify({'results':results})

@admin_panel.route('/allow-edit/<int:applicant_id>')
def allow_edit(applicant_id):
    applicant = appmdl.Applicant.query.get(applicant_id)
    applicant.agreed.agreed = False
    try:
        
        db.session.commit()
    except Exception as e:
        print(e)
    return redirect(url_for('admin_panel.admin_dashboard'))
# ================================== context processor
@admin_panel.context_processor
@login_required
@has_role('admin')
def context():
    '''pass the calculated results into the context processer
    for templates usage'''
    return  dict(get_results=lgs.get_results)

# =============================== admin delete information =======================
@admin_panel.route('/delete-faculty/<int:faculty_id>')
@login_required
@has_role('admin')
def delete_faculty(faculty_id):
    '''delete the faculty'''
    faculty = mdl.Faculty.query.get(faculty_id)
    db.session.delete(faculty)
    db.session.commit()
    return redirect(url_for('admin_panel.view_faculty'))


@admin_panel.route('/delete-department/<int:department_id>')
@login_required
@has_role('admin')
def delete_department(department_id):
    '''delete deparmtment'''
    department = mdl.Department.query.get(department_id)
    lgs.process_delete_department(department)
    return redirect(url_for('admin_panel.view_departments'))


@admin_panel.route('/delete-level/<int:level_id>')
@login_required
@has_role('admin')
def delete_level(level_id):
    '''delete deparmtment return to their category department'''
    level = mdl.Type.query.get(level_id)
    lgs.process_delete_level(level)
    return redirect(url_for('admin_panel.view_runned_levels'))

@admin_panel.route('/delete-programme/<int:programme_id>')
@login_required
@has_role('admin')
def delete_programme(programme_id):
    '''delete_programme return to their category level'''
    programme = mdl.Programme.query.get(programme_id)
    lgs.process_delete_programme(programme=programme)
    return redirect(url_for('admin_panel.create_level_programme',level_id=programme.type_id))

@admin_panel.route('/delete-postgrad-programme/<int:programme_id>')
@login_required
@has_role('admin')
def delete_postgrad_programme(programme_id):
    '''delete_programme return to their category level'''
    
    programme = mdl.Postgradprogramme.query.get(programme_id)
    lgs.process_delete_postgrad_programme(programme=programme)
    return redirect(request.url)

@admin_panel.route('/delete-subject/<int:subject_id>')
@login_required
@has_role('admin')
def delete_subject(subject_id):
    '''delete_subject return to their category programme'''
    subject = mdl.Subject.query.get(subject_id)
    lgs.process_delete_subject(subject)
    return redirect(url_for('admin_panel.create_subject'))

@admin_panel.route('/remove-require-subject',methods=['POST'])
@login_required
@has_role('admin')
def remove_require_subject():
    if request.method == 'POST':
        data = request.get_json()
        programme = mdl.Programme.query.get(int(data['programmeId']))
        subject = mdl.Subject.query.get(int(data['subjectId']))
    return redirect(url_for('admin_panel.load_require_subjects',programme_id=programme.id))
        
# ========================= admin edit information ===========================

@admin_panel.route('/edit-faculty/<int:faculty_id>',methods=['GET','POST'])
@login_required
@has_role('admin')
def edit_factiulty(faculty_id):
    '''edit the content of faculty'''
    faculty = mdl.Faculty.query.get(faculty_id)
    form = fms.FacultyForm(obj=faculty)
    if form.validate_on_submit():
        form.populate_obj(faculty)
        db.session.add(faculty)
        db.session.commit()
        return redirect(url_for('admin_panel.view_faculty'))
    return render_template('admin_site/edit_faculty.html',form=form,faculty=faculty)


@admin_panel.route('/edit-department/<int:department_id>',methods=['GET','POST'])
@login_required
@has_role('admin')
def edit_department(department_id):
    '''edit the content of department'''
    department = mdl.Department.query.get(department_id)
    form = fms.CreateDepartment(obj=department)
    if form.validate_on_submit():
        form.populate_obj(department)
        db.session.add(department)
        db.session.commit()
        return redirect(url_for('admin_panel.create_department',faculty_id=department.faculty.id))
    return render_template('admin_site/edit_department.html',form=form,department=department)


@admin_panel.route('/edit-level/<int:level_id>',methods=['GET','POST'])
@login_required
@has_role('admin')
def edit_level(level_id):
    '''edit the content of level'''
    level = mdl.Type.query.get(level_id)
    form = fms.CreateLevelTypeForm(obj=level)
    if form.validate_on_submit():
        form.populate_obj(level)
        db.session.add(level)
        db.session.commit()
        return redirect(url_for('admin_panel.create_level',department_id=level.department.id))
    return render_template('admin_site/edit_level.html',form=form,level=level)


@admin_panel.route('/edit-postgrad_programme/<int:postgrad_programme_id>',methods=['GET','POST'])
@login_required
@has_role('admin')
def edit_postgrad_programme(postgrad_programme_id):
    '''edit the content of postgrad_programme'''
    post_programme = mdl.Postgradprogramme.query.get(postgrad_programme_id)
    form = fms.AddPostGradProgrammeForm(obj=post_programme)
    if form.validate_on_submit():
        form.populate_obj(post_programme)
        db.session.add(post_programme)
        db.session.commit()
        return redirect(url_for('admin_panel.create_postgrad_level_programme',level_id=post_programme.type.id))
    return render_template('admin_site/edit_postgrad.html',form=form,post_programme=post_programme)


@admin_panel.route('/edit-undegrad_programme/<int:undegrad_programme_id>',methods=['GET','POST'])
@login_required
@has_role('admin')
def edit_undegrad_programme(undegrad_programme_id):
    '''edit the content of undegrad_programme'''
    under_programme = mdl.Programme.query.get(undegrad_programme_id)
    form = fms.AddProgrammeRunForm(obj=under_programme)
    if form.validate_on_submit():
        form.populate_obj(under_programme)
        db.session.add(under_programme)
        db.session.commit()
        return redirect(url_for('admin_panel.create_level_programme',level_id=under_programme.type.id))
    return render_template('admin_site/edit_undergrad.html',form=form,under_programme=under_programme)


@admin_panel.route('/edit-subject-department/<int:subject_id>',methods=['GET','POST'])
@login_required
@has_role('admin')
def edit_subject(subject_id):
    '''edit the content of subject'''
    subject = mdl.Subject.query.get(subject_id)
    form = fms.RequireAddmissonSubjectForm(obj=subject)
    if form.validate_on_submit():
        form.populate_obj(subject)
        db.session.add(subject)
        db.session.commit()
        return redirect(url_for('admin_panel.create_subject'))
    
    return render_template('admin_site/edit_subject.html',form=form,subject=subject)


@admin_panel.route('/edit-admission/<int:admission_id>')
@login_required
@has_role('admin')
def edit_admission(admission_id):
    '''edit the admission status of a student'''
    admitted_applicant = mdl.Admission.query.get(admission_id)
    db.session.delete(admitted_applicant)
    db.session.commit()
    # print('will delete the applicant from the admission')
    return redirect(url_for('admin_panel.view_all_admitted_students'))


# =============================== card and related========================================
@admin_panel.route('/get-applicant-data')
def get_applicant_data():
    applicants = appmdl.Applicant.query.filter_by(admission=None).all()
    header = ['applicant id','applicant name','applicant option','Grade/Class','Cutoff Point','admission status']
    applicant_list = []
    unlisted_applicant = []
    for applicant in applicants:
        if applicant.card is None:
            db.session.delete(applicant.contact)
            db.session.delete(applicant.education)
            db.session.delete(applicant.referee)
            db.session.delete(applicant.agreed)
            db.session.delete(applicant.choice)
            db.session.delete(applicant)
            db.session.commit()
        if applicant.agreed and applicant.agreed.agreed==True:
            if applicant.admission is None:
                if applicant.results.all():
                    try:
                        grade,cut = lgs.get_results(applicant, applicant.choice.first_choice)
                        if grade<= cut:
                            applicant_list.append([applicant.id,applicant,applicant.choice.first_choice,grade,cut,'short listed'])
                        else:
                            grade,cut = lgs.get_results(applicant, applicant.choice.second_choice)
                            if grade <= cut:
                                applicant_list.append([applicant.id,applicant,applicant.choice.second_choice,grade,cut,'short listed'])
                            else:
                                grade,cut = lgs.get_results(applicant, applicant.choice.third_choice)
                                if grade <= cut:
                                    applicant_list.append([applicant.id,applicant,applicant.choice.third_choice,grade,cut,'short listed'])
                                else:
                                    unlisted_applicant.append([applicant.id,applicant,applicant.choice.first_choice,grade,cut,'pending'])
                                    unlisted_applicant.append([applicant.id,applicant,applicant.choice.second_choice,grade,cut,'pending'])
                                    unlisted_applicant.append([applicant.id,applicant,applicant.choice.third_choice,grade,cut,'pending'])
                    except TypeError:
                        pass
                    # print(grade,cut)
                else:
                    result = {'pass':1,'third class lower':2,'third class':3,'second class lower':5,'second class upper':6,'first class':7}
                    grade,cut = lgs.get_results(applicant, applicant.choice.first_choice)
                    if result[cut] <= result[grade]:
                        applicant_list.append([applicant.id,applicant,applicant.choice.first_choice,applicant.education.graduated_class.upper(),cut.upper(),'short listed'])
                    else:
                        grade,cut = lgs.get_results(applicant, applicant.choice.second_choice)
                        if result[cut] <= result[grade]:
                            applicant_list.append([applicant.id,applicant,applicant.choice.second_choice,applicant.education.graduated_class.upper(),cut.upper(),'short listed'])
                        else:
                            grade,cut = lgs.get_results(applicant, applicant.choice.third_choice)
                            if result[grade] <= result[cut]:
                                applicant_list.append([applicant.id,applicant,applicant.choice.third_choice,applicant.education.graduated_class.upper(),cut.upper(),'short listed'])
                            else:
                                unlisted_applicant.append([applicant.id,applicant,applicant.choice.first_choice,applicant.education.graduated_class.upper(),cut.upper(),'pending'])
                                unlisted_applicant.append([applicant.id,applicant,applicant.choice.second_choice,applicant.education.graduated_class.upper(),cut.upper(),'pending'])
                                unlisted_applicant.append([applicant.id,applicant,applicant.choice.third_choice,applicant.education.graduated_class.upper(),cut.upper(),'pending'])

    file_path = os.path.join(current_app.root_path,'static')
    with open(file_path+'/applicants/applicants_data.csv','w',encoding='UTF8',newline='') as f:
        writer = csv.writer(f)
        # write header
        writer.writerow(header)
        # write data
        writer.writerows(applicant_list)
    # write the unshort listed applicants
    with open(file_path+'/applicants/unshort_listed.csv','w',encoding='UTF8',newline='') as unlisted:
        writer = csv.writer(unlisted)
        # writer header
        writer.writerow(header)
        # write data
        writer.writerows(unlisted_applicant)
    return jsonify({'results':'success'})


@admin_panel.route('/upload/admited',methods=['GET','POST'])
def upload_admited_applicants():
    '''upload the admited applicants'''
    if request.method == 'POST':
        data_value = {}
        file = request.get_array(field_name='file')
        for data in range(1,len(file)):
            datum = {}
            applicant = appmdl.Applicant.query.get(int(file[data][0]))
            if applicant.admission is None:
                datum['applicant id'] = file[data][0]
                datum['applicant name'] = file[data][1]
                datum['applicant option'] = file[data][2]
                if file[data][5] == 'admit' or file[data][5] =='admitted':
                    datum['admission status'] = 'admitted'
                    data_value[data] = datum
                else:
                    pass
            else:
                print(applicant,'has been admitted already')
        app=create_app()
        thread = Thread(target=lgs.process_admit_appicant,args=[data_value,app])
        thread.start()
    return redirect(url_for('admin_panel.view_all_admitted_students'))

# find applicant
@admin_panel.route('/find applicant/',methods=['POST'])
def find_applicant():
    'find applicant by pin'
    form = request.form.get('search_applicant')
    card = authmdl.Card.query.filter_by(pin=form).first()
    if card is not None:
        if card.applicant is not None:
            if card.applicant.choice is not None:
                first_ch_programme = mdl.Programme.query.filter_by(programme_name=card.applicant.choice.first_choice).first()
                second_ch_programme = mdl.Programme.query.filter_by(programme_name=card.applicant.choice.second_choice).first()
                third_ch_programme = mdl.Programme.query.filter_by(programme_name=card.applicant.choice.third_choice).first()
            else:
                first_ch_programme = mdl.Postgradprogramme.query.filter_by(programme_title=card.applicant.postgradchoice.first_choice).first()
                second_ch_programme = mdl.Postgradprogramme.query.filter_by(programme_title=card.applicant.postgradchoice.second_choice).first()
                third_ch_programme = mdl.Postgradprogramme.query.filter_by(programme_title=card.applicant.postgradchoice.third_choice).first()
        else:
            flash(f'{form} Does not have applicant.',category='info')
            return redirect(url_for('admin_panel.view_and_admin_applicants'))
    else:
        flash(f'{form} Does not exist.',category='info')
        return redirect(url_for('admin_panel.view_and_admin_applicants'))
    return render_template('admin_site/find_applicant.html',card=card
                           ,first_ch_programme=first_ch_programme,second_ch_programme=second_ch_programme,
                           third_ch_programme=third_ch_programme)

@admin_panel.route('/download/admitted')
def download_admitted_students():
    admitted_students = mdl.Admission.query.all()
    admitted_list = []
    for student in admitted_students:
        admitted_list.append([student.student_id,student.admission.applicant.surname,student.admission.applicant.first_name,student.admission.applicant.first_name,student.admission.applicant.last_name,student.admission.applicant.gender,student.admission.applicant.date_of_birth,student.admission.applicant.contact.contact_number,student.admission.applicant.contact.email,
                              student.programme_listed,student.level])
