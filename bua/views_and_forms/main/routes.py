from flask_login import current_user
from sqlalchemy import func

from bua import db
from bua.models import Task, Squad, Todo
from flask import Flask, render_template, request, redirect, url_for, Blueprint, abort, flash

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    squads = Squad.query.order_by(Squad.id.desc())
    return render_template('main/home.html', squads=squads)


@main.route("/about")
def about():
    return render_template('main/about.html', title='About')



@main.route("/")
@main.route("/your_squad")
def all_squad():


    activity_count = db.session.query(Task.activity).count()

    members = (db.session.query(Squad).filter(Squad.id).first())

    vol_sum = db.session.query(func.sum(Task.volume)).scalar()/activity_count
    time_sum = db.session.query(func.sum(Task.avg_time)).scalar()
    ftes = (((((vol_sum) * (time_sum))*12)/60)/1975)

    waste_time = db.session.query(func.sum(Task.pain_point_time)).scalar()
    w_t_hrs_per_Month = (((waste_time)*(vol_sum))/60)

    tasks = Task.query.order_by(Task.date_posted.desc())

    affected_volume = db.session.query(func.sum(Todo.affected_volume)).scalar()
    saving_sum = db.session.query(func.sum(Todo.saving)).scalar()
    saving_ftes = (((((saving_sum) * (affected_volume)) * 12) / 60) / 1975)

    squad_members = db.session.query(func.sum(Squad.squad_members)).scalar()
    capacity_open = (squad_members-ftes)


    return render_template('main/all_squad.html',
                           tasks=tasks,
                           squad_members=squad_members,


                           activity_count=activity_count,
                           time_sum=time_sum, vol_sum=vol_sum,
                           ftes=ftes, waste_time=waste_time,
                           w_t_hrs_per_Month=w_t_hrs_per_Month,
                           saving_ftes=saving_ftes,
                           capacity_open=capacity_open
                           )

@main.route("/task/<int:task_id>")
def task(task_id):
        task = Task.query.get_or_404(task_id)

        tftes = (((int(task.volume) * int(task.avg_time)*12)/60)/1975)


        return render_template('main/all_squad.html', task=task, tftes=tftes)



