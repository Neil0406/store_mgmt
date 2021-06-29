import pymysql
from datetime import datetime
import os
import configparser

class CreateAuth():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(os.getcwd() +'/config.ini')
        self.db = config['Database']['db_name']
        self.user = config['Database']['db_user']
        self.passwd = config['Database']['db_password']
        self.host = config['Database']['db_host']
        self.port = config['Database']['db_port']

    def insert_data(self):
        time_ = datetime.now()
        conn = pymysql.connect(host=self.host, port=int(self.port), user=self.user, passwd=self.passwd, db=self.db, charset='utf8')
        # 建立遊標, 查詢資料預設為元組型別
        cursor = conn.cursor()

        auth_ = ['hight','medium', 'low']
        key_ = [
                'user_control_main' , 
                'create_user', 
                'user_control', 
                'auth_control', 
                'company_main',
                'create_company' , 
                'company_list' , 
                'update_company' , 
                'delete_company', 
                'company_product_main' , 
                'create_company_product' ,
                'company_product_list' 
                'update_company_product' , 
                'delete_company_product' , 
                'show_company_product_purchase_price' , 
                'purchase_main',
                'create_purchase' , 
                'purchase_list' , 
                'update_purchase' , 
                'delete_purchase' , 
                'show_purchase_purchase_price' , 
                'sale_main' , 
                'create_sale' , 
                'sale_list' , 
                'update_sale' , 
                'delete_sale' ,
                'show_sale_purchase_price' ,
                'updated' ,
                'created'
        ]
        data = []
        for i in auth_:
            dic = {}
            for j in key_:
                if i == 'hight':
                    dic['auth'] = i
                    dic[j] = True
                    if j == 'updated' or j == 'created':
                        dic[j] = time_
                else:
                    dic['auth'] = i
                    dic[j] = True
                    if j == 'updated' or j == 'created':
                        dic[j] = time_
            data.append(dic)
        
        for i in data:
            keys = ','.join(list(i.keys()))
            val = list(i.values())
            val = tuple(val)
            cursor.executemany("insert into store_mgmt_authcontrol("+keys+")values(%s,%s, %s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [val])
  
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
    CreateAuth = CreateAuth()
    CreateAuth.insert_data()