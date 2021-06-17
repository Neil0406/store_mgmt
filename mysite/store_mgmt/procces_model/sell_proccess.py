from datetime import datetime, timedelta
from store_mgmt.models import PurchaseInfo, CompanyProductInfo, SellInfo
from django.forms.models import model_to_dict
from django.db.models.functions import Concat
import os


class SellModel():
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

    def create_sell(self, **kwargs):
        try:
            data = SellInfo(
                purchase_id = kwargs['purchase_id'],
                company_id = kwargs['company_id'],
                product_id = kwargs['product_id'],
                selling_price = kwargs['selling_price_'],
                selling_amount = kwargs['selling_amount'],
                selling_date = self.str_to_datetime(kwargs['selling_date']),
                selling_remark = kwargs['selling_remark'],
                updated = self.get_datetime(),
                active = True
            )
            purchase = PurchaseInfo.objects.get(id=kwargs['purchase_id'])
            purchase.product_in_stock = purchase.product_in_stock - float(kwargs['selling_amount'])
            if purchase.product_in_stock < 0:
                ret = '庫存數量不足'
            else:
                data.save()
                purchase.save()
                ret = 'success'
        except:
            ret = 'error'
        return ret

    def purchase_search(self, company_id, types, keyword):
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


