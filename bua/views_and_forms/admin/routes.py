from datetime import datetime, timedelta

from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from bua import db, bcrypt
from bua.models import Squad, Task
from bua.views_and_forms.squads.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from bua.views_and_forms.squads.utils import save_picture, send_reset_email


admin = Blueprint('admin', __name__)


@admin.route('/admin_view_users')
@login_required
def admin_view_users():
    if current_user.role != 'admin':
        abort(403)
    else:
        users = Squad.query.order_by(Squad.id).all()
        return render_template('admin_view_users.html', users=users)


@admin.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        abort(403)
    else:
        users = Squad.query.order_by(Squad.id).all()
        kpi_mau = Squad.query.filter(Squad.last_logged_in > (datetime.today() - timedelta(days=30))).count()
        kpi_total_confirmed = Squad.query.filter_by(email_confirmed=True).count()
        kpi_mau_percentage = (100 / kpi_total_confirmed) * kpi_mau
        return render_template('admin_dashboard.html', users=users, kpi_mau=kpi_mau, kpi_total_confirmed=kpi_total_confirmed, kpi_mau_percentage=kpi_mau_percentage)
