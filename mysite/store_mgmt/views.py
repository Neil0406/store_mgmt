from django.shortcuts import render,redirect, HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import MgmtUser, CompanyInfo, CompanyProductInfo, PurchaseInfo
from .utils.password_encode import PasswordEncode
from datetime import datetime, timedelta
from django.forms.models import model_to_dict
import json

from .procces_model.user_control_procces import UserControlModel
from .procces_model.user_procces import UserModel
from .procces_model.company_procces import CompanyModel
from .procces_model.purchase_proccess import PurchaseModel
from .procces_model.sell_proccess import SellModel

def session_check(request):
	if 'email' in request.session:
		try:
			email = request.session['email'] 
			user = MgmtUser.objects.get(email=email)
			session_expire = user.session_expire
			now = datetime.now()
			user.action = now                 #紀錄動作時間
			user.save()
			if session_expire > now and user.active == True:
				return user, True
			else:
				return None, False
		except:                              #被手動刪除上面會取不到 user 資料
			del request.session['email']
			request.session.flush()
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
		try:
			user = MgmtUser.objects.get(email=email)
			password_check = PasswordEncode().decrypt(user.public_key, user.private_key)
			if password == password_check and user.active == True:
				request.session['email']= email
				time_ = datetime.now()
				day = timedelta(days=7)
				session_expire = day + time_
				user.session_expire = session_expire
				user.save()
				return redirect ('home/')
			elif password == password_check and user.active == False:
				info = '帳號尚未啟用'
				return render(request,'login.html', locals())
			else:
				info = '帳號或密碼錯誤'
				return render(request,'login.html', locals())
		except:
			info = '帳號不存在'
			return render(request,'login.html', locals())
	else:
		return render(request,'login.html', locals())

def sign_up(request):
	info =''
	user, check = session_check(request)
	if check == True:
		return redirect ('/')
	elif request.method == 'POST':
		data = request.POST.get('data')
		data = json.loads(data)
		auth = 'low'
		active = False
		ret = UserControlModel().create_user(data['name'], data['email'], auth, data['password'], data['password_check'], active)
		ret = json.dumps({'data':ret})				 
		return HttpResponse (ret)
	else:
		return render(request,'user/sign_up.html', locals())

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


class UserControl():
	def create_user(self, request):
		user, check = session_check(request)
		if check == True:
			if user.auth == 'hight':
				if request.method == 'POST':
					data = request.POST.get('data')
					data = json.loads(data)
					active = True
					ret = UserControlModel().create_user(data['name'], data['email'], data['auth'], data['password'], data['password_check'], active)
					ret = json.dumps({'data':ret})				 
					return HttpResponse (ret)
				return render(request,'user_control/create_user.html', locals())
			else:
				return redirect ('/')
		else:
			return redirect ('/')

	def user_control(self, request):
		user, check = session_check(request)
		if check == True:
			if user.auth == 'hight':
				user_list = MgmtUser.objects.all()
				if request.method == 'POST':
					user_id = request.POST.get('user_id')
					ret = UserControlModel().get_user_by_id(user_id)
					ret = json.dumps({'data':ret})
					return HttpResponse(ret)
				return render(request,'user_control/user_control.html', locals())
			else:
				return redirect ('/')
		else:
			return redirect ('/')

	def update_user(self, request):
		user, check = session_check(request)
		if check == True:
			if user.auth == 'hight':
				if request.method == 'POST':
					data = request.POST.get('data')
					data = json.loads(data)
					ret = UserControlModel().update_user(data['user_id'], data['name'], data['email'], data['auth'], data['password'], data['password_check'], data['active'])
					ret = json.dumps({'data':ret})
					return HttpResponse(ret)
			else:
				return redirect ('/')
		else:
			return redirect ('/')

	def delete_user(self, request):
		user, check = session_check(request)
		if check == True:
			if user.auth == 'hight':
				if request.method == 'POST':
					user_id = request.POST.get('user_id')
					ret = UserControlModel().delete_user(user_id)
					ret = json.dumps({'data':ret})
					return HttpResponse(ret)
			else:
				return redirect ('/')
		else:
			return redirect ('/')


class User():
	def update_user(self, request):
		user, check = session_check(request)
		if check == True:
			if request.method == 'POST':
				try:
					image = request.FILES['image']
				except:
					image = request.POST.get('image')
				data = request.POST.get('data')
				data = json.loads(data)
				data['image'] = image
				ret = UserModel().update_user(**data)
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
			return render(request,'user/update_user.html', locals())
		else:
			return redirect ('/')

	def update_user_password(self, request):
		user, check = session_check(request)
		if check == True and request.method == 'POST':
			data = request.POST.get('data')
			data = json.loads(data)
			ret = UserModel().update_user_password(**data)
			ret = json.dumps({'data':ret})
			return HttpResponse(ret)
		else:
			return redirect ('/')

