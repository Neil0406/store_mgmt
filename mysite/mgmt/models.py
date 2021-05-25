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
    updated = models.DateTimeField(auto_now_add=False)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):     
        return '{}'.format(self.name) 

#公司基本資訊
class CompanyInfo(models.Model):
    id = models.AutoField(primary_key=True)                               #pk                     
    company_name = models.CharField(blank=True, null=True ,max_length=50)         #公司名
    company_region = models.CharField(blank=True, null=True ,max_length=10)       #縣市
    company_town= models.CharField(blank=True, null=True ,max_length=10)          #鄉鎮區
    company_address = models.CharField(blank=True, null=True ,max_length=60)      #公司地址
    company_phone = models.CharField(blank=True, null=True ,max_length=30)        #公司電話
    company_ext = models.CharField(blank=True, null=True ,max_length=20)          #公司分機
    company_contact_person = models.CharField(blank=True, null=True ,max_length=30)      #公司聯絡人
    company_email = models.CharField(blank=True, null=True ,max_length=100)              #公司email
    mobile_phone = models.CharField(blank=True, null=True ,max_length=30)                #手機
    mobile_contact_person = models.CharField(blank=True, null=True ,max_length=30)       #手機聯絡人
    mobile_email = models.CharField(blank=True, null=True ,max_length=100)               #手機聯絡人email
    uniform_numbers = models.CharField(blank=True, null=True ,max_length=50)             #公司統編
    company_url = models.URLField(blank=True, null=True)                                 #公司網址
    company_info = models.TextField(blank=True, null=True)                               #另外資訊
    company_active = models.BooleanField(blank=True, null=True)                          #廠商是否有效                  
    updated = models.DateTimeField(auto_now_add=False)                                  
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):     
        return '{}'.format(self.company_name) 

#公司商品資訊
class CompanyProductInfo(models.Model):
    id = models.AutoField(primary_key=True)                          #pk                     
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE)
    company_name = models.CharField(blank=True, null=True ,max_length=50)         #公司名
    types = models.CharField(blank=True, null=True ,max_length=30)   #種類
    brand = models.CharField(blank=True, null=True ,max_length=100)   #種類
    model = models.CharField(blank=True, null=True ,max_length=100)  #型號(編號)
    name = models.CharField(blank=True, null=True ,max_length=100)   #商品名
    info = models.TextField(blank=True, null=True)                   #另外資訊
    updated = models.DateTimeField(auto_now_add=False)                                  
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):     
        return '{}'.format(self.model) 

#進貨資訊(log)
class ProductInfo(models.Model):                      
    id = models.AutoField(primary_key=True)                       
    company = models.ForeignKey(CompanyInfo, related_name='company_id', on_delete=models.CASCADE)
    company_name = models.CharField(blank=True, null=True ,max_length=50)         #公司名
    types = models.CharField(blank=True, null=True ,max_length=30)   #種類
    brand = models.CharField(blank=True, null=True ,max_length=50)   #品牌
    model = models.CharField(blank=True, null=True ,max_length=100)  #型號(編號)
    name = models.CharField(blank=True, null=True ,max_length=100)   #商品名
    purchase_price = models.FloatField(blank=True, null=True)        #進貨價
    selling_price = models.FloatField(blank=True, null=True)         #售價
    amount = models.FloatField(blank=True, null=True)
    product_in_stock = models.FloatField(blank=True, null=True)      #庫存數量
    image = models.ImageField(upload_to='./static/product_images', storage=ImageStorage())
    image2 = models.ImageField(upload_to='./static/product_images', storage=ImageStorage())
    image3 = models.ImageField(upload_to='./static/product_images', storage=ImageStorage())
    info = models.TextField(blank=True, null=True) 
    purchase_date = models.DateTimeField(auto_now_add=False)         #進貨日
    updated = models.DateTimeField(auto_now_add=False)                                  
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):     
        return '{}'.format(self.company_id) 

#售出資訊(log)
class ProductSelling(models.Model):
    id = models.AutoField(primary_key=True)                       
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE)
    product_id = models.IntegerField(blank=True, null=True)    
    company_name = models.CharField(blank=True, null=True ,max_length=50)         #公司名
    types = models.CharField(blank=True, null=True ,max_length=30)   #種類
    brand = models.CharField(blank=True, null=True ,max_length=50)   #品牌
    model = models.CharField(blank=True, null=True ,max_length=100)  #型號(編號)
    name = models.CharField(blank=True, null=True ,max_length=100)   #商品名

    selling_price = models.FloatField(blank=True, null=True)         #銷售單價
    selling_amount = models.FloatField(blank=True, null=True)        #售出數量
    selling_sum = models.FloatField(blank=True, null=True)           #總銷售額

    info = models.TextField(blank=True, null=True) 
    selling_date = models.DateTimeField(auto_now_add=False)         #售出日
    updated = models.DateTimeField(auto_now_add=False)                                  
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):     
        return '{}'.format(self.company_id) 