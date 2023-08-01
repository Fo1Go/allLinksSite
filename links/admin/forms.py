from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length
from links.models import ROLES


class EditRoleForm(FlaskForm):
    username = StringField('Username', 
                        validators=[DataRequired(), 
                                    Length(min=2, max=128)])
    role = SelectField('Roles', 
                          choices=list(ROLES.keys()))
    master_key = PasswordField('Master key:', 
                        validators=[DataRequired()])
    submit = SubmitField('Add role')