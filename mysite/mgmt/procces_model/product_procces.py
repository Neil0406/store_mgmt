from mgmt.models import ProductInfo, ProductSelling
from django.forms.models import model_to_dict
from datetime import datetime
import os


class ProductModel():
    def create_product(self, **kwargs):
        try:
            data = ProductInfo(
                company_id = kwargs['company_id'],
                company_name = kwargs['company_name'],
                types= kwargs['types'], 
                brand = kwargs['brand'], 
                model= kwargs['model'], 
                name=kwargs['name'],
                purchase_price=kwargs['purchase_price'],
                selling_price= kwargs['selling_price'],
                amount=kwargs['amount'], 
                product_in_stock = kwargs['amount'], 
                image= kwargs['image'],
                image2= kwargs['image2'],
                image3= kwargs['image3'],
                info=kwargs['info'],
                purchase_date=kwargs['purchase_date'], 
                updated= kwargs['updated']
            )
            data.save()
            ret = 'success'
        except Exception as e:
            print(e)
            ret = 'error'
        return ret

    def get_product_update_data(self, product_id):
        ret = ProductInfo.objects.filter(id=product_id)
        ret = [model_to_dict(i) for i in ret]
        ret[0]['updated'] = ret[0]['updated'].strftime('%Y-%m-%d %H:%M:%S')
        ret[0]['purchase_date'] = ret[0]['purchase_date'].strftime('%Y-%m-%d')
        if ret[0]['image'] == '':
            ret[0]['image'] = ''
        else:
            ret[0]['image'] = str(ret[0]['image'])
        if ret[0]['image2'] == '':
            ret[0]['image2'] = ''
        else:
            ret[0]['image2'] = str(ret[0]['image2'])
        if ret[0]['image3'] == '':
            ret[0]['image3'] = ''
        else:
            ret[0]['image3'] = str(ret[0]['image3'])
        return ret[0] 

    def product_update(self, **kwargs):
        try:
            data = ProductInfo.objects.get(id=kwargs['id'])
            data.company_id = kwargs['company_id']
            data.company_name = kwargs['company_name']
            data.types = kwargs['types']
            data.brand = kwargs['brand']
            data.model = kwargs['model']
            data.name = kwargs['name']
            data.purchase_price = kwargs['purchase_price']
            data.selling_price = kwargs['selling_price']
            data.amount = kwargs['amount'] 
            data.product_in_stock = kwargs['product_in_stock']
            data.info = kwargs['info']
            data.purchase_date = kwargs['purchase_date']
            data.updated = datetime.now()
            if kwargs['image'] == 'no_update':                       #不更新
                pass
            elif data.image != '' and kwargs['image'] == '':        #刪除資料夾檔案
                self.delete_image(data.image)
                data.image = kwargs['image']
            elif data.image != '' and kwargs['image'] != '':        #刪除資料夾檔案
                self.delete_image(data.image)
                data.image = kwargs['image']
            else:
                data.image = kwargs['image']

            if kwargs['image2'] == 'no_update':                       #不更新
                pass
            elif data.image2 != '' and kwargs['image2'] == '':        #刪除資料夾檔案
                self.delete_image(data.image2)
                data.image2 = kwargs['image2']
            elif data.image2 != '' and kwargs['image2'] != '':        #刪除資料夾檔案
                self.delete_image(data.image2)
                data.image2 = kwargs['image2']
            else:
                data.image2 = kwargs['image2']

            if kwargs['image3'] == 'no_update':                       #不更新
                pass
            elif data.image3 != '' and kwargs['image3'] == '':        #刪除資料夾檔案
                self.delete_image(data.image3)
                data.image3 = kwargs['image3']
            elif data.image3 != '' and kwargs['image3'] != '':        #刪除資料夾檔案
                self.delete_image(data.image3)
                data.image3 = kwargs['image3']
            else:
                data.image3 = kwargs['image3']
            data.save()
            ret = 'success'
        except:
            ret = 'error'
        return ret

    def delete_image(self, data_image):                #刪除照片
        path = os.getcwd()
        path = path + '/' +str(data_image)
        os.remove(path)

    def product_delete(self, product_id):              #刪除進貨商品
        try:
            instance = ProductInfo.objects.get(id=product_id)
            if instance.image != '':
                self.delete_image(instance.image)
            if instance.image2 != '':
                self.delete_image(instance.image2)
            if instance.image3 != '':
                self.delete_image(instance.image3)
            instance.delete()
            ret = 'success'
        except:
            ret = 'error'
        return ret

    def get_selling_data_check(self, **kwargs):
        company_id = kwargs['company_id']
        model = kwargs['model']
        name = kwargs['name']
        ret = ProductInfo.objects.filter(company_id=company_id).filter(model=model).filter(name=name).filter(product_in_stock__gt = 0)   #庫存大於 0
        ret = [model_to_dict(i) for i in ret]
        if len(ret) != 0:
            data = []
            for i in ret:
                data.append({
                    'product_id': i['id'],
                    'company_id': i['company'],
                    'company_name': i['company_name'],
                    'types': i['types'],
                    'brand': i['brand'],
                    'model': i['model'],
                    'name': i['name'],
                    'purchase_price': i['purchase_price'],
                    'selling_price': i['selling_price'],
                    'amount': i['amount'],
                    'product_in_stock': i['product_in_stock'],
                    'info': i['info'],
                    'purchase_date': i['purchase_date'].strftime('%Y-%m-%d'),
                })
            return data
        else:
            return ''
    
    def selling(self, **kwargs):
        try:
            company_name = kwargs['company_name']
            company_id = int(kwargs['company_id'])
            types = kwargs['types']
            brand = kwargs['brand']
            model = kwargs['model']
            name = kwargs['name']
            selling_amount = int(kwargs['selling_amount'])       #售出數量
            selling_price = int(kwargs['selling_price'])         #售出單價
            selling_date = datetime.strptime(kwargs['selling_date'], '%Y-%m-%d')
            info = kwargs['info']
            product_id = int(kwargs['product_id'])                    #銷貨id(對照庫存表的id)
            '''
            流程
            1. 依照 product_id 收尋進貨表 
            2. 將進貨表的 product_in_stock (庫存)數量 - selling_amount (銷售))數量
            3. 更新進貨表
            3. 將selling_price(銷售單價)  x selling_amount(銷售數量) >> 寫入selling_sum(總銷售額)
            4. 新增updated時間
            '''
            data = ProductInfo.objects.get(id=product_id)
            data.product_in_stock = data.product_in_stock - selling_amount
            data.updated = datetime.now()
            data.save()

            selling_sum = selling_amount * selling_price
            
            update = ProductSelling(
                company_name = company_name,
                company_id = company_id,
                types = types,
                brand = brand,
                model = model,
                name = name,
                selling_amount = selling_amount,
                selling_price = selling_price,
                selling_date = selling_date,
                info = info,
                product_id = product_id,
                selling_sum = selling_sum,
                updated = datetime.now()
            )
            update.save()
            ret = 'success'
        except:
            ret = 'error'
        return ret