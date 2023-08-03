from flask import Blueprint, render_template, flash, redirect, url_for, request
from links.main.forms import ReviewForm
from links.models import Reviews, News
from links import db
from flask_login import current_user
from links.users.forms import RegisterForm
from links.admin.forms import AddNewsForm, EditNewsForm
from links.admin.utils import save_image



main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    form = RegisterForm()
    news = News.query.order_by(News.date.desc()).limit(5)
    return render_template('main/home.html', 
                           form=form,
                           news=news)


@main.route('/about')
def about():
    title = 'about'
    return render_template('main/about.html', 
                           title=title)


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


@main.route('/news', methods=['GET', 'POST'])
def news():
    form = AddNewsForm()
    if form.validate_on_submit():
        if form.img.data:
            image = save_image(form.img.data)
        else:
            image = None
        article_title = form.title.data
        text = form.text.data
        article = News(title=article_title, text=text, image=image)
        db.session.add(article)
        db.session.commit()
    elif request.method == 'GET':
        form.title.data = ''
        form.text.data = ''

    title = 'News'
    page = request.args.get('page', 1, type=int)
    articles = News.query.order_by(News.date.desc()).paginate(page=page, per_page=10)
    return render_template('main/news.html', 
                           articles=articles,
                           title=title,
                           form=form)


@main.route('/news/<int:article_id>', methods=['GET', 'POST'])
def article(article_id):
    form = EditNewsForm()
    article = News.query.get(article_id)
    if form.validate_on_submit():
        if form.edit_submit.data:
            if form.img.data:
                image = save_image(form.img.data)
                article.image = image
            else:
                image = None
            article.title = form.title.data
            article.text = form.text.data
        if form.delete_submit.data:
            db.session.delete(article)
        db.session.commit()
        return redirect(url_for('main.news'))
    elif request.method == 'GET':
        form.title.data = article.title
        form.text.data = article.text

    title = 'Arcitle - ' + article.title
    return render_template('main/article.html',
                           title=title,
                           article=article,
                           form=form)