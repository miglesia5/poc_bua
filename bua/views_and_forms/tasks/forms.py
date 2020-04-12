from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class TaskForm(FlaskForm):

    activity = StringField('Activity', validators=[DataRequired()])
    tool = StringField('Tool', validators=[DataRequired()])
    product = TextAreaField('Product', validators=[DataRequired()])
    summary = TextAreaField('Summary', validators=[DataRequired()])

    avg_time = StringField('Min. per Transaction', validators=[DataRequired(), Length(min=1, max=5)])
    volume = StringField('Volume per Month', validators=[DataRequired(), Length(min=1, max=5)])

    pain_point = TextAreaField('Feedback', validators=[DataRequired()])
    pain_point_time = StringField('Waste Time per Transaction in Minutes', validators=[DataRequired(),Length(min=1, max=5)])

    submit = SubmitField('Submit')
