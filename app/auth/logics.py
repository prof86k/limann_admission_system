from flask.helpers import flash, url_for
from . import models as mdl
from .. import db
from flask import flash
from flask_login import login_user, current_user

'''the logics of the application goes here'''
def process_buy_form(form_data):
    '''process the buy card data in to database'''
    fullname = form_data.applicants_full_name.data
    email    = form_data.applicants_email.data
    contact  = form_data.applicants_contact.data
    appl_type = form_data.application_type.data
    amount    = form_data.amount.data
    payment_mode = form_data.payment_mode.data
    buy_card = mdl.Buy(applicants_full_name=fullname,applicants_email=email,
                       applicants_contact=contact,application_type=str(appl_type),
                       payment_mode=payment_mode,amount=amount
                       )
    card_settings = mdl.Cardstate.query.filter_by(card_type=str(appl_type)).first()
    try:
        if card_settings is not None:
            if card_settings.state == 'paid':
                if current_user.has_role('card_seller'):
                    buy_card.admin_id = current_user.id
                    db.session.add(buy_card)
                    db.session.commit()
                    card = mdl.Card.query.count()
                    # save the data and generate the serial and pin to populate into the Card table
                    card_serial_number = buy_card.generate_serial_pin().get('serial number')+str(card)
                    card_pin_number    = buy_card.generate_serial_pin().get('pin')+str(card)
                    bought_card_info   = mdl.Card(serial_number = card_serial_number,pin=card_pin_number)
                    bought_card_info.buy_id = buy_card.id
                    bought_card_info.pin
                    db.session.add(bought_card_info)
                    db.session.commit()
                    return card_serial_number,card_pin_number,buy_card.amount,card_settings,card_settings.state,buy_card.applicants_full_name,buy_card.admin.username
            elif card_settings.state == 'free':
                db.session.add(buy_card)
                db.session.commit()
                card = mdl.Card.query.count()
                # save the data and generate the serial and pin to populate into the Card table
                card_serial_number = buy_card.generate_serial_pin().get('serial number')+str(card)
                card_pin_number    = buy_card.generate_serial_pin().get('pin')+str(card)
                bought_card_info   = mdl.Card(serial_number = card_serial_number,pin=card_pin_number)
                bought_card_info.buy_id = buy_card.id
                bought_card_info.pin
                db.session.add(bought_card_info)
                db.session.commit()
                return card_serial_number,card_pin_number,buy_card.amount,card_settings,card_settings.state,buy_card.applicants_full_name,'None'
        else:
            flash(f'Applications for programmes are not open yet.',category='info')
            return
    except Exception as e:
        db.session.rollback()
        print(f'operation failed due {e}')
        flash(f'Unable to save and generate serial and pin. please Try again',category='danger')
        flash(f'You Could not generate serial and pin NOTE THAT ACCOUNT CREATION IS NOT FREE PLEASE CONTACT SALES AGENT or THE ADMINISTRATOR',category='info')
        return



def process_apply(form_data):
    '''process the card login data'''
    card = mdl.Card.query.filter_by(serial_number=form_data.serial.data).first()
    if card is not None and card.is_active():
        if card.pin==form_data.pin.data :
            return card.pin
        else:
            flash(f'This Card Pin is incorrect',category='danger')
    else:
        return flash(f'Invalid credential for {form_data.serial.data} check that card serial does not expire',category='danger')
    
def process_admin_login(form) -> bool:
    '''check if the user is admin'''
    admin_username = form.username.data
    password = form.password.data
    admin_user = mdl.Admin.query.filter_by(username=admin_username).first()
    if admin_user is not None:
        if admin_user.check_hashed_password(password):
            login_user(admin_user)
            return True
        else:
            flash(f'password provided is incorrect',category='danger')
    else:
        flash(f'Username Does Not Exist',category='danger') 
        return False
