import bcrypt
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from blog import db
from blog.models import User
from blog.users.forms import (
    LoginForm,
    RegistrationForm,
    RequestResetForm,
    ResetPasswordForm,
    EditProfileForm
)
from blog.users.utils import send_reset_email

users = Blueprint("users", __name__)


@login_required
@users.route("/account")
def account():
    return render_template("account.html")


@login_required
@users.route("/edit_profile", methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    # After the user submits the form.
    if form.validate_on_submit():
        # I first though that we would have to requery the database , but turns out we
        # can simply use the current_user 
        current_user.username = form.username.data # set the data to whatever was 
        # submitted using the form
        current_user.email = form.email.data
        db.session.commit()
        flash('Your profile has been updated! ', 'success')
        return redirect(url_for('users.account'))
    # After the user is requesting the form before filling and submitting.
    elif request.method == 'GET':
        # Prefill the forms with previous data so that it is easier to make minor 
        # modifications
        form.username.data = current_user.username        
        form.email.data = current_user.email
    # Here the template 'edit_profile.html' gets the prefilled form which the user
    # can then modify accordingly.
    return render_template("edit_profile.html", form=form) 


@users.route("/login", methods=["GET", "POST"])
def login():

    # -------------------------------------------------------------------------------------
    # CASE 1: User is logged in already and requests for this endpoint.
    # -------------------------------------------------------------------------------------
    # if the user is already logged in, then trying to reach the login endpoint is useless/
    # non-sensical operation. So we'll redirect them to the home page, which is an indirect
    # way of pointing out that what they are trying to do is not valid?? ... or sth like
    # that ig. Below, "is_authenticated" checks if the user is already logged in or not.
    # if the user is already logged in then no code segment other than given below, will
    # run.
    # -------------------------------------------------------------------------------------

    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    # -------------------------------------------------------------------------------------
    # CASE 2: User is not logged in already.
    # -------------------------------------------------------------------------------------
    # This particular endpoint will be called in two scenarios:
    #
    # a. User is trying to login in so does a GET request, either by clicking on some on
    #    some link (through <a href="...") or directly typing out the url on the
    #    browser's url bar, which presents him with the form which then he fills and then
    #    clicks the submit button
    #
    # b. User clicks on the submit button after filling out the form, a POST request is
    #    is send to the same endpoint (i.e login), but this time instead of sending the
    #    login.html as response to the user, we do something else:- we perform some stuffs
    #    on server side (in this case checking if the user is present in the database)
    #    and also if the entered password matches the actual password stored.
    #    If it matches then we login him and then redirect him to somewhere else, in this
    #    case the home page. Like before if the user has no business being in the login page
    #    we redirect him somewhere else, because the only reason a user should be presented
    #    with login page is if he wants to login and in no any other case, should he be
    #    presented with this login form.
    # -------------------------------------------------------------------------------------

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.checkpw(form.password.data.encode("utf-8"), user.password):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for("main.index"))
        else:
            flash("Login Unsuccessful. Please check username and password")
    return render_template("login.html", form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.hashpw(
            form.password.data.encode("utf-8"), bcrypt.gensalt()
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in!", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", form=form)


# Reset password routes and related functions:


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
        flash(
            "An email has been sent with instructions to reset your password.", "info"
        )
        return redirect(url_for("users.login"))
    return render_template("reset_request.html", form=form)


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or an expired token")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.hashpw(
            form.password.data.encode("utf-8"), bcrypt.gensalt()
        )
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been updated! You are now able to log in!", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_token.html", form=form)
