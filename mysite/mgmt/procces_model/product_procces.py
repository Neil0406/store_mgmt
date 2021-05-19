from mgmt.models import ProductInfo
from django.forms.models import model_to_dict
from datetime import datetime
import os


class ProductModel():
    def create_product(self, **kwargs):
        try:
            data = ProductInfo(
                company_id = kwargs['company_id'],
                types= kwargs['types'], 
                brand = kwargs['brand'], 
                model= kwargs['model'], 
                name=kwargs['name'],
                purchase_price=kwargs['purchase_price'],
                selling_price= kwargs['selling_price'],
                amount=kwargs['amount'], 
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
            data.purchase_price = int(kwargs['purchase_price'])
            data.selling_price = kwargs['selling_price']
            data.amount = kwargs['amount'] 
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

    def delete_image(self, data_image):
        path = os.getcwd()
        path = path + '/' +str(data_image)
        os.remove(path)