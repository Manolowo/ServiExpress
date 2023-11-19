from django.urls import path
from . import views

urlpatterns=[
    path('', views.index, name="index"),

    path('login_view/', views.login_view, name='login_view'),
    
    path('cli_home/', views.cli_home, name='cli_home'),
    
    path('emp_home/', views.emp_home, name='emp_home'),
    
    path('adm_home/', views.adm_home, name='adm_home'),
    path('adm_users/', views.adm_users, name='adm_users'),
    path('add_user/', views.add_user, name='add_user'),
    path('delete_user/', views.delete_user, name='delete_user'),

]