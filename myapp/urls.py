from django.urls import path
from myapp import views
from django.urls import include

app_name = 'techavant'
urlpatterns = [
 path(r'', views.index, name='index'),
 path(r'about/', views.about, name='about'),
 path(r'<int:cat_no>/', views.detail, name='Category'),
 path(r'products/', views.products, name='product'),
 path(r'place_order/', views.place_order),
 path(r'products/<int:prod_id>', views.productdetail),
 path(r'login/', views.user_login, name='login'),
 path(r'logout/', views.user_logout, name='logout'),
 path(r'myorders/', views.myorders, name='myorders'),
 path(r'register/', views.register, name='register'),
 path(r'test', views.test, name='test'),
 path(r'json', views.json, name='json'),
 path(r'forgot_password/', views.forgot_password, name='forgot_password')

]