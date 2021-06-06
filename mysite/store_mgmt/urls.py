from django.conf.urls import url
from store_mgmt import views
from django.urls import path


urlpatterns = [
    path('', views.login),
    path('logout/', views.logout),
    path('home/', views.home),
    #UserControl
    path('create_user/', views.UserControl().create_user),        
    path('user_control/', views.UserControl().user_control),
    path('user_control/update_user/', views.UserControl().update_user),
    path('user_control/delete_user/', views.UserControl().delete_user),
    #User
    path('user/update_user/', views.User().update_user),   
    path('user/update_user_password/', views.User().update_user_password),   
    #Company
    path('company/create_company/', views.Company().create_company), 
    path('company/company_list/', views.Company().company_list),  
    path('company/get_update_company/', views.Company().get_update_company), 
    path('company/update_company/', views.Company().update_company), 
    path('company/delete_company/', views.Company().delete_company), 
    #CompanyProduct
    path('company/create_company_product/', views.Company().create_company_product), 
    path('company/get_company_product_types/', views.Company().get_company_product_types), 
    path('company/get_company_product_brand/', views.Company().get_company_product_brand), 
    path('company/get_company_product_model/', views.Company().get_company_product_model), 
    path('company/get_company_product_name/', views.Company().get_company_product_name), 

    path('company/company_product_list/', views.Company().company_product_list), 
    path('company/get_update_company_product/', views.Company().get_update_company_product), 
    path('company/update_company_product/', views.Company().update_company_product), 
    path('company/delete_company_product/', views.Company().delete_company_product), 

    #Purchase
    path('product/create_purchase_product/', views.Purchase().create_purchase_product), 

]
