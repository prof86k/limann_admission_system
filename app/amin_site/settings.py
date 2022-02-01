from flask import render_template,flash,redirect,request,jsonify
from flask.helpers import flash, url_for
import secrets
import os
from PIL import Image
from flask import current_app
from . import admin_panel
from . import forms as fms
from .. import models as mdl 
from .. import db
from ..auth.decorators import has_role
from ..auth import models as authmdl
from ..auth import forms as authfms
from flask_login import login_required
from . import logics as lgs

def save_signature(form_passport_pic):
    random_image_name = secrets.token_hex(8)
    _, file_ext =os.path.splitext(form_passport_pic.filename)
    passport_picname = random_image_name+file_ext
    image_pic = os.path.join(current_app.root_path,'static/images/admin_img',passport_picname)
    
    # resize the image
    output_size = (125,125)
    image_size = Image.open(form_passport_pic)
    image_size.thumbnail(output_size)
    image_size.save(image_pic)
    # return the image filename
    return passport_picname

@admin_panel.route('/add-settings')
@login_required
@has_role('admin')
def add_settings():
    '''add settings to the application'''
    
    return render_template('settings/settings.html')

@admin_panel.route('/create/user',methods=['GET','POST'])
@login_required
@has_role('admin')
def create_user():
    users = authmdl.Admin.query.all()
    form = authfms.AdminCreationForm()
    if form.validate_on_submit():
        lgs.process_user_creation(form)
        return redirect(request.url)
    return render_template('settings/create_user.html',form=form,users=users)

@admin_panel.route('/edit-user/<int:user_id>',methods=['GET','POST'])
@login_required
@has_role('admin')
def edit_user_info(user_id):
    user = authmdl.Admin.query.get_or_404(user_id)
    form = authfms.AdminCreationForm(obj=user)
    if form.validate_on_submit():
        user.set_password_to_hash(form.password.data)
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin_panel.create_user'))
    return render_template('settings/edit_user.html',form=form,user=user)

@admin_panel.route('/delete-user/<int:user_id>')
@has_role('admin')
def delete_user(user_id):
    user = authmdl.Admin.query.get_or_404(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f'User couldn\'t be deleted due to {e}')
    return redirect(url_for('admin_panel.create_user'))

@admin_panel.route('/set-card/state',methods=['GET','POST'])
@login_required
@has_role('admin')
def set_card():
    '''define the nature of the card for application'''
    cards_set = authmdl.Cardstate.query.all()
    form = authfms.CardStateForm()
    if form.validate_on_submit():
        lgs.process_set_cards(form)
        return redirect(request.url)
    return render_template('settings/set_card.html',form=form,cards=cards_set)

@admin_panel.route('/view-purchased-cards')
@login_required
@has_role('admin')
def view_cards():
    page = request.args.get('page',1,int)
    cards = authmdl.Card.query.order_by(authmdl.Card.date_bought.desc()).paginate(page,15)
    return render_template('auth/purchased_card_info.html',cards=cards)

@admin_panel.route('/delete-purchased-cards/<int:card_id>/<int:buy_id>')
@login_required
@has_role('admin')
def delete_card(card_id,buy_id):
    card = authmdl.Card.query.get(card_id)
    buy = authmdl.Buy.query.get(buy_id)
    try:
        db.session.delete(card)
        db.session.delete(buy)
        db.session.commit()
        print('deleted')
    except Exception as e:
        print(e)
        db.session.rollback()
    return redirect(url_for('admin_panel.view_cards'))
        
@admin_panel.route('/edit-card-settings/<int:card_id>',methods=['GET','POST'])
@login_required
@has_role('admin')
def edit_card_settings(card_id):
    '''edit the card information'''
    card = authmdl.Cardstate.query.get_or_404(card_id)
    form = authfms.CardStateForm(obj=card)
    if form.validate_on_submit():
        form.populate_obj(card)
        db.session.add(card)
        db.session.commit()
        return redirect(url_for('admin_panel.set_card'))
    return render_template('settings/edit_card_settings.html',form=form,card=card)

@admin_panel.route('/delete-card/settings/<int:card_id>')
@login_required
@has_role('admin')
def delete_card_settings(card_id):
    '''delete the card'''
    card = authmdl.Cardstate.query.get_or_404(card_id)
    try:
        db.session.delete(card)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f'operation failed due to {e}')
    return redirect(url_for('admin_panel.set_card'))

@admin_panel.route('/add-dues',methods=['GET','POST'])
def add_sr_dues():
    form = fms.SrcForm()
    dues = mdl.Srcdues.query.order_by(mdl.Srcdues.date_added.desc()).all()

    if form.validate_on_submit():
        amount = form.amount.data
        dues = mdl.Srcdues(amount=amount)
        try:
            db.session.add(dues)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f'Dues Couldn\'t be saved due to {e}')
        return redirect(request.url)
    return render_template('settings/add_dues.html',form=form,dues=dues)

@admin_panel.route('/edit-dues/<int:dues_id>',methods=['GET','POST'])
def edit_dues(dues_id):
    dues = mdl.Srcdues.query.get(dues_id)
    if dues is not None:
        form = fms.SrcForm(obj=dues)
        if form.validate_on_submit():
            form.populate_obj(dues)
            db.session.add(dues)
            db.session.commit()
            return redirect(url_for('admin_panel.add_sr_dues'))
    return render_template('settings/edit_dues.html',dues=dues,form=form)

