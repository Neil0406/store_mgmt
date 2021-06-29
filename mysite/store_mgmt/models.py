from django.db import models
from .utils.storage import ImageStorage


#使用者
class MgmtUser(models.Model):            
    id = models.AutoField(primary_key=True)                              
    name = models.CharField(blank=True ,max_length=20)
    auth = models.CharField(blank=True ,max_length=10)
    email= models.EmailField(blank=True)
    public_key = models.CharField(blank=True ,max_length=200)
    private_key = models.CharField(blank=True ,max_length=200)
    session_expire = models.DateTimeField(auto_now_add=False)
    image = models.ImageField(upload_to='./static/user_images', storage=ImageStorage())
    action = models.DateTimeField(auto_now_add=False)
    active = models.BooleanField(blank=True, null=True)
    updated = models.DateTimeField(auto_now_add=False)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):     
        return '{}'.format(self.name)

#公司基本資訊
class CompanyInfo(models.Model):
    id = models.AutoField(primary_key=True)                               #pk                     
    name = models.CharField(blank=True, null=True ,max_length=50)         #公司名
    region = models.CharField(blank=True, null=True ,max_length=10)       #縣市
    town= models.CharField(blank=True, null=True ,max_length=10)          #鄉鎮區
    address = models.CharField(blank=True, null=True ,max_length=60)      #公司地址
    phone = models.CharField(blank=True, null=True ,max_length=30)        #公司電話
    ext = models.CharField(blank=True, null=True ,max_length=20)          #公司分機
    contact_person = models.CharField(blank=True, null=True ,max_length=30)      #公司聯絡人
    email = models.CharField(blank=True, null=True ,max_length=100)              #公司email
    mobile_phone = models.CharField(blank=True, null=True ,max_length=30)                #手機
    mobile_contact_person = models.CharField(blank=True, null=True ,max_length=30)       #手機聯絡人
    mobile_email = models.CharField(blank=True, null=True ,max_length=100)               #手機聯絡人email
    uniform_numbers = models.CharField(blank=True, null=True ,max_length=50)             #公司統編
    url = models.URLField(blank=True, null=True)                                 #公司網址
    info = models.TextField(blank=True, null=True)                               #其他資訊
    active = models.BooleanField(blank=True, null=True)                          #廠商是否有效                  
    updated = models.DateTimeField(auto_now_add=False)                                  
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):     
        return '{}'.format(self.name) 

#公司商品資訊
class CompanyProductInfo(models.Model):
    id = models.AutoField(primary_key=True)                           #pk                     
    company = models.ForeignKey(CompanyInfo, related_name='company_product', on_delete=models.CASCADE)
    types = models.CharField(blank=True, null=True ,max_length=30)   #種類
    brand = models.CharField(blank=True, null=True ,max_length=100)   #種類
    model = models.CharField(blank=True, null=True ,max_length=100)  #型號(編號)
    name = models.CharField(blank=True, null=True ,max_length=100)   #商品名
    purchase_price = models.FloatField(blank=True, null=True)        #進貨價
    sale_price = models.FloatField(blank=True, null=True)         #售價
    image1 = models.ImageField(upload_to='./static/product_images', storage=ImageStorage())
    image2 = models.ImageField(upload_to='./static/product_images', storage=ImageStorage())
    image3 = models.ImageField(upload_to='./static/product_images', storage=ImageStorage())
    info = models.TextField(blank=True, null=True)                   #簡介
    active = models.BooleanField(blank=True, null=True)               
    updated = models.DateTimeField(auto_now_add=False)                                  
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):     
        return '{}'.format(self.model)

#進貨log
class PurchaseInfo(models.Model):
    id = models.AutoField(primary_key=True)                           #pk                     
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE)
    product = models.ForeignKey(CompanyProductInfo, on_delete=models.CASCADE)
    purchase_price = models.FloatField(blank=True, null=True)        #進貨價
    sale_price = models.FloatField(blank=True, null=True)         #售價
    image1 = models.ImageField(upload_to='./static/product_images', storage=ImageStorage())
    image2 = models.ImageField(upload_to='./static/product_images', storage=ImageStorage())
    image3 = models.ImageField(upload_to='./static/product_images', storage=ImageStorage())
    amount = models.FloatField(blank=True, null=True)
    product_in_stock = models.FloatField(blank=True, null=True)      #庫存數量
    purchase_date = models.DateTimeField(auto_now_add=False)         #進貨日
    remark = models.TextField(blank=True, null=True)                 #備註
    active = models.BooleanField(blank=True, null=True)               
    updated = models.DateTimeField(auto_now_add=False)                                  
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):     
        return '{}'.format(self.product)

#銷貨log
class SaleInfo(models.Model):
    id = models.AutoField(primary_key=True)                           #pk                     
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE)
    product = models.ForeignKey(CompanyProductInfo, on_delete=models.CASCADE)
    purchase = models.ForeignKey(PurchaseInfo, on_delete=models.CASCADE)
    sale_price = models.FloatField(blank=True, null=True)         #售價
    sale_amount = models.FloatField(blank=True, null=True)
    sale_remark = models.TextField(blank=True, null=True)        #備註
    sale_date = models.DateTimeField(auto_now_add=False)         #銷貨日
    active = models.BooleanField(blank=True, null=True)               
    updated = models.DateTimeField(auto_now_add=False)                                  
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):     
        return '{}'.format(self.product)


#自訂權限
class AuthControl(models.Model):
    id = models.AutoField(primary_key=True)
    auth = models.CharField(blank=True, null=True ,max_length=50)
    user_control_main = models.BooleanField(blank=True, null=True)
    create_user = models.BooleanField(blank=True, null=True)
    user_control= models.BooleanField(blank=True, null=True)
    auth_control= models.BooleanField(blank=True, null=True)

    company_main = models.BooleanField(blank=True, null=True)
    create_company = models.BooleanField(blank=True, null=True)
    company_list = models.BooleanField(blank=True, null=True)
    update_company = models.BooleanField(blank=True, null=True)
    delete_company = models.BooleanField(blank=True, null=True)

    company_product_main = models.BooleanField(blank=True, null=True)
    create_company_product = models.BooleanField(blank=True, null=True)
    company_product_list = models.BooleanField(blank=True, null=True)
    update_company_product = models.BooleanField(blank=True, null=True)
    delete_company_product = models.BooleanField(blank=True, null=True)
    show_company_product_purchase_price = models.BooleanField(blank=True, null=True)

    purchase_main= models.BooleanField(blank=True, null=True)
    create_purchase = models.BooleanField(blank=True, null=True)
    purchase_list = models.BooleanField(blank=True, null=True)
    update_purchase = models.BooleanField(blank=True, null=True)
    delete_purchase = models.BooleanField(blank=True, null=True)
    show_purchase_purchase_price = models.BooleanField(blank=True, null=True)
    sale_main = models.BooleanField(blank=True, null=True)
    create_sale = models.BooleanField(blank=True, null=True)
    sale_list = models.BooleanField(blank=True, null=True)
    update_sale = models.BooleanField(blank=True, null=True)
    delete_sale = models.BooleanField(blank=True, null=True)
    show_sale_purchase_price = models.BooleanField(blank=True, null=True)
    
    updated = models.DateTimeField(auto_now_add=False)                                  
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):     
        return '{}'.format(self.auth)
