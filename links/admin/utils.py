import os 
import secrets
from PIL import Image
from flask import current_app


def get_master_key(**kwarg):
    path = kwarg.get('path')
    if path is None: 
        path = current_app.root_path
        
    file_path = os.path.join(path, 'master_key.txt')
    master_key = ''
    if os.path.exists(file_path):
        with open(file_path) as file:
            master_key = file.readline()
    
    return master_key


def save_image(form_picture):
    random_hex = secrets.token_hex(30)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static\\news_images', picture_fn)
    output_size = (256, 256)

    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(picture_path)
    
    return picture_fn


if __name__ == '__main__':
    key = get_master_key(path='D:\\information\\programming\\portfolio\\site_all_links\\links')
    print(key)