@admin_panel.route('/subjects-4-grades',methods=['GET','POST'])
def subjects_for_grades():
    form = fms.Subjects4GradesForm()
    subjects = mdl.Coreforgrades.query.all()
    if form.validate_on_submit():
        subject_name = form.subject_name.data
        subject_status = form.subject_status.data
        min_grade = form.min_grade.data
        subjects = mdl.Coreforgrades(subject_name=str(subject_name),subject_status=subject_status,min_grade=min_grade)
        try:
            db.session.add(subjects)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f'subject could not be added due to {e}')
        return redirect(request.url)
    return render_template('settings/subjects_for_grades.html',subjects=subjects,form =form)

@admin_panel.route('/edit-subject-4/<int:subject_id>',methods=['GET','POST'])
def edit_subjects_4(subject_id):
    subject = mdl.Coreforgrades.query.get(subject_id)
    if subject is not None:
        form = fms.Subjects4GradesForm(obj=subject)
        if form.validate_on_submit():
            form.populate_obj(subject)
            db.session.add(subject)
            db.session.commit()
            return redirect(url_for('admin_panel.subjects_for_grades'))
    return render_template('settings/edit_subject.html',form=form)

@admin_panel.route('/get-subject-4/<int:subject_id>')
def get_subjects_4(subject_id):
    subject = mdl.Coreforgrades.query.get(subject_id)
    results = {}
    if subject is not None:
        results['subject_name'] = subject.subject_name
        results['subject_status'] = subject.subject_status
        results['min_grade'] = subject.min_grade
        return jsonify({'results':results})
    
@admin_panel.route('/subject-number',methods=['GET','POST'])
def subject_number_for_grade():
    form = fms.SubjectsLengthForm()
    if form.validate_on_submit():
        number = form.number.data
        number = mdl.Lengthofgradingsubjects(number=number)
        try:
            db.session.add(number)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print('subjects number could not be set due to {e}')
        return redirect(url_for('admin_panel.add_settings'))
    return render_template('settings/subject_number.html',form=form)

@admin_panel.route('/edit-subject-number/<int:number_id>',methods=['GET','POST'])
def edit_subject_number(number_id):
    number = mdl.Lengthofgradingsubjects.query.get(number_id)
    form = fms.SubjectsLengthForm(obj=number)
    if form.validate_on_submit():
        form.populate_obj(number)
        db.session.add(number)
        db.session.commit()
        return redirect(url_for('admin_panel.subject_number_for_grade'))
    return render_template('settings/edit_subject_number.html',form=form,number=number)

@admin_panel.route('/add-registrar',methods=['GET','POST'])
def add_registrar():
    form = fms.RegistrarForm()
    registrar = authmdl.Registrar.query.all()
    if form.validate_on_submit():
        registrar_name = form.registrar_name.data
        if form.registrar_signature.data:
            registrar_signature = save_signature(form.registrar_signature.data)
            registrar = authmdl.Registrar(registrar_name=registrar_name,registrar_signature=registrar_signature)
            try:
                db.session.add(registrar)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f'Registrar info unable to add due to {e}')
            return redirect(request.url)
    return render_template('settings/registrar.html',form=form,registrar=registrar)
    
@admin_panel.route('/edit-registrar/<int:registrar_id>',methods=['GET','POST'])
def edit_registrar(registrar_id):
    registrar = authmdl.Registrar.query.get(registrar_id)
    form = fms.RegistrarForm(obj=registrar)
    if form.validate_on_submit():
        form.populate_obj(registrar)
        if form.registrar_signature.data:
            registrar_sign = save_signature(form.registrar_signature.data)
            registrar.registrar_signature = registrar_sign
            try:
                db.session.add(registrar)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f'from admin setting in edit registrar has {e}')
        return redirect(url_for('admin_panel.add_registrar'))
    return render_template('settings/edit_registrar.html',form=form,registrar=registrar)

@admin_panel.route('/add-bank',methods=['GET','POST'])
def add_bank():
    form = fms.BankForm()
    bank = authmdl.Bank.query.all()
    if form.validate_on_submit():
        bank_name = form.bank_name.data
        transaction_mode = form.transaction_mode.data
        bank = authmdl.Bank(bank_name=bank_name,transaction_mode=transaction_mode)
        try:
            db.session.add(bank)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f'bank info unable to add due to {e}')
        return redirect(request.url)
    
    return render_template('settings/bank.html',form=form,bank=bank)
    
@admin_panel.route('/edit-bank/<int:bank_id>',methods=['GET','POST'])
def edit_bank(bank_id):
    bank = authmdl.Bank.query.get(bank_id)
    form = fms.BankForm(obj=bank)
    if form.validate_on_submit():
        form.populate_obj(bank)
        db.session.add(bank)
        db.session.commit()
        return redirect(url_for('admin_panel.add_bank'))
    
    return render_template('settings/edit_bank.html',form=form,bank=bank)

@admin_panel.route('/delete-bank/settings/<int:bank_id>')
@login_required
@has_role('admin')
def delete_bank_settings(bank_id):
    '''delete the bank'''
    bank = authmdl.Bank.query.get_or_404(bank_id)
    try:
        db.session.delete(bank)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f' could not delete bank operation failed due to {e}')
    return redirect(url_for('admin_panel.add_bank'))

@admin_panel.route('/delete-subject/settings/<int:subject_id>')
@login_required
@has_role('admin')
def delete_subject_4_settings(subject_id):
    '''delete the bank'''
    bank = mdl.Coreforgrades.query.get_or_404(subject_id)
    try:
        db.session.delete(subject_id)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f' could not delete bank operation failed due to {e}')
    return redirect(url_for('admin_panel.subjects_for_grades'))