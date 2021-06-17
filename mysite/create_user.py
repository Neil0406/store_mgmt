import pymysql
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import os
import configparser

class PasswordEncode():
    def generate_key(self):
        '''
        ##### 隨機產生 key
        '''
        return Fernet.generate_key()


    def encrypt(self, pwd):
        '''
        ##### 編碼
            - 輸入密碼
            - 產生新密碼
            - 將 key ciphered 和 decode 存入db
        '''  
        key = self.generate_key()
        cipher_suite = Fernet(key)
        bpwd = bytes(pwd, 'utf-8')
        ciphered = cipher_suite.encrypt(bpwd)

        key = bytes(key).decode("utf-8")
        ciphered = bytes(ciphered).decode("utf-8")
        return key, ciphered


    def decrypt(self, key, enc_pwd):
        '''
        ##### 解碼
            - 輸入 db 裡的 key ciphered
            - 轉回原密碼
        '''  
        cipher_suite = Fernet(bytes(key, 'utf-8'))
        uncipher_text = (cipher_suite.decrypt(bytes(enc_pwd, 'utf-8')))
        return bytes(uncipher_text).decode("utf-8")


class CreateSuperuser():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(os.getcwd() +'/config.ini')
        self.db = config['Database']['db_name']
        self.user = config['Database']['db_user']
        self.passwd = config['Database']['db_password']
        self.host = config['Database']['db_host']
        self.port = config['Database']['db_port']
    
    def insert_data(self, name, public_key, private_key, email):
        time_ = datetime.now()
        day = timedelta(days=7)
        session_expire = day + time_
        conn = pymysql.connect(host=self.host, port=int(self.port), user=self.user, passwd=self.passwd, db=self.db, charset='utf8')
        # 建立遊標, 查詢資料預設為元組型別
        cursor = conn.cursor()

        # cursor.execute("select * from mgmt_mgmtuser")
        cursor.executemany("insert into store_mgmt_mgmtuser(name, auth, public_key, private_key, email, action ,created, updated, session_expire, image, active)values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [(name, 'hight', public_key, private_key,email, time_ , time_, time_, session_expire, '', True)])

        new_id = cursor.lastrowid
        print("Id :", new_id)

        # 提交，不然無法儲存新建或者修改的資料
        conn.commit()
        # 關閉遊標
        cursor.close()
        # 關閉連線
        conn.close()
        print('新增成功')

if __name__ == '__main__':
    name = str(input('Name :'))
    email = str(input('Email :'))
    password = str(input('password :'))
    password_check = str(input('password_check :'))
    if password == password_check:
        PasswordEncode = PasswordEncode()
        key, ciphered = PasswordEncode.encrypt(password)
        CreateSuperuser = CreateSuperuser()
        CreateSuperuser.insert_data(name, key, ciphered, email)
    else:
        print('密碼不符')