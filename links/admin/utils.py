import os
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


if __name__ == '__main__':
    key = get_master_key(path='D:\\information\\programming\\portfolio\\site_all_links\\links')
    print(key)