from cryptography.fernet import Fernet

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



if __name__ == '__main__':
    PasswordEncode = PasswordEncode()
    #編碼
    key, encryptstr = PasswordEncode.encrypt("abc123456")
    #解碼
    pwd = PasswordEncode.decrypt(key, encryptstr)
    print(pwd)