"""my_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from my_app import views

urlpatterns = [
    path('',views.login,name='login'),
    path('register',views.register,name='register'),
    path("c_password",views.c_password,name="c_password"),
    path("logout",views.logout,name="logout"),
    path("projects",views.projects,name="projects"),
    path("search",views.search,name="search"),
    path("all_list",views.all_list,name="all_list"),
    path("delete/<int:pk>/",views.delete,name="delete"),
    path("search_employe",views.search_employe,name="search_employe"),
    path("attendance_Hr",views.attendance_Hr,name="attendance_Hr"),
    path("salary",views.salary,name="salary"),  
    path("Pay",views.initiate_payment,name="Pay"),
    path("callback/",views.callback,name="callback"),
    path("CB",views.CB,name="CB"),
    path("update/<int:pk>/",views.update,name="update"),

    path("Performance",views.Performance,name="Performance"),

    path("valid_name/",views.valid_name,name="valid_name"),
    path("puch_in/",views.puch_in,name="puch_in"),
    path("puch_out/",views.puch_out,name="puch_out"),

    path("attendance_employe/",views.attendance_employe,name="attendance_employe"),

    path("contacts/",views.contacts,name="contacts"),
    path("download/",views.download,name="download"),
    path("uid/",views.uid,name="uid"),
    
    

    path("file_manager/",views.file_manager,name="file_manager"),
    path("re_search",views.re_search,name="re_search"),
    path("profile",views.profile,name="profile"),
    path("change_password_profile",views.change_password_profile,name="change_password_profile"),
    
    # path("button",views.button,name="button"),
    
   
    

    
    
    




    
    

]
