from flask import url_for
from aboveboard import mail
from flask_mail import Message


# Send password reset function for routes below
def send_password_reset(requester):
    token = requester.get_token()
    msg = Message('Password Reset Request',
                  sender='noreply@aboveboardgamedb.com',
                  recipients=[requester.email])
    msg.html = f'''<p>Hi {requester.fname},</p>
    <p>To reset your password,
    <a href="{url_for('users.reset_token', token=token, _external=True)}">
    click here</a></p>
    If you did not make this request then simply ignore this email
    and no changes will be made.
    '''
    mail.send(msg)
