from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length


class ReviewForm(FlaskForm):
    title = StringField('Title', 
                        validators=[DataRequired(), 
                                    Length(min=2, max=128)])
    text = TextAreaField('Review', 
                         validators=[DataRequired()])
    rating = SelectField('Rate', 
                          choices=[1,2,3,4,5,6,7,8,9,10])
    submit = SubmitField('Send review')