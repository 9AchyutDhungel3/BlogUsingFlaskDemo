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
