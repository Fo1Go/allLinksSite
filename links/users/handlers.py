from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from links import bcrypt, db
from links.users.forms import (RegisterForm, LoginForm, UpdateProfileForm, 
                               LinkCreateForm, LinkEditForm, ResetPasswordForm, 
                               CreateNewPasswordForm, EditRoleForm )
from links.models import User, Links, Roles, Reviews, Friends, ROLES
from links.users.utils import (save_picture, get_qrcode, send_mail, 
                               generate_token, validate_token)


users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.profile'))
    form = RegisterForm()
    title = 'Register now'
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)\
                        .decode('utf-8')
        user = User(username=form.username.data, 
                    email=form.email.data, 
                    password=hash_password)
        db.session.add(user)
        db.session.commit()
        user_role = Roles(user_id=user.id, 
                          user_role=ROLES['user'])
        db.session.add(user_role)
        db.session.commit()
        flash('You have been created account. Now you can login.', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/register.html', form=form, title=title)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.profile'))
    title = 'Login now'
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)  
                else: 
                    redirect(url_for('users.profile'))
        flash('Not valid data. Try again.', 'warning')
    return render_template('users/login.html', form=form, title=title)
    

@users.route('/password/reset', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user: 
            token = generate_token(user)
            send_mail(token=token, email=form.email.data)
            flash('An email has been sent with instructions \to reset your password.', 
                'info')
            return redirect(url_for('main.home'))
        flash('No user with this email', 'danger')

    title = 'Reset password'
    return render_template('users/reset_password.html', form=form, title=title)


@users.route('/password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = CreateNewPasswordForm() 
    if form.validate_on_submit():
        user_id = validate_token(token=token)
        if user_id:
            user = User.query.get(user_id)   
            hash_password = bcrypt.generate_password_hash(form.password.data)\
                            .decode('utf-8')
            user.password = hash_password
            db.session.commit()
            flash('Your password has been changed.', 'info')
            return redirect('users.login')
        flash('Not valid token', 'danger')
    title = 'Create new password'
    return render_template('users/create_password.html', form=form, title=title)


@users.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('main.home'))


@users.route('/profile', methods=['GET', 'POST']) 
@login_required
def profile():
    form = LinkCreateForm()
    if form.validate_on_submit():
        link = Links(name=form.name.data, 
                     link=form.link.data, 
                     owner_id=current_user.id)
        db.session.add(link)
        db.session.commit()
        flash('You have been add new link', 'success')
        return redirect(url_for('users.profile'))
    title = 'Profile'
    links = Links.query.filter_by(owner_id=current_user.id).all()
    image_file = url_for('static', filename=f'profile_pictures/{current_user.image_file}')
    qrcode = get_qrcode(current_user.username)
    return render_template('users/profile.html', 
                           title=title, 
                           image_file=image_file, 
                           form=form, 
                           links=links, 
                           qrcode=qrcode)


@users.route('/profile/update', methods=['GET', 'POST'])
@login_required
def profile_update():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        if form.username.data:
            current_user.username = form.username.data
        if form.email.data:
            current_user.email = form.email.data
        if form.password.data and form.new_confirm_password.data and form.new_password.data:
            if bcrypt.check_password_hash(current_user.password, form.password.data):
                if not bcrypt.check_password_hash(current_user.password, form.new_password.data):
                    hashed_password = bcrypt.generate_password_hash(form.new_password.data)\
                        .decode('UTF-8')
                    current_user.password = hashed_password
                    flash('Your password has been updated!', 'success')
                else:
                    flash('You cant set same password!', 'danger')
            else:
                flash('Your password not equal your current password!', 'danger')
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    title = 'Profile Update'
    image_file = url_for('static', filename=f'profile_pictures/{current_user.image_file}')
    return render_template('users/profile_update.html', 
                           form=form, 
                           title=title, 
                           image_file=image_file)


@users.route('/profile/links/<link_name>', methods=['GET', 'POST'])
@login_required
def edit_link(link_name):
    link = Links.query.filter_by(owner_id=current_user.id).filter_by(name=link_name).first()
    form = LinkEditForm()   
    if form.validate_on_submit():
        if form.edit_submit.data:
            if form.link.data != link.link:
                link.link = form.link.data
            db.session.commit()
        if form.delete_submit.data:
            db.session.delete(link)
            db.session.commit()
            flash('Link has been deleted.', 'success')   
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        form.link.data = link.link
    title = 'Edit link'
    return render_template('users/edit_link.html', 
                           form=form, 
                           link=link)


@users.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if username == current_user.username:
        return redirect(url_for('users.profile'))
    if not user:
        flash('No user with this username', 'danger')
        return redirect(url_for('main.home'))
    image_file = url_for('static', filename=f'profile_pictures/{user.image_file}')
    links = Links.query.filter_by(owner_id=user.id)
    qrcode = get_qrcode(current_user.username)
    return render_template('users/user.html', 
                           user=user, 
                           image_file=image_file, 
                           links=links, 
                           qrcode=qrcode)


@users.route('/admin/panel')
@login_required
def admin_panel():
    if current_user.role[0].user_role == ROLES['user']:
        flash('You don\'t have enough permission', 'danger')
        return redirect(url_for('main.home'))
    title = 'Admin Panel'
    role = current_user.role[0].user_role.upper()
    return render_template('users/admin_panel.html', 
                           title=title, 
                           role=role)


@users.route('/admin/reviews')
@login_required
def admin_panel_reviews():
    if current_user.role[0].user_role == ROLES['user']:
        flash('You don\'t have enough permission', 'danger')
        return redirect('main.home')
    title = 'Admin Panel | Reviews'
    page = request.args.get('page', 1, type=int)
    reviews = Reviews.query.order_by(Reviews.date.desc()).paginate(page=page, per_page=25)
    return render_template('users/admin_panel_reviews.html', 
                           title=title, 
                           reviews=reviews)


@users.route('/admin/roles', methods=['GET', 'POST'])
@login_required
def admin_panel_edit_roles():
    if current_user.role[0].user_role != ROLES['admin']:
        flash('You don\'t have enough permission', 'danger')
        return redirect('main.home')
    form = EditRoleForm()
    if form.validate_on_submit():
        page_uri = url_for('users.admin_panel_edit_roles')
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            flash('No user exists with this username', 'warning')
            return redirect(page_uri)
        if user.id is current_user.id:
            flash('You cannot change you\'s role', 'warning')
            return redirect(page_uri)
        if user.role[0].user_role == ROLES['admin']:
            flash('You cant change role with admin\'s', 'danger')
            return redirect(page_uri)
        role = Roles.query.filter_by(user_id=user.id).first()
        role.user_role = form.role.data
        db.session.commit()
        flash('Success!', 'success')
        return redirect(url_for('users.admin_panel'))
    title = 'Admin Panel | Edit Roles'
    return render_template('users/admin_panel_roles.html', 
                           title=title, 
                           form=form)