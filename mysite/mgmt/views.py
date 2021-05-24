from django.shortcuts import render,redirect, HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from .utils.password_encode import PasswordEncode
from .models import MgmtUser, CompanyInfo, CompanyProductInfo, ProductInfo
from .procces_model.company_procces import CompanyModel
from .procces_model.product_procces import ProductModel
from datetime import datetime, timedelta
from django.forms.models import model_to_dict
import json

def session_check(request):
	if 'email' in request.session:
		email = request.session['email'] 
		user = MgmtUser.objects.get(email=email)
		session_expire = user.session_expire
		now = datetime.now()
		if session_expire > now:
			return user, True
		else:
			return None, False
	else:
		return None, False


def login(request):
	info =''
	user, check = session_check(request)
	if check == True:
		return redirect ('home/')
	elif request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')
		user = MgmtUser.objects.get(email=email)
		password_check = PasswordEncode().decrypt(user.public_key, user.private_key)
		if password == password_check:
			request.session['email']= email
			time_ = datetime.now()
			day = timedelta(days=7)
			session_expire = day + time_
			user.session_expire = session_expire
			user.save()
			return redirect ('home/')
		else:
			info = '帳號或密碼錯誤'
			return render(request,'login.html', locals())
	else:
		return render(request,'login.html', locals())

def logout(request):
	if 'email' in request.session and request.method == 'GET':
		del request.session['email']
		request.session.flush()
		return redirect ('/')
	else:
		return redirect ('/')

def home(request):
	user, check = session_check(request)
	if check == True:
		return render(request,'home.html', locals())
	else:
		return redirect ('/')


class Product():
	def product_list(self, request):
		user, check = session_check(request)
		if check == True:
			product_list = ProductInfo.objects.all()
			if request.method == 'POST':
				product_id = request.POST.get('product_id')
				ret = ProductModel().get_product_update_data(product_id)
				company_list = CompanyInfo.objects.all().filter(company_active=True)          #如果不想看到刪除店家 .filter(company_active=True)
				company_name_list = [i.company_name for i in company_list]
				company_id_list = [i.id for i in company_list]
				ret = json.dumps({'data':ret, 'company_name_list':company_name_list, 'company_id_list':company_id_list})
				return HttpResponse(ret)
			return render(request,'product/product_list.html', locals())
		else:
			return redirect ('/')

	def create_product(self, request):
		user, check = session_check(request)
		if check == True:
			company_list = CompanyInfo.objects.all().filter(company_active=True)
			if request.method == 'POST':
				try:
					image = request.FILES['image']
				except:
					image = ''
				try:
					image2 = request.FILES['image2']
				except:
					image2 = ''
				try:
					image3 = request.FILES['image3']
				except:
					image3 = ''
				data = request.POST.get('data')
				data = json.loads(data)  
				data['image'] = image
				data['image2'] = image2
				data['image3'] = image3
				data['purchase_date'] = datetime.strptime(data['purchase_date'], '%Y-%m-%d')
				updated = datetime.now()
				data['updated'] = updated
				ret = ProductModel().create_product(**data)
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)

			return render(request,'product/create_product.html', locals())
		else:
			return redirect ('/')

	def product_update(self, request):
		user, check = session_check(request)
		if check == True:
			if request.method == 'POST':
				try:
					image = request.FILES['image']
				except:
					try:
						image = request.POST.get('image')
						image = json.loads(image) 
						image = image['type']	
					except:
						image = ''
				try:
					image2 = request.FILES['image2']
				except:
					try:
						image2 = request.POST.get('image2')
						image2 = json.loads(image2) 
						image2 = image2['type2']
					except Exception as e:
						image2 = ''
				try:
					image3 = request.FILES['image3']
				except:
					try:
						image3 = request.POST.get('image3')
						image3 = json.loads(image3) 
						image3 = image3['type3'] 	
					except Exception as e:
						image3 = ''

				data = request.POST.get('data')
				data = json.loads(data)  
				data['image'] = image
				data['image2'] = image2
				data['image3'] = image3
				data['purchase_date'] = datetime.strptime(data['purchase_date'], '%Y-%m-%d')
				ret = ProductModel().product_update(**data)
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
			else:
				return redirect ('/')
		else:
			return redirect ('/')

	def product_delete(self, request):
		user, check = session_check(request)
		if check == True:
			if request.method == 'POST':
				product_id = request.POST.get('product_id')
				ret = ProductModel().product_delete(product_id)
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
			else:
				return redirect ('/')
		else:
			return redirect ('/')

	def selling(self, request):
		user, check = session_check(request)
		if check == True:
			company_list = CompanyInfo.objects.all().filter(company_active=True)
			if request.method == 'POST':
				data = request.POST.get('data')
				data = json.loads(data)
				ret = ProductModel().selling(**data)
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
			return render(request,'product/selling.html', locals())
		else:
			return redirect ('/')

	def get_selling_data_check(self, request):
		user, check = session_check(request)
		if check == True:
			if request.method == 'POST':
				company_id = request.POST.get('company_id')
				types = request.POST.get('types')
				brand = request.POST.get('brand')
				model = request.POST.get('model')
				name = request.POST.get('name')
				data = {'company_id':company_id, 'types':types, 'brand':brand, 'model':model, 'name':name}
				ret = ProductModel().get_selling_data_check(**data)
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
			else:
				return redirect ('/')
		else:
			return redirect ('/')


