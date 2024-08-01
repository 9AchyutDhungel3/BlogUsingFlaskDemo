import smtplib, os
from flask import url_for


def send_reset_email(user):
    token = user.get_reset_token()
    conn = smtplib.SMTP("smtp.gmail.com", 587)
    conn.ehlo()
    conn.starttls()
    
    email = os.getenv('EMAIL')
    password = os.getenv('EMAIL_PASS')
    conn.login(email, password)
    
    conn.sendmail(email, user.email, f'''Password Reset Request\n\nTo reset your password, visit the following link: 
{url_for('users.reset_token', token=token, _external=True)}
If you didn't make this request then simply ignore this email and no changes will be made.''' )