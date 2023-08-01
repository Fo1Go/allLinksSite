import secrets
import os.path
import qrcode
from PIL import Image
from flask_mail import Message
from flask import current_app, url_for
from links import mail
from time import time
from authlib.jose import jwt


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static\\profile_pictures', picture_fn)
    output_size = (256, 256)

    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(picture_path)
    
    return picture_fn


def delete_qrcode(username):
    qrcode_name = f'{username}.png'
    qrcode_path = os.path.join(current_app.root_path, 'static\\qrcodes', qrcode_name)
    if os.path.isfile(qrcode_path):
        os.remove(qrcode_path)


def get_qrcode(username):
    qrcode_name = f'{username}.png'
    output_size = (256, 256)
    qrcode_path = os.path.join(current_app.root_path, 'static\\qrcodes', qrcode_name)
    qrcode_uri = url_for('users.user', username=username, _external=True)
    if not os.path.isfile(qrcode_path):
        qrcode_image = qrcode.make(qrcode_uri)
        qrcode_image.thumbnail(output_size)
        qrcode_image.save(qrcode_path)
    return url_for('static', filename=f'qrcodes/{qrcode_name}')


def validate_token(token):
    try:
        token_decoded = jwt.decode(s=token, key=current_app.secret_key)
        user_id = token_decoded['id']
        expires = token_decoded['expires']
        print(user_id)
        if time() > expires:
            return None
    except:
        return None
    
    return user_id


def generate_token(user, *args, TOKEN_TIMEOUT=3600):
    header = {'alg': 'HS256'}
    payload = {'id': user.id,
                'expires': time()+TOKEN_TIMEOUT}
    token = jwt.encode(header=header, payload=payload, key=current_app.secret_key)

    return token


def send_mail(token, email):
    message_text = f'''To reset your password, visit the following link:
{url_for('users.reset_password', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
This message has been created automatically
'''
    subject = 'Reset password'
    sender = os.environ.get('MAIL_USERNAME')

    message = Message()
    message.subject = subject
    message.body = message_text
    message.sender = sender
    message.add_recipient(email)

    print()

    mail.send(message)