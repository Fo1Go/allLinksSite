from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (StringField, EmailField, PasswordField, SubmitField, 
                     BooleanField, SearchField, SelectField)
from wtforms.validators import (DataRequired, Length, 
                                ValidationError, EqualTo, Email)
from links.models import User, Links, ROLES
from flask_login import current_user
from re import match


class RegisterForm(FlaskForm):
    username = StringField('Username', 
                        validators=[DataRequired(), 
                                    Length(min=2, max=40)])
    email = EmailField('Email', 
                        validators=[DataRequired(), 
                                    Email()])
    password = PasswordField('Password', 
                        validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', 
                        validators=[DataRequired(), 
                                    EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is taken. \
                                  Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(username=email.data).first()
        if user:
            raise ValidationError('This email is taken. \
                                  Please choose a different one.')


class LoginForm(FlaskForm):
    email = EmailField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                        validators=[DataRequired()])
    remember = BooleanField('Remeber me')
    submit = SubmitField('Log in')


class ResetPasswordForm(FlaskForm):
    email = EmailField('Email', 
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')


class CreateNewPasswordForm(FlaskForm):
    password = PasswordField('Password', 
                        validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', 
                        validators=[DataRequired(), 
                                    EqualTo('password')])
    submit = SubmitField('Create New Password')


class UpdateProfileForm(FlaskForm):
    username = StringField('Username', 
                        validators=[Length(min=2, max=40)])
    email = EmailField('Email', 
                        validators=[Email()])
    password = PasswordField('Old password', 
                        validators=[])
    new_password = PasswordField('Password', 
                        validators=[])
    new_confirm_password = PasswordField('Confirm password', 
                        validators=[EqualTo('new_password')])
    picture = FileField('Update picture', 
                       validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if current_user.username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is taken. \
                                      Please choose a different one.')
    
    def validate_email(self, email):
        if current_user.username != email.data:
            user = User.query.filter_by(username=email.data).first()
            if user:
                raise ValidationError('This email is taken. \
                                      Please choose a different one.')
            

class LinkCreateForm(FlaskForm):
    name = StringField('Link name', 
                       validators=[Length(min=2, max=128), DataRequired()])
    link = StringField('URI', validators=[DataRequired()])
    submit = SubmitField('Add link')
    
    def validate_name(self, name):
        links = Links.query.filter_by(owner_id=current_user.id).all()
        if links:
            for l in links:
                if name.data == l.name:
                    raise ValidationError('You cannot have 2 same links')
    
    def validate_link(self, link):
        pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
        if not match(pattern, link.data):
            raise ValidationError('Not valid link')
                

class LinkEditForm(FlaskForm):
    link = StringField('URI', validators=[DataRequired()])
    edit_submit = SubmitField('Edit link')
    delete_submit = SubmitField('Delete link')
                
    def validate_link(self, link):
        if self.edit_submit.data:
            pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
            if not match(pattern, link.data):
                raise ValidationError('Not valid link')
            

class SearchUserForm(FlaskForm):
    search = SearchField('Username')
    submit = SubmitField('Search')


class EditRoleForm(FlaskForm):
    role = SelectField('Roles', 
                          choices=list(ROLES.keys()))
    master_key = PasswordField('Master key:', 
                        validators=[DataRequired()])
    submit = SubmitField('Add role')