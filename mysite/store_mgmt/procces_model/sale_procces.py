from datetime import datetime, timedelta
from store_mgmt.models import PurchaseInfo, CompanyProductInfo, SaleInfo
from django.forms.models import model_to_dict
from django.db.models.functions import Concat
import os


class SaleModel():
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

    def create_sale(self, **kwargs):
        try:
            data = SaleInfo(
                purchase_id = kwargs['purchase_id'],
                company_id = kwargs['company_id'],
                product_id = kwargs['product_id'],
                sale_price = kwargs['sale_price_'],
                sale_amount = kwargs['sale_amount'],
                sale_date = self.str_to_datetime(kwargs['sale_date']),
                sale_remark = kwargs['sale_remark'],
                updated = self.get_datetime(),
                active = True
            )
            purchase = PurchaseInfo.objects.get(id=kwargs['purchase_id'])
            purchase.product_in_stock = purchase.product_in_stock - float(kwargs['sale_amount'])
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
    
    def sale_search(self, company_id, types, keyword):
        if company_id != '' and types == '' and keyword == '':
            sale_list = SaleInfo.objects.filter(company_id=company_id)
        if company_id != '' and types != '' and keyword == '':
            sale_list = SaleInfo.objects.filter(company_id=company_id).filter(product_id__types=types)
        if company_id != '' and types == '' and keyword != '':
            company_product_list = CompanyProductInfo.objects.filter(company_id=company_id).annotate(search=Concat('types','brand','model', 'name')).filter(search__icontains=keyword)
            sale_list = []
            for i in company_product_list:
                for j in SaleInfo.objects.filter(product_id = i.id):
                    sale_list.append(j)

        if company_id != '' and types != '' and keyword != '':
            company_product_list = CompanyProductInfo.objects.filter(company_id=company_id).annotate(search=Concat('types','brand','model', 'name')).filter(search__icontains=keyword).filter(types=types).filter(active=True)
            sale_list = []
            for i in company_product_list:
                for j in SaleInfo.objects.filter(product_id = i.id):
                    sale_list.append(j)

        if company_id == '' and types != '' and keyword == '':
            sale_list = SaleInfo.objects.filter(product_id__types=types)
        if company_id == '' and types == '' and keyword != '':
            company_product_list = CompanyProductInfo.objects.annotate(search=Concat('types','brand','model', 'name')).filter(search__icontains=keyword)
            sale_list = []
            for i in company_product_list:
                for j in SaleInfo.objects.filter(product_id = i.id):
                    sale_list.append(j)
    
        if company_id == '' and types != '' and keyword != '':
            company_product_list = CompanyProductInfo.objects.filter(types=types).annotate(search=Concat('types','brand','model', 'name')).filter(search__icontains=keyword)
            sale_list = []
            for i in company_product_list:
                for j in SaleInfo.objects.filter(product_id = i.id):
                    sale_list.append(j)

        sale_list = sorted(sale_list, key=lambda k: k.sale_date, reverse=True)   #排序 sale_date 由近到遠

        ret = []
        if len(sale_list) != 0:
            for i in sale_list:
                dic = model_to_dict(i)
                dic.update({'company_name':i.company.name})
                dic.update({'types':i.product.types})
                dic.update({'brand':i.product.brand})
                dic.update({'model':i.product.model})
                dic.update({'name':i.product.name})
                dic.update({'purchase_price':i.purchase.purchase_price})
                if i.purchase.image1 == '':
                    image1 = ''
                else:
                    image1 = str(i.purchase.image1)
                if i.purchase.image2 == '':
                    image2 = ''
                else:
                    image2 = str(i.purchase.image2)
                if i.purchase.image3 == '':
                    image3 = ''
                else:
                    image3 = str(i.purchase.image3)
                dic.update({'image1':image1})
                dic.update({'image2':image2})
                dic.update({'image3':image3})
                dic.update({'sale_date':self.datetime_to_str(i.sale_date)})
                dic.update({'updated':self.datetime_to_str(i.updated)})
                ret.append(dic)
        return ret

    def sale_search_by_date(self, search_start_time, search_end_time):
        time_error = ''
        if search_start_time != '':
            search_start_time = self.str_to_datetime(search_start_time)
        if search_end_time != '':
            search_end_time = self.str_to_datetime(search_end_time)

        if search_start_time != '' and search_end_time == '':
            # print('收尋開始時間以後全部')
            sale_list = SaleInfo.objects.filter(sale_date__gte=search_start_time)
        if search_start_time != '' and search_end_time != '':
            if search_start_time > search_end_time:
                # print('結束時間大於開始時間')
                sale_list = []
                time_error = 'time_error'
            else:
                # print('正常搜尋')
                sale_list = SaleInfo.objects.filter(sale_date__gte=search_start_time).filter(sale_date__lte=search_end_time)
        ret = []
        for i in sale_list:
            dic = model_to_dict(i)
            dic.update({'company_name':i.company.name})
            dic.update({'types':i.product.types})
            dic.update({'brand':i.product.brand})
            dic.update({'model':i.product.model})
            dic.update({'name':i.product.name})
            dic.update({'purchase_price':i.purchase.purchase_price})
            if i.purchase.image1 == '':
                image1 = ''
            else:
                image1 = str(i.purchase.image1)
            if i.purchase.image2 == '':
                image2 = ''
            else:
                image2 = str(i.purchase.image2)
            if i.purchase.image3 == '':
                image3 = ''
            else:
                image3 = str(i.purchase.image3)
            dic.update({'image1':image1})
            dic.update({'image2':image2})
            dic.update({'image3':image3})
            dic.update({'sale_date':self.datetime_to_str(i.sale_date)})
            dic.update({'updated':self.datetime_to_str(i.updated)})
            ret.append(dic)
        if time_error == 'time_error':
            ret = 'time_error'
        return ret

    def get_update_sale(self, sale_id):
        sale = SaleInfo.objects.filter(id=sale_id)
        company_name = sale[0].company.name
        purchase = sale[0].purchase
        company_product = sale[0].product

        ret = model_to_dict(sale[0])
        purchase = model_to_dict(purchase)
        if purchase['image1'] == '':
            ret['image1'] = ''
        else:
            ret['image1'] = str(purchase['image1'])
        if purchase['image2'] == '':
            ret['image2'] = ''
        else:
            ret['image2'] = str(purchase['image2'])
        if purchase['image3'] == '':
            ret['image3'] = ''
        else:
            ret['image3'] = str(purchase['image3'])

        ret['sale_date'] = self.datetime_to_str(ret['sale_date'])
        ret['updated'] = self.datetime_to_str(ret['updated'])

        ret['purchase_remark'] = purchase['remark']
        ret['purchase_date'] = self.datetime_to_str(purchase['purchase_date'])
        ret['purchase_sale_price'] = purchase['sale_price']
        ret['purchase_price'] = purchase['purchase_price']
        ret['purchase_amount'] = purchase['amount']
        ret['product_in_stock'] = purchase['product_in_stock']

        ret['company'] = company_name
        ret['types'] = company_product.types
        ret['brand'] = company_product.brand
        ret['model'] = company_product.model
        ret['name'] = company_product.name
        ret['info'] = company_product.info
        return ret

    def update_sale(self, **kwargs):
        sale = SaleInfo.objects.get(id=kwargs['sale_id'])
        try:
            product_in_stock = sale.purchase.product_in_stock + sale.sale_amount   #先將db內 庫存與銷售2張表相加還原
            if float(kwargs['sale_amount']) == 0:
                # print('退貨')
                sale.purchase.product_in_stock = product_in_stock
                sale.purchase.save()
                sale.delete()
                ret = 'return'
            elif product_in_stock - float(kwargs['sale_amount']) < 0:
                ret = '庫存數量不足'
            else:
                sale.purchase.product_in_stock = product_in_stock - float(kwargs['sale_amount'])
                sale.sale_price = kwargs['sale_price_']
                sale.sale_amount = kwargs['sale_amount']
                sale.sale_date = self.str_to_datetime(kwargs['sale_date'])
                sale.sale_remark = kwargs['sale_remark']
                sale.updated = self.get_datetime()
                # print('庫存數量：' , sale.purchase.product_in_stock)
                # print('售出數量：' , sale.sale_amount)
                sale.purchase.save()
                sale.save()
                ret = 'success'
        except Exception as e:
            ret = 'error'
        return ret

    def delete_sale(self, sale_id):
        try:
            sale = SaleInfo.objects.get(id=sale_id)
            product_in_stock = sale.purchase.product_in_stock + sale.sale_amount   #刪除會被加回庫存         
            sale.purchase.product_in_stock = product_in_stock
            sale.purchase.save()
            sale.delete()
            ret = 'success'
        except:
            ret = 'error'
        return ret