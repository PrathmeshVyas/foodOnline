from django.urls import path, include
from . import views
from accounts import views as Accountviews
from django.contrib import admin
admin.site.site_header='foodOnline'
admin.site.index_title='foodOnline administration'


urlpatterns = [
    path('', Accountviews.vendorDashboard, name='vendor'),
   path('vprofile/', views.vprofile, name='vprofile'),
   path('menu_builder/', views.menu_builder, name='menu_builder'),
]