class Company():
	def create_company(self, request):
		user, check = session_check(request)
		if check == True :
			if request.method == 'POST':
				data = request.POST.get('data')
				data = json.loads(data)
				ret = CompanyModel().create_company(**data)
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
			return render(request,'company/create_company.html', locals())
		else:
			return redirect ('/')

	def company_list(self, request):
		user, check = session_check(request)
		if check == True :
			company_list = CompanyInfo.objects.all().filter(active=True)
			return render(request,'company/company_list.html', locals())
		else:
			return redirect ('/')

	def get_update_company(self, request):
		user, check = session_check(request)
		if check == True :
			company_id = request.POST.get('company_id')
			ret = CompanyModel().get_update_company(company_id)
			ret = json.dumps({'data':ret})
			return HttpResponse(ret)
		else:
			return redirect ('/')	

	def update_company(self, request):
		user, check = session_check(request)
		if check == True :
			data = request.POST.get('data')
			data = json.loads(data)
			ret = CompanyModel().update_company(**data)
			ret = json.dumps({'data':ret})
			return HttpResponse(ret)
		else:
			return redirect ('/')	

	def delete_company(self, request):
		user, check = session_check(request)
		if check == True :
			company_id = request.POST.get('company_id')
			ret = CompanyModel().delete_company(company_id)
			ret = json.dumps({'data':ret})
			return HttpResponse(ret)
		else:
			return redirect ('/')



	def create_company_product(self, request):
		user, check = session_check(request)
		if check == True :
			company_list = CompanyInfo.objects.all().filter(active=True)
			if request.method == 'POST':
				try:
					image1 = request.FILES['image1']
				except:
					image1 = ''
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
				data['image1'] = image1
				data['image2'] = image2
				data['image3'] = image3
				ret = CompanyModel().create_company_product(**data)
				print(ret)
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
			return render(request,'company/create_company_product.html', locals())
		else:
			return redirect ('/')
	
	def get_company_product_types(self, request):
		user, check = session_check(request)
		if check == True :
			if request.method == 'POST':
				company_id = request.POST.get('company_id')
				ret = CompanyModel().get_company_product_types(company_id)
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
		else:
			return redirect ('/')

	def get_company_product_brand(self, request):
		user, check = session_check(request)
		if check == True :
			if request.method == 'POST':
				company_id = request.POST.get('company_id')
				types = request.POST.get('types')
				ret = CompanyModel().get_company_product_brand(company_id, types)
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
		else:
			return redirect ('/')

	def get_company_product_model(self, request):
		user, check = session_check(request)
		if check == True :
			if request.method == 'POST':
				company_id = request.POST.get('company_id')
				types = request.POST.get('types')
				brand = request.POST.get('brand')
				ret = CompanyModel().get_company_product_model(company_id, types, brand)
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
		else:
			return redirect ('/')
	
	def get_company_product_name(self, request):
		user, check = session_check(request)
		if check == True :
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

	def get_company_product(self, request):
		user, check = session_check(request)
		if check == True :
			if request.method == 'POST':
				company_id = request.POST.get('company_id')
				types = request.POST.get('types')
				brand = request.POST.get('brand')
				model = request.POST.get('model')
				name = request.POST.get('name')
				ret = CompanyModel().get_company_product(company_id, types, brand, model, name)
				# ret = ''
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
		else:
			return redirect ('/')


	def company_product_list(self, request):
		user, check = session_check(request)
		if check == True :
			company_list = CompanyInfo.objects.all().filter(active=True)
			company_product_types_list = []
			company_product_list = []

			for i in CompanyProductInfo.objects.filter(company__active = True).filter(active=True).values("types").distinct():  #先過濾公司是否取動再搜尋所有 types 並且不重複
				company_product_types_list.append(i['types'])

			for i in CompanyProductInfo.objects.filter(company__active = True).filter(active=True).order_by('-updated')[:10]:    #先過濾公司是否取動再搜尋 -updated(排續新到舊) 最新的10個
					company_product_list.append(i)

			return render(request,'company/company_product_list.html', locals())
		else:
			return redirect ('/')

	def company_product_search(self, request):
		user, check = session_check(request)
		if check == True :
			if request.method == 'POST':
				company_id = request.POST.get('company_id')
				types = request.POST.get('types')
				keyword = request.POST.get('keyword')
				ret = CompanyModel().company_product_search(company_id, types, keyword)
				# ret = ''
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
		else:
			return redirect ('/')

	def get_update_company_product(self, request):
		user, check = session_check(request)
		if check == True :
			if request.method == 'POST':
				company_product_id = request.POST.get('company_product_id')
				ret = CompanyModel().get_update_company_product(company_product_id)
				# ret = ''
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
		else:
			return redirect ('/')

	def update_company_product(self, request):
		user, check = session_check(request)
		if check == True :
			if request.method == 'POST':
				try:
					image1 = request.FILES['image1']
				except:
					image1 = request.POST.get('image1')
				try:
					image2 = request.FILES['image2']
				except:
					image2 = request.POST.get('image2')
				try:
					image3 = request.FILES['image3']
				except:
					image3 = request.POST.get('image3')
				data = request.POST.get('data')	
				data = json.loads(data)
				data['image1'] = image1
				data['image2'] = image2
				data['image3'] = image3
				ret = CompanyModel().update_company_product(**data)
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
		else:
			return redirect ('/')

	def delete_company_product(self, request):
		user, check = session_check(request)
		if check == True :
			if request.method == 'POST':
				company_product_id = request.POST.get('company_product_id')
				ret = CompanyModel().delete_company_product(company_product_id)
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
		else:
			return redirect ('/')

