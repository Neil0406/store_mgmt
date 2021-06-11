from datetime import datetime, timedelta
from store_mgmt.models import PurchaseInfo, CompanyProductInfo
from django.forms.models import model_to_dict
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