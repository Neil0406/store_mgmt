from datetime import datetime, timedelta
from store_mgmt.models import CompanyInfo, CompanyProductInfo
from django.forms.models import model_to_dict
import os
from django.db.models.functions import Concat


class CompanyModel():
    def get_datetime(self):
        time_ = datetime.now()
        return time_
    def datetime_to_str(self, date_time):
        # time_ = date_time.strftime("%Y/%m/%d, %H:%M:%S")
        time_ = date_time.strftime("%Y-%m-%d")
        return time_
    def create_company(self, **kwargs):
        try:
            name = kwargs['name'].strip()
            check = CompanyInfo.objects.get(name=name)
            if check.active == False:
                check.active = True
                check.save()
                ret = 'restart'
            else:
                ret = 'exists'
        except:
            data = CompanyInfo(
                	name = kwargs['name'].strip(),
                    region= kwargs['region'].strip(), 
                    town= kwargs['town'].strip(), 
					address=kwargs['address'].strip(),
                    phone=kwargs['phone'].strip(),
                    ext= kwargs['ext'].strip(),
					contact_person=kwargs['contact_person'].strip(),
                    email=kwargs['email'].strip(), 
                    mobile_phone= kwargs['mobile_phone'].strip(),
					mobile_contact_person=kwargs['mobile_contact_person'].strip(),
                    mobile_email=kwargs['mobile_email'].strip(), 
                    uniform_numbers= kwargs['uniform_numbers'].strip(),
					url=kwargs['url'].strip(),
                    info=kwargs['info'],
                    updated= self.get_datetime(),
                    active = True
            )
            data.save()
            ret = 'success'
        return ret

    def get_update_company(self, company_id):
        company_info = CompanyInfo.objects.get(id=company_id)
        company_info = model_to_dict(company_info)
        company_info['updated'] = self.datetime_to_str(company_info['updated'])
        return company_info

    def update_company(self, **kwargs):
        def update(kwargs):
            company = CompanyInfo.objects.get(id=kwargs['id'])
            company.name = kwargs['name'].strip()
            company.region= kwargs['region'].strip()
            company.town= kwargs['town'].strip() 
            company.address=kwargs['address'].strip()
            company.phone=kwargs['phone'].strip()
            company.ext= kwargs['ext'].strip()
            company.contact_person=kwargs['contact_person'].strip()
            company.email=kwargs['email'].strip()
            company.mobile_phone= kwargs['mobile_phone'].strip()
            company.mobile_contact_person=kwargs['mobile_contact_person'].strip()
            company.mobile_email=kwargs['mobile_email'].strip()
            company.uniform_numbers= kwargs['uniform_numbers'].strip()
            company.url=kwargs['url'].strip()
            company.info=kwargs['info']
            company.updated= CompanyModel().get_datetime()
            company.save()
        try:
            name = kwargs['name'].strip()
            check = CompanyInfo.objects.get(name=name)
            if check.id == int(kwargs['id']):
                update(kwargs)
                ret = 'success'
            else:
                ret = 'exists'
        except:
            update(kwargs)
            ret = 'success'
        return ret
    
    def delete_company(self, company_id):
        '''
        確認是否已有建立商品，沒有的話執行真刪除
        '''
        company = CompanyInfo.objects.get(id=company_id)
        try:
            company_product = CompanyProductInfo.objects.get(company_id=company_id)
            company.active = False
            print('更新')
            company.save()
            ret = 'success'
        except Exception as e:
            company.delete()
            print('刪除')
            ret = 'success'
        return ret 

    def create_company_product(self, **kwargs):
        ret = CompanyProductInfo.objects.filter(company_id=kwargs['company_id']).filter(types=kwargs['types']).filter(brand=kwargs['brand']).filter(model=kwargs['model']).filter(name=kwargs['name'])
        l = [model_to_dict(i) for i in ret]
        if len(l) == 0:    
            try:
                data = CompanyProductInfo(
                        company_id = kwargs['company_id'],
                        types= kwargs['types'].strip(), 
                        brand= kwargs['brand'].strip(), 
                        model=kwargs['model'].strip(),
                        name=kwargs['name'].strip(),
                        purchase_price=kwargs['purchase_price'],
                        selling_price=kwargs['selling_price'],
                        image1=kwargs['image1'],
                        image2=kwargs['image2'],
                        image3=kwargs['image3'],
                        info=kwargs['info'],
                        active= True,
                        updated= self.get_datetime(),
                )
                data.save()
                ret = 'success'
            except Exception as e:
                ret = 'error'
        elif l[0]['active'] == False:
            company_product = CompanyProductInfo.objects.get(id=l[0]['id'])
            company_product.active = True
            company_product.purchase_price=kwargs['purchase_price']
            company_product.selling_price=kwargs['selling_price']
            company_product.image1=kwargs['image1']
            company_product.image2=kwargs['image2']
            company_product.image3=kwargs['image3']
            company_product.info=kwargs['info']
            company_product.save()
            ret = 'restart'
        elif l[0]['name'] == kwargs['name'] and l[0]['model'] == kwargs['model']:
            ret = 'exists'
        return ret

    def company_product_search(self, company_id, types, keyword):
        if company_id != '' and types == '' and keyword == '':
            company_product_list = CompanyProductInfo.objects.filter(company_id=company_id).filter(active=True)
        if company_id != '' and types != '' and keyword == '':
            company_product_list = CompanyProductInfo.objects.filter(company_id=company_id).filter(types=types).filter(active=True)
        if company_id != '' and types == '' and keyword != '':
            # company_product_list = CompanyProductInfo.objects.filter(company_id=company_id).filter(model__contains=model).filter(active=True)
            company_product_list = CompanyProductInfo.objects.filter(company_id=company_id).annotate(search=Concat('types','brand','model', 'name')).filter(search__icontains=keyword).filter(active=True)
        if company_id != '' and types != '' and keyword != '':
            company_product_list = CompanyProductInfo.objects.filter(company_id=company_id).filter(types=types).filter(active=True)
        if company_id == '' and types != '' and keyword == '':
            company_product_list = CompanyProductInfo.objects.filter(types=types).filter(active=True)
        if company_id == '' and types == '' and keyword != '':
            # company_product_list = CompanyProductInfo.objects.filter(model__contains=model).filter(active=True)
            company_product_list = CompanyProductInfo.objects.annotate(search=Concat('types','brand','model', 'name')).filter(search__icontains=keyword).filter(active=True)
        if company_id == '' and types != '' and keyword != '':
            # company_product_list = CompanyProductInfo.objects.filter(types=types).filter(model__contains=model).filter(active=True)
            company_product_list = CompanyProductInfo.objects.filter(types=types).annotate(search=Concat('types','brand','model', 'name')).filter(search__icontains=keyword).filter(active=True)


        ret = []
        for i in company_product_list:
            dic = model_to_dict(i)
            dic.update({'company_name':i.company.name})
            ret.append(dic)
        for i in ret:
            i['updated'] = self.datetime_to_str(i['updated'])
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


    def get_company_product_types(self, company_id):
        try:
            company_product_list = CompanyProductInfo.objects.filter(company_id=company_id).filter(active=True)
            ret = []
            for i in company_product_list:
                if model_to_dict(i)['types'] not in ret:
                    ret.append(model_to_dict(i)['types'])
        except:
            ret = 'error'
        return ret

    def get_company_product_brand(self, company_id, types):
        try:
            company_product_list = CompanyProductInfo.objects.filter(company_id=company_id).filter(types=types).filter(active=True)
            ret = []
            for i in company_product_list:
                if model_to_dict(i)['brand'] not in ret:
                    ret.append(model_to_dict(i)['brand'])
        except:
            ret = 'error'
        return ret

    def get_company_product_model(self, company_id, types, brand):
        try:
            company_product_list = CompanyProductInfo.objects.filter(company_id=company_id).filter(types=types).filter(brand=brand).filter(active=True)
            ret = []
            for i in company_product_list:
                if model_to_dict(i)['model'] not in ret:
                    ret.append(model_to_dict(i)['model'])
        except:
            ret = 'error'
        return ret

    def get_company_product_name(self, company_id, types, brand, model):
        try:
            company_product_list = CompanyProductInfo.objects.filter(company_id=company_id).filter(types=types).filter(brand=brand).filter(model=model).filter(active=True)
            ret = []
            for i in company_product_list:
                if model_to_dict(i)['name'] not in ret:
                    ret.append(model_to_dict(i)['name'])
        except:
            ret = 'error'
        return ret
    
    def get_company_product(self, company_id, types, brand, model, name):
        try:
            company_product = CompanyProductInfo.objects.filter(company_id=company_id).filter(types=types).filter(brand=brand).filter(model=model).filter(name=name).filter(active=True)
            ret = model_to_dict(company_product[0])
            ret['updated'] = self.datetime_to_str(ret['updated'])
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
        except:
            ret = 'error'
        return ret
    
    def get_update_company_product(self, company_product_id):
        company_product = CompanyProductInfo.objects.filter(id=company_product_id)
        company_name = company_product[0].company.name
        ret = model_to_dict(company_product[0])
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
        ret['company'] = company_name
        return ret

    def update_company_product(self, **kwargs):
        ret = CompanyProductInfo.objects.filter(company_id=kwargs['company_id']).filter(types=kwargs['types']).filter(brand=kwargs['brand']).filter(model=kwargs['model']).filter(name=kwargs['name'])
        l = [model_to_dict(i) for i in ret]
        def update(kwargs):
            company_product = CompanyProductInfo.objects.get(id=kwargs['company_product_id'])
            company_product.types = kwargs['types'].strip()
            company_product.brand = kwargs['brand'].strip()
            company_product.model = kwargs['model'].strip()
            company_product.name = kwargs['name'].strip()
            company_product.info = kwargs['info'].strip()
            company_product.purchase_price = kwargs['purchase_price']
            company_product.selling_price = kwargs['selling_price']
            company_product.updated= self.get_datetime()
            if kwargs['image1'] != 'no_update':
                if company_product.image1 != '':
                    self.delete_image(company_product.image1)
                company_product.image1 = kwargs['image1']
            if kwargs['image2'] != 'no_update':
                if company_product.image2 != '':
                    self.delete_image(company_product.image2)
                company_product.image2 = kwargs['image2']
            if kwargs['image3'] != 'no_update':
                if company_product.image3 != '':
                    self.delete_image(company_product.image3)
                company_product.image3 = kwargs['image3']
            company_product.save()
        if len(l) == 0:    
            update(kwargs)
            ret = 'success'
        elif int(kwargs['company_product_id']) == l[0]['id']:
            update(kwargs)
            ret = 'success'
        elif l[0]['name'] == kwargs['name'] and l[0]['model'] == kwargs['model']:
            ret = 'exists'
        return ret

    def delete_image(self, data_image):                #刪除照片
        path = os.getcwd()
        path = path + '/' +str(data_image)
        os.remove(path)

    def delete_company_product(self, company_product_id):
        company_product = CompanyProductInfo.objects.get(id=company_product_id)
        try:
            company_product.active = False
            print(company_product)
            company_product.save()
            ret = 'success'
        except:
            ret = 'error'
        return ret