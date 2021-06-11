from datetime import datetime, timedelta
from store_mgmt.models import MgmtUser
from store_mgmt.utils.password_encode import PasswordEncode
from django.forms.models import model_to_dict


class UserControlModel():
    def get_datetime(self):
        time_ = datetime.now()
        return time_

    def email_check(self, email):
        '''
        確認 email 是否存在
        '''
        try:
            ret = MgmtUser.objects.get(email=email)
            ret = 'exists'
        except:
            ret = 'success'
        return ret

    def get_user_by_id(self, user_id):
        user = MgmtUser.objects.get(id=user_id)
        user = model_to_dict(user)
        ret = {'id':user['id'], 'name':user['name'], 'email':user['email'], 'auth':user['auth'], 'active':user['active']}
        return ret

    def create_user(self, name, email, auth, password, password_check, active):
        check = self.email_check(email)
        if check == 'success':
            key, ciphered = PasswordEncode().encrypt(password)
            data = MgmtUser(
                name = name,
                email = email,
                auth = auth,
                public_key = key, 
                private_key = ciphered,
                session_expire = self.get_datetime(),
                action = self.get_datetime(),
                active = active,
                updated = self.get_datetime(),
                created = self.get_datetime(),
            )
            data.save()
            ret = 'success'
        elif check == 'exists':
            ret = 'exists'
        return ret

    def update_user(self, user_id, name, email, auth, password, password_check, active):
        user = MgmtUser.objects.get(id=user_id)
        '''
        1. email檢查
        2. 密碼檢查
        '''
        if user.email == email:
            check = 'success'
        else:
            check = self.email_check(email)
        if check == 'success':
            # print(_id, name, email, auth, password, password_check)
            user.name = name
            user.email = email
            user.auth = auth
            if active == 'true':
                active = True
            else:
                active = False
            user.active = active
            if password != '':
                key, ciphered = PasswordEncode().encrypt(password)
                user.public_key = key
                user.private_key = ciphered
            user.updated = self.get_datetime()
            user.save()

            ret = 'success'
        elif check == 'exists':
            ret = 'exists'
        return ret

    def delete_user(self, user_id):
        '''
        刪除 user
        '''
        user = MgmtUser.objects.get(id=user_id)
        if user.auth == 'hight':
            ret = 'error'
        else:
            user.delete()
            ret = 'success'
        return ret

