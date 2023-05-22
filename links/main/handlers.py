from flask import Blueprint, render_template, flash, redirect, url_for
from links.main.forms import ReviewForm
from links.models import Reviews
from links import db
from flask_login import current_user
from links.users.forms import RegisterForm


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    form = RegisterForm()
    return render_template('main/home.html', form=form)


@main.route('/about')
def about():
    title = 'about'
    return render_template('main/about.html', title=title)


@main.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = ReviewForm()
    if form.validate_on_submit():
        review = Reviews(title=form.title.data, \
                         text=form.text.data, \
                         rating=form.rating.data,\
                         rater_id=current_user.id)
        db.session.add(review)
        db.session.commit()
        flash(f"Your feedback has been send! Thanks!", 'success')
        return redirect(url_for('main.home'))
    title = 'feedback'
    return render_template('main/feedback.html', title=title, form=form)


