from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
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


class AddNewsForm(FlaskForm):
    title = StringField('Title', 
                        validators=[DataRequired(), 
                                    Length(min=1, max=256)])
    text = StringField('Text', 
                        validators=[DataRequired()])
    img = FileField('Preview picture', 
                       validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add article')
    
    
    def __repr__(self):
        return f'News("{self.title}", "{self.date}")'
    

class EditNewsForm(FlaskForm):
    title = StringField('Title', 
                        validators=[DataRequired(), 
                                    Length(min=1, max=256)])
    text = StringField('Text', 
                        validators=[DataRequired()])
    img = FileField('Preview picture', 
                       validators=[FileAllowed(['jpg', 'png'])])
    edit_submit = SubmitField('Edit news')
    delete_submit = SubmitField('Delete article')


    def __repr__(self):
        return f'News("{self.title}", "{self.date}")'