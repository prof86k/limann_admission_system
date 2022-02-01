from flask import render_template, redirect, request
from flask import url_for, jsonify
from flask_login import logout_user, current_user

from . import auth
from . import forms as fms
from . import logics as lgs
from .models import Cardstate
from ..amin_site import forms as adfms


@auth.route('/create account', methods=['GET', 'POST'])
def buy_card():
    card_state = Cardstate.query.all()
    form = fms.BuyCardForm()
    if form.validate_on_submit():
        try:
            cardnumber, pin, amount, types, mode, name,sellername = lgs.process_buy_form(form_data=form)
            return redirect(
                url_for('auth.print_card', amount=amount, card=cardnumber, pin=pin, types=types, mode=mode, name=name,sellername=sellername))
        except Exception as e:
            print(f'Card unable to buy! operation is not applicable {e}')
            pass
    return render_template('auth/buy_card.html', form=form, card_state=card_state)


@auth.route('/print-card/<card>/<pin>/<amount>/<types>/<mode>/<name>/<sellername>')
def print_card(card, pin, amount, types, mode, name,sellername):
    return render_template('auth/print_cards.html', types=types, mode=mode, name=name, card=card, pin=pin,
                           amount=amount,sellername=sellername)


@auth.route('/get-card/<int:card_id>')
def get_card_info(card_id):
    card = Cardstate.query.get(card_id)
    card_state = {}
    card_state['application_type'] = card.card_type
    card_state['amount'] = card.amount
    card_state['state'] = card.state
    return jsonify({'results': card_state})


@auth.route('/', methods=['GET', 'POST'])
def apply():
    form = fms.CardApplyForm()
    if form.validate_on_submit():
        card_id = lgs.process_apply(form)
        if card_id is not None:
            return redirect(url_for('application.check_admission_status', card_id=card_id))
        return redirect(request.url)
    return render_template('auth/apply.html', form=form)


@auth.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    '''administrator login view'''
    form = adfms.AdminLoginForm()
    if form.validate_on_submit():
        if lgs.process_admin_login(form) == True:
            if current_user.has_role('admin'):
                return redirect(request.args.get('next') or url_for('admin_panel.admin_dashboard'))
            else:
                return redirect(url_for('auth.buy_card'))
    return render_template('auth/admin_login.html', form=form)


@auth.route('/logout')
def log_out_user():
    logout_user()
    return redirect(url_for('auth.admin_login'))
