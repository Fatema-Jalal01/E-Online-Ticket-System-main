"""ticket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signuppage,name='sign'),
    path('login', views.loginpage,name='login'),
    path('homey', views.homey,name='homey'),
    path('logout', views.logoutpage,name='logout'),
    path('train', views.train,name='train'),
    path('bus', views.bus,name='bus'),
    path('airplane', views.airplane,name='airplane'),
    path('term', views.term,name='term'),
    path('searchbus',views.bus,name='searchbus'),
    path('serachair',views.airplane,name='serachair'),
    path('searcht',views.train,name='searcht'),
    path('seat_selection/<str:bus_id>/', views.seat_selection, name='seat_selection'),
    path('train_seat_selection/<str:train_id>/', views.train_seat_selection, name='train_seat_selection'),
    path('plane_seat_selection/<str:air_id>/', views.plane_seat_selection, name='plane_seat_selection'),
    path('buspay/<str:bus_id>/', views.buspay, name='buspay'),
    path('pay_temp/<str:bus_id>/',views.pay_temp,name='pay_temp'),
    path('trainpay/<str:train_id>/', views.trainpay, name='trainpay'),
    path('train_pay_temp/<str:train_id>/',views.train_pay_temp,name='train_pay_temp'),
    path('planepay/<str:air_id>/', views.planepay, name='planepay'),
    path('plane_pay_temp/<str:air_id>/',views.plane_pay_temp,name='plane_pay_temp'),
    path('term', views.term,name='term'),
    path('about', views.about,name='about'),
    path('manual', views.manual,name='manual'),   
    path('confirm', views.confirm, name='confirm'),
    path('delete-seat/', views.delete_seat, name='delete_seat'),
    path('train_confirm/', views.train_confirm, name='train_confirm'),
    path('plane_confirm/', views.plane_confirm, name='plane_confirm'),
    path('train-delete-seat/', views.train_delete_seat, name='train_delete_seat'),
    path('plane-delete-seat/', views.plane_delete_seat, name='plane_delete_seat'),


]
#path('', views.homepage,name='homepage'),

#path('homey', views.homey,name='homey'),
#path('<int:bus_id>/',views.seat,name='seat'),
#path('seat_selection', views.seat_selection, name='seat_selection'),