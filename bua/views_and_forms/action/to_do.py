from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from sqlalchemy import func

from bua import db
from bua.models import Todo, Task
from bua.views_and_forms.action.forms import TodoForm

todo = Blueprint('todo', __name__)


@todo.route("/todo", methods=['GET', 'POST'])
@login_required
def to_do():
    all = Todo.query.all

    incomplete = Todo.query.filter_by(complete=False).all()
    complete = Todo.query.filter_by(complete=True).all()

    goal_count = db.session.query(Todo.goal).count()
    incomplete_count = Todo.query.filter_by(complete=False).count()
    complete_count = Todo.query.filter_by(complete=True).count()

    affected_volume = db.session.query(func.sum(Todo.affected_volume)).scalar()
    saving_sum = db.session.query(func.sum(Todo.saving)).scalar()
    saving_ftes= (((((saving_sum)*(affected_volume))*12)/60)/1975)

    return render_template('tasks/to_do.html', incomplete=incomplete, complete=complete,
                           goal_count=goal_count, incomplete_count=incomplete_count,
                           complete_count=complete_count, saving_sum=saving_sum,
                           saving_ftes=saving_ftes, all=all)


@todo.route('/add', methods=['POST'])
@login_required
def add():
    todo = Todo(goal=request.form['todoitem'],
                saving=request.form['savingitem'],
                affected_volume=request.form['affected_volume'],
                complete=False)
    db.session.add(todo)
    db.session.commit()
    flash('Your Goal has been created!', 'info')
    return redirect(url_for('todo.to_do'))


@todo.route('/complete/<id>')
@login_required
def complete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()
    flash('Your Goal has been Completed!', 'success')
    return redirect(url_for('todo.to_do'))


@todo.route('/incomplete/<id>')
@login_required
def incomplete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = False
    db.session.commit()

    flash('Your Goal has been set as Incomplete!', 'secondary')
    return redirect(url_for('todo.to_do'))


# ####to=do #### Make the delete function work

@todo.route('/delete/<int:id>')
def delete_goal(id):
    goal = Todo.query.get(id)
    if not goal:
        return redirect(url_for('todo.to_do'))

    db.session.delete(goal)
    db.session.commit()

    flash('Your Goal has been deleted!', 'danger')
    return redirect(url_for('todo.to_do'))

