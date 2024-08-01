from flask import  Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from blog.posts.forms import PostForm
from blog.models import Post
from blog import db

posts = Blueprint('posts', __name__)

@login_required
@posts.route("/manage_posts")
def manage_posts():
    return render_template('manage_posts.html')

@posts.route("/blogs")
def blogs():
    return render_template('blogs.html')

@posts.route("/posts/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('create_post.html', form=form)

@posts.route("/posts/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)
