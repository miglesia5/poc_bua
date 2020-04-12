from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from sqlalchemy import func

from bua import db
from bua.models import Task
from bua.views_and_forms.tasks.forms import TaskForm

tasks = Blueprint('tasks', __name__)


@tasks.route("/task/new", methods=['GET', 'POST'])
@login_required
def new_task():
    form = TaskForm()
    if form.validate_on_submit():
        activity = Task(
                        activity=form.activity.data,
                        tool=form.tool.data,
                        product=form.product.data,
                        summary=form.summary.data,

                        avg_time=form.avg_time.data,
                        volume=form.volume.data,

                        pain_point=form.pain_point.data,
                        pain_point_time=form.pain_point_time.data,

                        author=current_user)
        db.session.add(activity)
        db.session.commit()
        flash('Your activity has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('tasks/create_task.html', title='New Task',
                           form=form, legend='New Task')


@tasks.route("/task/<int:task_id>")
def task(task_id):
        task = Task.query.get_or_404(task_id)


        ftes = (((int(task.volume) * int(task.avg_time)*12)/60)/1975)


        waste_time = (task.pain_point_time)
        return render_template('tasks/task.html', task=task, ftes=ftes, waste_time=waste_time)


#movies[(movies.duration=>200) & (movies.genre == 'Drama')]
#movies[(movies.duration=>200) | (movies.genre == 'Drama')]
#movies[movies.genre.isin(["crime", 'drama', 'action'])]
#

@tasks.route("/task/<int:task_id>/update", methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        abort(403)
    form = TaskForm()
    if form.validate_on_submit():

        task.activity = form.activity.data
        task.tool = form.tool.data
        task.product = form.product.data
        task.summary = form.summary.data

        task.avg_time = form.avg_time.data
        task.volume = form.volume.data

        task.pain_point = form.pain_point.data
        task.pain_point_time = form.pain_point_time.data

        author = current_user
        db.session.commit()
        flash('Your task has been updated!', 'success')
        return redirect(url_for('main.home', task_id=task.id))
    elif request.method == 'GET':

        form.activity.data = task.activity
        form.tool.data = task.tool
        form.product.data = task.product
        form.summary.data = task.summary

        form.avg_time.data = task.avg_time
        form.volume.data = task.volume

        form.pain_point.data = task.pain_point
        form.pain_point_time.data = task.pain_point_time

        author = current_user
    return render_template('tasks/create_task.html', title='Update Post',
                           form=form, legend='Update Post')


@tasks.route("/task/<int:task_id>/delete", methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    db.session.delete(task)
    db.session.commit()
    flash('Your task has been deleted!', 'danger')
    return redirect(url_for('main.home'))
