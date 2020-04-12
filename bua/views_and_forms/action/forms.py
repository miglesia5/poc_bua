from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, validators
from wtforms.validators import DataRequired, Length


class TodoForm(FlaskForm):
    todoitem = TextAreaField('Goal', validators=[DataRequired()])
    saving = StringField('Estimated Savings', validators=[DataRequired(), Length(min=1, max=5)])
    complete = BooleanField('Is the Activity Complete?', [validators.InputRequired()])
    submit = SubmitField('Add Action')
