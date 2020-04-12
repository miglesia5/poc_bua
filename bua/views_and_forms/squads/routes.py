from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import func

from bua import db, bcrypt
from bua.models import Squad, Task, Todo
from bua.views_and_forms.squads.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from bua.views_and_forms.squads.utils import save_picture, send_reset_email


squads = Blueprint('squads', __name__)



@squads.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        squad = Squad(squadname=form.squadname.data, email=form.email.data, squad_members=form.squad_members.data, password=hashed_password)

        db.session.add(squad)
        db.session.commit()

        return redirect(url_for('squads.login'))
    return render_template('squad/register.html', title='Register', form=form)


@squads.route("/log", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        squad = Squad.query.filter_by(email=form.email.data).first()
        if squad and bcrypt.check_password_hash(squad.password, form.password.data):
            login_user(squad, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('squad/login.html', title='Login', form=form)


@squads.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@squads.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.squadname = form.squadname.data
        current_user.squad_members = form.squad_members.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('squads.account'))
    elif request.method == 'GET':
        form.squadname.data = current_user.squadname
        form.squad_members.data = current_user.squad_members
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('main/account.html', title='Account',
                           image_file=image_file, form=form)


def sum_fte(task_id):
    taskid = Task.query.get_or_404(task_id).escalar()
    task_ftes = (((int(taskid.volume) * int(taskid.avg_time) * 12) / 60) / 1975)
    #def my_filter(query):
     #   return query.filter_by(name='wendy')
    #wendy = my_filter(session.query(User)).one()


@squads.route("/squad/<squadname>")



def squad_detail(squadname):

    squad = Squad.query.filter_by(squadname=squadname).first_or_404()
    tasks = Task.query.filter_by(author=squad)\
        .order_by(Task.date_posted.desc())

    activity_count = Task.query.filter_by(author=squad).count()

    vol_sum = db.session.query(func.sum(Task.volume)).filter_by(author=squad).scalar()/activity_count
    time_sum = db.session.query(func.sum(Task.avg_time)).filter_by(author=squad).scalar()
    squad_ftes = (((((vol_sum) * (time_sum)) * 12) / 60) / 1975)

    standard_activity_count = Task.query.filter_by(author=squad).filter(Task.pain_point=="Standard").count()

    standard_vol = db.session.query(func.sum(Task.volume)).filter_by(author=squad).filter(Task.pain_point=="Standard").scalar()/standard_activity_count
    standard_time_sum = db.session.query(func.sum(Task.avg_time)).filter_by(author=squad).filter(Task.pain_point=="Standard").scalar()
    standard_ftes = (((((standard_vol) * (standard_time_sum)) * 12) / 60) / 1975)


    return render_template('tasks/squad_details.html',
                           tasks=tasks, squad=squad,
                           activity_count=activity_count,
                           squad_ftes=squad_ftes,
                           standard_ftes=standard_ftes,
                           )


@squads.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        squad = Squad.query.filter_by(email=form.email.data).first()
        send_reset_email(squad)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('squads.login'))
    return render_template('squad/reset_request.html', title='Reset Password', form=form)


@squads.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    squad = Squad.verify_reset_token(token)
    if squad is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('squads.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        squad.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('squads.login'))
        return render_template('squad/reset_token.html', title='Reset Password', form=form)
