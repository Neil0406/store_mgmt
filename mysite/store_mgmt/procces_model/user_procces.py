from datetime import datetime, timedelta
from store_mgmt.models import MgmtUser
from store_mgmt.utils.password_encode import PasswordEncode
from django.forms.models import model_to_dict
import os

class UserModel():
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

    def update_user(self, **kwargs):
        user = MgmtUser.objects.get(id=kwargs['user_id'])
        if kwargs['image'] != 'no_update':     #不等於 no_update 代表需要更新或新增
            if user.image != '':
                self.delete_image(user.image)
            user.image = kwargs['image']

        if user.email == kwargs['email']:
            check = 'success'
        else:
            check = self.email_check(kwargs['email'])
        if check == 'success':
            user.email = kwargs['email']
            user.name = kwargs['name']
            user.updated = self.get_datetime()
            user.save()
            ret = 'success'
        else:
            ret = 'exists'
        return ret

    def delete_image(self, data_image):                #刪除照片
        path = os.getcwd()
        path = path + '/' +str(data_image)
        os.remove(path)

    def update_user_password(self, **kwargs):
        user = MgmtUser.objects.get(id=kwargs['user_id'])
        pwd = PasswordEncode().decrypt(user.public_key, user.private_key)
        if kwargs['old_password'] == pwd:
            # print('密碼相同')
            key, ciphered = PasswordEncode().encrypt(kwargs['password'])
            user.public_key = key
            user.private_key = ciphered
            user.updated = self.get_datetime()
            user.save()
            ret = 'success'
        else:
            ret = 'error'
            # print('舊密碼錯誤')
        return ret