# 進貨
class Purchase():
	def create_purchase(self, request):
		user, check = session_check(request)
		if check == True :
			if request.method == 'POST':
				try:
					image1 = request.FILES['image1']
				except:
					image1 = request.POST.get('image1')
				try:
					image2 = request.FILES['image2']
				except:
					image2 = request.POST.get('image2')
				try:
					image3 = request.FILES['image3']
				except:
					image3 = request.POST.get('image3')
				data = request.POST.get('data')	
				data = json.loads(data)
				data['image1'] = image1
				data['image2'] = image2
				data['image3'] = image3
				ret = PurchaseModel().create_purchase(**data)
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
			else:
				company_list = CompanyInfo.objects.all().filter(active=True)
				company_product_types_list = []
				for i in CompanyProductInfo.objects.filter(company__active = True).filter(active=True).values("types").distinct():  #先過濾公司是否啟用再搜尋所有 types 並且不重複
					company_product_types_list.append(i['types'])
				return render(request,'purchase/create_purchase.html', locals())
		else:
			return redirect ('/')
	
	def purchase_list(self, request):
		user, check = session_check(request)
		if check == True :
			company_list = CompanyInfo.objects.all()
			company_product_types_list = []
			purchase_list = []
			for i in CompanyProductInfo.objects.values("types").distinct(): 
				company_product_types_list.append(i['types'])
			for i in PurchaseInfo.objects.filter(product_in_stock__gt=0).order_by('-updated')[:30]:  #過濾庫存量大於0
					purchase_list.append(i)
			return render(request,'purchase/purchase_list.html', locals())
		else:
			return redirect ('/')

	def purchase_search(self, request):
		user, check = session_check(request)
		if check == True :
			if request.method == 'POST':
				company_id = request.POST.get('company_id')
				types = request.POST.get('types')
				keyword = request.POST.get('keyword')
				product_in_stock = request.POST.get('product_in_stock')
				ret = PurchaseModel().purchase_search(company_id, types, keyword, product_in_stock)
				# ret = ''
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
		else:
			return redirect ('/')	

	def get_update_purchase(self, request):
		user, check = session_check(request)
		if check == True :
			purchase_id = request.POST.get('purchase_id') 
			ret = PurchaseModel().get_update_purchase(purchase_id)
			ret = json.dumps({'data':ret})
			return HttpResponse(ret)
		else:
			return redirect ('/')

	def update_purchase(self, request):
		user, check = session_check(request)
		if check == True :
			if request.method == 'POST':
				try:
					image1 = request.FILES['image1']
				except:
					image1 = request.POST.get('image1')
				try:
					image2 = request.FILES['image2']
				except:
					image2 = request.POST.get('image2')
				try:
					image3 = request.FILES['image3']
				except:
					image3 = request.POST.get('image3')
				data = request.POST.get('data')	
				data = json.loads(data)
				data['image1'] = image1
				data['image2'] = image2
				data['image3'] = image3
				ret = PurchaseModel().update_purchase(**data)
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
		else:
			return redirect ('/')	

	def delete_purchase(self, request):
		user, check = session_check(request)
		if check == True :
			if request.method == 'POST':
				purchase_id = request.POST.get('purchase_id')
				ret = PurchaseModel().delete_purchase(purchase_id)
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
		else:
			return redirect ('/')	

class Sell():
	def create_sell(self, request):
		user, check = session_check(request)
		if check == True :
			if request.method == 'POST':
				data = request.POST.get('data')
				data = json.loads(data)
				ret = SellModel().create_sell(**data)
				# ret = ''
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
			else:
				company_list = []
				purchase_types_list = []
				purchase_list = []
				for i in PurchaseInfo.objects.filter(product_in_stock__gt=0):
					if i.company not in company_list:
						company_list.append(i.company)
					if i.product.types not in purchase_types_list:
						purchase_types_list.append(i.product.types)
				return render(request,'sell/create_sell.html', locals())
		else:
			return redirect ('/')	
	
	def purchase_search(self, request):
		user, check = session_check(request)
		if check == True :
			if request.method == 'POST':
				company_id = request.POST.get('company_id')
				types = request.POST.get('types')
				keyword = request.POST.get('keyword')
				ret = SellModel().purchase_search(company_id, types, keyword)
				# ret = ''
				ret = json.dumps({'data':ret})
				return HttpResponse(ret)
		else:
			return redirect ('/')	