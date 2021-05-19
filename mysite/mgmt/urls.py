from django.conf.urls import url
from mgmt import views
from django.urls import path


urlpatterns = [
    path('', views.login),
    path('logout/', views.logout),
    path('home/', views.home),
    path('product_list/', views.Product().product_list),
    path('create_product/', views.Product().create_product),
    path('product_update/', views.Product().product_update),
    path('create_company/', views.Company().create_company),
    path('company_list/', views.Company().company_list),
    path('company_update/', views.Company().company_update),


    path('company_product/', views.Company().company_product),
    path('get_company_product_types/', views.Company().get_company_product_types),
    path('get_company_product_brand/', views.Company().get_company_product_brand),
    path('get_company_product_model/', views.Company().get_company_product_model),
    path('get_company_product_name/', views.Company().get_company_product_name),

]
