from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from .models import Post, Category
from .forms import PostForm
from . import db

posts_bp = Blueprint('posts', __name__, url_prefix='/posts')


@posts_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user,
                    category_id=form.category.data)
        db.session.add(post)
        db.session.commit()
        flash('Post created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', form=form)


@posts_bp.route('/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@posts_bp.route('/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.', 'success')
    return redirect(url_for('main.home'))
