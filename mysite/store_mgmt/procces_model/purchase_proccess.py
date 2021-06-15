from datetime import datetime, timedelta
from store_mgmt.models import PurchaseInfo, CompanyProductInfo
from django.forms.models import model_to_dict
from django.db.models.functions import Concat
import os


# 進貨
class PurchaseModel():
    def get_datetime(self):
        time_ = datetime.now()
        return time_
    def datetime_to_str(self, date_time):
        # time_ = date_time.strftime("%Y/%m/%d, %H:%M:%S")
        time_ = date_time.strftime("%Y-%m-%d")
        return time_
    def str_to_datetime(self, date_time):
        time_ = datetime.strptime(date_time, '%Y-%m-%d')
        return time_

    def create_purchase(self, **kwargs):    
        company_product = CompanyProductInfo.objects.get(id=kwargs['company_product_id'])
        if kwargs['image1'] == 'no_update':
            kwargs['image1'] = company_product.image1
        if kwargs['image2'] == 'no_update':
            kwargs['image2'] = company_product.image2
        if kwargs['image3'] == 'no_update':
            kwargs['image3'] = company_product.image3
        try:
            data = PurchaseInfo(
                company_id = kwargs['company_id'],
                product_id =  kwargs['company_product_id'],
                purchase_price = kwargs['purchase_price'],
                selling_price = kwargs['selling_price'],
                amount = kwargs['amount'],
                product_in_stock = kwargs['amount'],
                remark = kwargs['remark'],
                image1 = kwargs['image1'],
                image2 = kwargs['image2'],
                image3 = kwargs['image3'],
                purchase_date = self.str_to_datetime(kwargs['purchase_date']),
                active = True,
                updated = self.get_datetime()
            )
            data.save()
            ret = 'success'
        except:
            ret = 'error'
        return ret

    def purchase_search(self, company_id, types, keyword):
        '''
        庫存查詢
        ### 排除庫存量為0的商品 .filter(product_in_stock__gt=0)
        '''
        if company_id != '' and types == '' and keyword == '':
            purchase_list = PurchaseInfo.objects.filter(company_id=company_id).filter(product_in_stock__gt=0)
        if company_id != '' and types != '' and keyword == '':
            purchase_list = PurchaseInfo.objects.filter(company_id=company_id).filter(product_id__types=types).filter(product_in_stock__gt=0)
        if company_id != '' and types == '' and keyword != '':
            company_product_list = CompanyProductInfo.objects.filter(company_id=company_id).annotate(search=Concat('types','brand','model', 'name')).filter(search__icontains=keyword)
            purchase_list = []
            for i in company_product_list:
                for j in PurchaseInfo.objects.filter(product_id = i.id).filter(product_in_stock__gt=0):
                    purchase_list.append(j)

        if company_id != '' and types != '' and keyword != '':
            company_product_list = CompanyProductInfo.objects.filter(company_id=company_id).annotate(search=Concat('types','brand','model', 'name')).filter(search__icontains=keyword).filter(types=types).filter(active=True)
            purchase_list = []
            for i in company_product_list:
                for j in PurchaseInfo.objects.filter(product_id = i.id).filter(product_in_stock__gt=0):
                    purchase_list.append(j)

        if company_id == '' and types != '' and keyword == '':
            purchase_list = PurchaseInfo.objects.filter(product_id__types=types).filter(product_in_stock__gt=0)
        if company_id == '' and types == '' and keyword != '':
            company_product_list = CompanyProductInfo.objects.annotate(search=Concat('types','brand','model', 'name')).filter(search__icontains=keyword)
            purchase_list = []
            for i in company_product_list:
                for j in PurchaseInfo.objects.filter(product_id = i.id).filter(product_in_stock__gt=0):
                    purchase_list.append(j)
       
        if company_id == '' and types != '' and keyword != '':
            company_product_list = CompanyProductInfo.objects.filter(types=types).annotate(search=Concat('types','brand','model', 'name')).filter(search__icontains=keyword)
            purchase_list = []
            for i in company_product_list:
                for j in PurchaseInfo.objects.filter(product_id = i.id).filter(product_in_stock__gt=0):
                    purchase_list.append(j)
                    
        ret = []
        for i in purchase_list:
            dic = model_to_dict(i)
            dic.update({'company_name':i.company.name})
            dic.update({'types':i.product.types})
            dic.update({'brand':i.product.brand})
            dic.update({'model':i.product.model})
            dic.update({'name':i.product.name})
            ret.append(dic)
        for i in ret:
            i['updated'] = self.datetime_to_str(i['updated'])
            i['purchase_date'] =  self.datetime_to_str(i['purchase_date'])
            if i['image1'] == '':
                i['image1'] = ''
            else:
                i['image1'] = str(i['image1'])
            if i['image2'] == '':
                i['image2'] = ''
            else:
                i['image2'] = str(i['image2'])
            if i['image3'] == '':
                i['image3'] = ''
            else:
                i['image3'] = str(i['image3'])
        return ret

    def get_update_purchase(self,purchase_id):
        purchase = PurchaseInfo.objects.filter(id=purchase_id)
        company_name = purchase[0].company.name
        company_product = purchase[0].product
        ret = model_to_dict(purchase[0])
        if ret['image1'] == '':
            ret['image1'] = ''
        else:
            ret['image1'] = str(ret['image1'])
        if ret['image2'] == '':
            ret['image2'] = ''
        else:
            ret['image2'] = str(ret['image2'])
        if ret['image3'] == '':
            ret['image3'] = ''
        else:
            ret['image3'] = str(ret['image3'])
        ret['updated'] = self.datetime_to_str(ret['updated'] )
        ret['purchase_date'] = self.datetime_to_str(ret['purchase_date'] )
        ret['company'] = company_name
        ret['types'] = company_product.types
        ret['brand'] = company_product.brand
        ret['model'] = company_product.model
        ret['name'] = company_product.name
        ret['info'] = company_product.info
        return ret
    
    def update_purchase(self, **kwargs):
        try:
            purchase = PurchaseInfo.objects.get(id=kwargs['purchase_id'])

            amount = purchase.amount - int(kwargs['amount'])                      #進貨數量若更改會連動 庫存數量
            purchase.product_in_stock =  purchase.product_in_stock - amount
            purchase.amount = amount

            purchase.purchase_price = kwargs['purchase_price']
            purchase.selling_price = kwargs['selling_price']
            purchase.amount = kwargs['amount']
            purchase.purchase_date = kwargs['purchase_date']
            purchase.remark = kwargs['remark']
            purchase.update = self.get_datetime()
            if kwargs['image1'] != 'no_update':
                if purchase.image1 != '':
                    if purchase.product.image1 == purchase.image1:
                        pass
                    else:
                        self.delete_image(purchase.image1)
                purchase.image1 = kwargs['image1']
            if kwargs['image2'] != 'no_update':
                if purchase.image2 != '':
                    if purchase.product.image2 == purchase.image2:
                        pass
                    else:
                        self.delete_image(purchase.image2)
                purchase.image2 = kwargs['image2']
            if kwargs['image3'] != 'no_update':
                if purchase.image3 != '':
                    if purchase.product.image3 == purchase.image3:
                        pass
                    else:
                        self.delete_image(purchase.image3)
                purchase.image3 = kwargs['image3']
            purchase.save()
            ret = 'success'
        except:
            ret = 'error'
        return ret 

    def delete_image(self, data_image):                #刪除照片
        path = os.getcwd()
        path = path + '/' +str(data_image)
        os.remove(path)

    def delete_purchase(self, purchase_id):
        try:
            purchase = PurchaseInfo.objects.get(id=purchase_id)
            if purchase.image1 != '':
                if purchase.product.image1 == purchase.image1:
                    pass
                else:
                    self.delete_image(purchase.image1)
            if purchase.image2 != '':
                if purchase.product.image2 == purchase.image2:
                    pass
                else:
                    self.delete_image(purchase.image2)
            if purchase.image3 != '':
                if purchase.product.image3 == purchase.image3:
                    pass
                else:
                    self.delete_image(purchase.image3)
            purchase.delete()
            ret = 'success'
        except:
            ret = 'error'
        return ret

