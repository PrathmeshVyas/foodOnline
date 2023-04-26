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
    path('menu_builder/category/<int:pk>/', views.fooditems_by_category, name='fooditems_by_category'),
    # category crud
    path('menu_builder/category/add/', views.add_category, name='add_category'),
    path('menu_builder/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('menu_builder/category/delete/<int:pk>/', views.delete_category, name='delete_category'),
    #fooditems crud
    path('menu_builder/food/add/', views.add_food, name='add_food'),

]   