from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from links import db
from links.admin.forms import EditRoleForm, AddNewsForm
from links.admin.utils import get_master_key, save_image
from links.models import User, Roles, Reviews, News, ROLES


admin = Blueprint('admin', __name__)


@admin.route('/admin/panel')
@login_required
def admin_panel():
    if current_user.role[0].user_role == ROLES['user']:
        flash('You don\'t have enough permission', 'danger')
        return redirect(url_for('main.home'))
    
    title = 'Admin Panel'
    role = ''.join([x.user_role.upper() for x in current_user.role])

    return render_template('admin/admin_panel.html', 
                           title=title, 
                           role=role)


@admin.route('/admin/reviews')
@login_required
def admin_panel_reviews():
    if ROLES['user'] in [x.user_role for x in current_user.role]:
        flash('You don\'t have enough permission', 'danger')
        return redirect('main.home')
    
    title = 'Admin Panel | Reviews'
    page = request.args.get('page', 1, type=int)
    reviews = Reviews.query.order_by(Reviews.date.desc()).paginate(page=page, per_page=25)

    return render_template('admin/admin_panel_reviews.html', 
                           title=title, 
                           reviews=reviews)


@admin.route('/admin/roles', methods=['GET', 'POST'])
@login_required
def admin_panel_edit_roles():
    roles_current_user = [x.user_role for x in current_user.role]

    if ROLES['admin'] not in roles_current_user: 
        flash('You don\'t have enough permission', 'danger')
        return redirect('main.home')
    
    form = EditRoleForm()
    page_uri = url_for('admin.admin_panel_edit_roles')

    if form.validate_on_submit():
        if form.master_key.data != get_master_key():
            flash('Wrong master key', 'warning')
            return redirect(page_uri)
        
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            flash('No user exists with this username', 'warning')
            return redirect(page_uri)
        
        if user.id is current_user.id:
            flash('You cannot change you\'s role', 'warning')
            return redirect(page_uri)
        
        role = Roles.query.filter_by(user_id=user.id).first()
        role.user_role = form.role.data
        db.session.commit()
        flash('Success!', 'success')
        return redirect(url_for('admin.admin_panel'))
    
    title = 'Admin Panel | Edit Roles'
    return render_template('admin/admin_panel_roles.html', 
                           title=title, 
                           form=form)


@admin.route('/admin/news', methods=['GET', 'POST'])
@login_required
def admin_panel_add_news():
    if ROLES['user'] in [x.user_role for x in current_user.role]:
        flash('You don\'t have enough permission', 'danger')
        return redirect('main.home')
    
    title = 'Add new arcitcle'
    form = AddNewsForm()
    if form.validate_on_submit():
        if form.img.data:
            image = save_image(form.img.data)
        else:
            image = None
        article_title = form.title.data
        article_text = form.article.data
        article = News(title=article_title, text=article_text, image=image)
        db.session.add(article)
        db.session.commit()
    elif request.method == 'GET':
        form.title.data = ''
        form.text.data = ''
    return render_template('admin/admin_panel_add_news.html', 
                           title=title, 
                           form=form)