from mgmt.models import ProductInfo
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