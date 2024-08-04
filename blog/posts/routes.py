from flask import Blueprint, render_template, redirect, request, url_for, flash, abort
from flask_login import login_required, current_user
from blog.posts.forms import PostForm
from blog.models import Post
from blog import db

posts = Blueprint("posts", __name__)


@login_required
@posts.route("/manage_posts")
def manage_posts():
    return render_template("manage_posts.html")


@posts.route("/blogs")
def blogs():
    return render_template("blogs.html")


# to create a new post you must be logged in
@posts.route("/posts/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data, content=form.content.data, author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created", "success")
        return redirect(url_for("main.index"))
    return render_template("create_post.html", form=form)


# Just to view a particular post  you don't need to be logged in
@posts.route("/posts/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@posts.route("/posts/<int:post_id>/update", methods=["GET", "POST"])
@login_required  # to edit a post you must be logged in
def update_post(post_id):
    post = Post.query.get_or_404(
        post_id
    )  # see if the post with that particular id exists in the database.
    if post.author != current_user:
        abort(403)  # only the author of the post must be authorized to edit the post
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated!", "success")
        return redirect(url_for("post", post_id=post.id))
    # Note here that unlike what we used to do before, we have explicitly defined a condition if the request is "GET" . Here we don't want to present the user to have to
    # type the entire preexisting post again, when what he was wanted was just to edit a
    # word or two. So we prefill the form that is presented to the user when he/she
    # does a GET request on this particular endpoint, that way he/she doesn't have to
    # retype the entire post content and title .
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("post.html", title=post.title, post=post)
