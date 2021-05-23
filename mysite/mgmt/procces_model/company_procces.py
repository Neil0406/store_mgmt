from mgmt.models import CompanyInfo, CompanyProductInfo
from django.forms.models import model_to_dict
from datetime import datetime

class CompanyModel():
    def create_company(self, **kwargs):
        try:
            company_name = kwargs['company_name']
            check = CompanyInfo.objects.get(company_name=company_name)
            if check.company_active == False:
                check.company_active = True
                check.save()
                ret = 'restart'
            else:
                ret = 'exists'
        except:
            data = CompanyInfo(
                	company_name = kwargs['company_name'],
                    company_region= kwargs['company_region'], 
                    company_town= kwargs['company_town'], 
					company_address=kwargs['company_address'],
                    company_phone=kwargs['company_phone'],
                    company_ext= kwargs['company_ext'],
					company_contact_person=kwargs['company_contact_person'],
                    company_email=kwargs['company_email'], 
                    mobile_phone= kwargs['mobile_phone'],
					mobile_contact_person=kwargs['mobile_contact_person'],
                    mobile_email=kwargs['mobile_email'], 
                    uniform_numbers= kwargs['uniform_numbers'],
					company_url=kwargs['company_url'],
                    company_info=kwargs['company_info'],
                    updated= kwargs['updated'],
                    company_active = True
            )
            data.save()
            ret = 'success'
        return ret

    def get_company_update_data(self, company_id):
        ret = CompanyInfo.objects.filter(id=company_id)
        ret = [model_to_dict(i) for i in ret]
        ret[0]['updated'] = ret[0]['updated'].strftime('%Y-%m-%d %H:%M:%S')
        return ret[0]

    def company_update(self, **kwargs):
        try:
            check = CompanyInfo.objects.get(company_name=kwargs['company_name'])  #確認名子是否已存在
            if check.id == int(kwargs['_id']):
                _id = kwargs['_id']
                data = CompanyInfo.objects.get(id=_id)
                data.company_name = kwargs['company_name']                
                data.company_region = kwargs['company_region']
                data.company_town = kwargs['company_town']
                data.company_address = kwargs['company_address']
                data.company_phone = kwargs['company_phone']
                data.company_ext = kwargs['company_ext']
                data.company_contact_person = kwargs['company_contact_person']
                data.company_email = kwargs['company_email']
                data.mobile_phone = kwargs['mobile_phone']
                data.mobile_contact_person = kwargs['mobile_contact_person']
                data.mobile_email = kwargs['mobile_email']
                data.uniform_numbers = kwargs['uniform_numbers']
                data.company_url = kwargs['company_url']
                data.company_info = kwargs['company_info']
                data.updated = datetime.now()
                data.save()
                ret = 'success' 
            else:
                ret = 'exists'
        except:
            ret = 'error'
        return ret

    def company_delete(self, company_id):
        try:
            data = CompanyInfo.objects.get(id=company_id)
            data.company_active = False
            data.save()
            # instance = CompanyInfo.objects.get(id=company_id) #真刪除
            # instance.delete()
            ret = 'success' 
        except:
            ret = 'error'
        return ret

    def create_company_product(self, **kwargs):
        ret = CompanyProductInfo.objects.filter(company_id=kwargs['company_id']).filter(types=kwargs['types']).filter(brand=kwargs['brand']).filter(model=kwargs['model']).filter(name=kwargs['name'])
        l = [model_to_dict(i) for i in ret]
        if len(l) == 0:    
            try:
                data = CompanyProductInfo(
                        company_id = kwargs['company_id'],
                        company_name = kwargs['company_name'],
                        types= kwargs['types'], 
                        brand= kwargs['brand'], 
                        model=kwargs['model'],
                        name=kwargs['name'],
                        updated= kwargs['updated'],
                )
                data.save()
                ret = 'success'
            except:
                ret = 'error'
        elif l[0]['name'] == kwargs['name'] and l[0]['model'] == kwargs['model']:
            ret = 'exists'
        return ret
    
    def get_company_product_update_data(self, company_product_id):
        ret = CompanyProductInfo.objects.filter(id=company_product_id)
        ret = [model_to_dict(i) for i in ret]
        ret[0]['updated'] = ret[0]['updated'].strftime('%Y-%m-%d %H:%M:%S')
        return ret[0]

    def company_product_update(self, **kwargs):
        ret = CompanyProductInfo.objects.filter(company_id=kwargs['company_id']).filter(types=kwargs['types']).filter(brand=kwargs['brand']).filter(model=kwargs['model']).filter(name=kwargs['name'])
        l = [model_to_dict(i) for i in ret]
        if len(l) == 0 or int(kwargs['company_product_id']) == l[0]['id']:    
            try:
                data = CompanyProductInfo.objects.get(id=kwargs['company_product_id'])
                data.company_name = kwargs['company_name']
                data.company_id = kwargs['company_id']
                data.types = kwargs['types']
                data.brand = kwargs['brand']
                data.model = kwargs['model']
                data.name = kwargs['name']
                data.info = kwargs['info']
                data.save()
                ret = 'success'
            except:
                ret = 'error'
        elif l[0]['name'] == kwargs['name'] and l[0]['model'] == kwargs['model']:
            ret = 'exists'
        return ret 

    def company_product_delete(self, company_product_id):
        try:
            instance = CompanyProductInfo.objects.get(id=company_product_id) #真刪除
            instance.delete()
            ret = 'success'
        except:
            ret = 'error' 
        return ret

    def get_company_product_types(self, company_id):
        try:
            ret = CompanyProductInfo.objects.filter(company_id=company_id)
            l = []
            for i in ret:
                if i.types not in l:
                    l.append(i.types)
            ret = l
        except Exception as e:
            ret = 'error'
        return ret

    def get_company_product_brand(self, company_id, types):
        try:
            ret = CompanyProductInfo.objects.filter(company_id=company_id).filter(types=types)
            l = []
            for i in ret:
                if i.brand not in l:
                    l.append(i.brand)
            ret = l
        except Exception as e:
            ret = 'error'
        # print(ret)
        return ret

    def get_company_product_model(self, company_id, types, brand):
        try:
            ret = CompanyProductInfo.objects.filter(company_id=company_id).filter(types=types).filter(brand=brand)
            l = []
            for i in ret:
                if i.model not in l:
                    l.append(i.model)
            ret = l
        except Exception as e:
            ret = 'error'
        # print(ret)
        return ret

    def get_company_product_name(self, company_id, types, brand, model):
        try:
            ret = CompanyProductInfo.objects.filter(company_id=company_id).filter(types=types).filter(brand=brand).filter(model=model)
            l = []
            for i in ret:
                if i.name not in l:
                    l.append(i.name)
            ret = l
        except Exception as e:
            ret = 'error'
        # print(ret)
        return ret