class Company():
	def create_company(self, request):              #page
		user, check = session_check(request)
		if check == True:
			if request.method == 'POST':     
				data = request.POST.get('data')   
				data = json.loads(data)          
				updated = datetime.now() 
				data['updated'] = updated
				ret = CompanyModel().create_company(**data)               
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
			return render(request,'company/create_company.html', locals())
		else:
			return redirect ('/')

	def company_list(self, request):
		user, check = session_check(request)
		if check == True:
			company_list = CompanyInfo.objects.all().filter(company_active=True)
			if request.method == 'POST': 
				company_id = request.POST.get('company_id')
				ret = CompanyModel().get_company_update_data(company_id)
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
			return render(request,'company/company_list.html', locals())
		else:
			return redirect ('/')

	def company_update(self, request):
		user, check = session_check(request)
		if check == True:
			if request.method == 'POST': 
				data = request.POST.get('data')
				_id = request.POST.get('_id')
				data = json.loads(data)
				data['_id'] = _id
				ret = CompanyModel().company_update(**data)
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
			else:
				return redirect ('/')
		else:
			return redirect ('/')	

	def company_delete(self, request):
		user, check = session_check(request)
		if check == True:
			if request.method == 'POST': 
				company_id = request.POST.get('company_id')
				# print(company_id)
				ret = CompanyModel().company_delete(company_id)
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
			else:
				return redirect ('/')
		else:
			return redirect ('/')	

	def create_company_product(self, request):              #page
		user, check = session_check(request)
		if check == True:
			company_list = CompanyInfo.objects.all().filter(company_active=True)
			if request.method == 'POST':   
				data = request.POST.get('data')  
				data = json.loads(data)
				updated = datetime.now() 
				data['updated'] = updated   
				ret = CompanyModel().create_company_product(**data)
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
			return render(request,'company/created_company_product.html', locals())
		else:
			return redirect ('/')

	def company_product_list(self, request):                      #廠商代理資訊更新頁面
		user, check = session_check(request)
		if check == True:
			company_list = CompanyInfo.objects.all().filter(company_active=True)
			id_list = [i.id for i in company_list]
			ret = CompanyProductInfo.objects.filter(company_id__in=id_list)                   #找出 company_id 出現在 id_list 的所有資料
			company_product_list = [model_to_dict(i) for i in ret]
			if request.method == 'POST':
				company_product_id = request.POST.get('company_product_id')
				company_id = request.POST.get('company_id')
				company_name_list = [i.company_name for i in company_list]
				ret = CompanyModel().get_company_product_update_data(company_product_id)
				ret = json.dumps({'data':ret, 'company_name_list':company_name_list, 'company_id_list':id_list})
				return HttpResponse(ret)
			return render(request,'company/company_proxy_product.html', locals())
		else:
			return redirect ('/')	

	def company_product_update(self, request):                      #廠商代理資訊更新
		user, check = session_check(request)
		if check == True:
			if request.method == 'POST':
				data = request.POST.get('data')
				data = json.loads(data)
				ret = CompanyModel().company_product_update(**data)
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
			else:
				return redirect ('/')
		else:
			return redirect ('/')	

	def company_product_delete(self, request):                      #廠商代理資訊更新
		user, check = session_check(request)
		if check == True:
			if request.method == 'POST':
				company_product_id = request.POST.get('company_product_id')
				ret = CompanyModel().company_product_delete(company_product_id)
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
			else:
				return redirect ('/')
		else:
			return redirect ('/')	

	def get_company_product_types(self, request):
		user, check = session_check(request)
		if check == True:
			if request.method == 'POST':
				company_id = request.POST.get('company_id')
				ret = CompanyModel().get_company_product_types(company_id)
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
			else:
				return redirect ('/')
		else:
			return redirect ('/')

	def get_company_product_brand(self, request):
		user, check = session_check(request)
		if check == True:
			if request.method == 'POST':
				company_id = request.POST.get('company_id')
				types = request.POST.get('types')
				ret = CompanyModel().get_company_product_brand(company_id, types)
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
			else:
				return redirect ('/')
		else:
			return redirect ('/')

	def get_company_product_model(self, request):
		user, check = session_check(request)
		if check == True:
			if request.method == 'POST':
				company_id = request.POST.get('company_id')
				types = request.POST.get('types')
				brand = request.POST.get('brand')
				ret = CompanyModel().get_company_product_model(company_id, types, brand)
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
			else:
				return redirect ('/')
		else:
			return redirect ('/')

	
	def get_company_product_name(self, request):
		user, check = session_check(request)
		if check == True:
			if request.method == 'POST':
				company_id = request.POST.get('company_id')
				types = request.POST.get('types')
				brand = request.POST.get('brand')
				model = request.POST.get('model')
				ret = CompanyModel().get_company_product_name(company_id, types, brand, model)
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
			else:
				return redirect ('/')
		else:
			return redirect ('/')


	

