import hashlib
from django.conf import settings



def md5(data_string):
    salt = settings.SECRET_KEY.encode('utf-8')
    obj = hashlib.md5(salt)
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()