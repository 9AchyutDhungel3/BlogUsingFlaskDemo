import smtplib, os
from flask import url_for


def send_reset_email(user):
    token = user.get_reset_token().decode(
        "utf-8"
    )  # Decode the token to remove the 'b' prefix
    conn = smtplib.SMTP("smtp.gmail.com", 587)
    conn.ehlo()
    conn.starttls()

    email = os.getenv("EMAIL")
    password = os.getenv("EMAIL_PASS")
    conn.login(email, password)

    reset_link = url_for("users.reset_token", token=token, _external=True)

    message = f"""Subject: Password Reset Request

To reset your password, visit the following link: 
{reset_link}

If you didn't make this request then simply ignore this email and no changes will be made."""

    conn.sendmail(email, user.email, message)
    conn.quit()


def save_picture(form_picture):
    """
    Save the picture uploaded through a form.

    Parameters
    ----------
    form_picture : Any
        The picture file uploaded through the form.

    Returns
    -------
    str
        The filename of the saved picture.
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, "static/profile_pics", picture_fn
    )
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn
