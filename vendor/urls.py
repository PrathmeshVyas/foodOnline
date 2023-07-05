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
    path('menu_builder/food/edit/<int:pk>/', views.edit_food, name='edit_food'),
    path('menu_builder/food/delete/<int:pk>/', views.delete_food, name='delete_food'),
    # opening hour crud
    path('opening_hour/', views.opening_hours, name='opening_hours'),
    path('opening_hour/add/', views.add_opening_hours, name='add_opening_hours'),
    path('opening_hour/remove/<int:pk>/', views.remove_opening_hours, name='remove_opening_hours'),
]   