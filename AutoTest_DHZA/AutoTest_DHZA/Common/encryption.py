import bcrypt
import hashlib
import uuid

class Encryption:
    def bcrypt_en(str):
        b = str.encode('utf-8')
        password=bcrypt.hashpw(b,bcrypt.gensalt(rounds = 10, prefix=b"2a"))
        newpwd='{bcrypt}'+password.decode()
        return newpwd

    def md5_en(str):
        b = str.encode('utf-8')
        m = hashlib.md5()
        m.update(b)
        password = m.hexdigest()
        newpwd='{md5}'+password
        return newpwd

    def get_uuid(key):
        uuid36=uuid.uuid4()
        struuid=str(uuid36)
        return struuid




