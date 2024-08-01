# Insert any routes unrelated to the user or their posts,
# but directly related to the website in general.

from flask import Blueprint, render_template
from blog.models import Post

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/index")
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)