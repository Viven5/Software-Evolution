from flask import Blueprint, render_template, request
from .models import Post, Category

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@main_bp.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main_bp.route('/search')
def search():
    q = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter((Post.title.ilike(f'%{q}%')) | (Post.content.ilike(f'%{q}%')))
    posts = posts.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('search_results.html', posts=posts, query=q)


@main_bp.route('/category/<string:name>')
def category(name):
    page = request.args.get('page', 1, type=int)
    category = Category.query.filter_by(name=name).first_or_404()
    posts = Post.query.filter_by(category=category).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('category.html', posts=posts, category=category)
