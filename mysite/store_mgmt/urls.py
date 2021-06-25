from django.conf.urls import url
from store_mgmt import views
from django.urls import path


urlpatterns = [
    path('', views.login),
    path('logout/', views.logout),
    path('home/', views.home),
    path('sign_up/', views.sign_up),
    # Home
    path('home/realtime_content/', views.Home().realtime_content),
    path('home/revenue_status_content/', views.Home().revenue_status_content),
    path('home/hot_sale_content/', views.Home().hot_sale_content),
    path('home/main_revenue_content/', views.Home().main_revenue_content),

    #User Control
    path('create_user/', views.UserControl().create_user),        
    path('user_control/', views.UserControl().user_control),
    path('user_control/update_user/', views.UserControl().update_user),
    path('user_control/delete_user/', views.UserControl().delete_user),
    #User Update
    path('user/update_user/', views.User().update_user),   
    path('user/update_user_password/', views.User().update_user_password),   
    #Company
    path('company/create_company/', views.Company().create_company), 
    path('company/company_list/', views.Company().company_list),  
    path('company/get_update_company/', views.Company().get_update_company), 
    path('company/update_company/', views.Company().update_company), 
    path('company/delete_company/', views.Company().delete_company), 
    #Create Company Product
    path('company/create_company_product/', views.Company().create_company_product), 
    path('company/get_company_product_types/', views.Company().get_company_product_types), 
    path('company/get_company_product_brand/', views.Company().get_company_product_brand), 
    path('company/get_company_product_model/', views.Company().get_company_product_model), 
    path('company/get_company_product_name/', views.Company().get_company_product_name), 
    path('company/get_company_product/', views.Company().get_company_product), 
    #Company Product List
    path('company/company_product_list/', views.Company().company_product_list), 
    path('company/company_product_search/', views.Company().company_product_search), 
    path('company/get_update_company_product/', views.Company().get_update_company_product), 
    path('company/update_company_product/', views.Company().update_company_product), 
    path('company/delete_company_product/', views.Company().delete_company_product), 
    #Create Purchase
    path('purchase/create_purchase/', views.Purchase().create_purchase), 
    #Purchase List
    path('purchase/purchase_list/', views.Purchase().purchase_list), 
    path('purchase/purchase_search/', views.Purchase().purchase_search), 
    path('purchase/purchase_search_by_date/', views.Purchase().purchase_search_by_date), 
    path('purchase/get_update_purchase/', views.Purchase().get_update_purchase),
    path('purchase/update_purchase/', views.Purchase().update_purchase),
    path('purchase/delete_purchase/', views.Purchase().delete_purchase),
    #Create sale
    path('sale/create_sale/', views.Sale().create_sale), 
    path('sale/purchase_search/', views.Sale().purchase_search),   #建立銷售時使用
    #Sale List
    path('sale/sale_list/', views.Sale().sale_list),
    path('sale/sale_search/', views.Sale().sale_search),           #查詢 / 修改銷售時使用
    path('sale/sale_search_by_date/', views.Sale().sale_search_by_date),           #查詢 / 修改銷售時使用
    path('sale/get_update_sale/', views.Sale().get_update_sale),
    path('sale/update_sale/', views.Sale().update_sale),
    path('sale/delete_sale/', views.Sale().delete_sale),

]
