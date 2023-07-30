from django.shortcuts import render, redirect
from accounts.forms import UserProfileForm, UserInfoForm
from django.contrib.auth.decorators import login_required 
from accounts.models import UserProfile
from django.shortcuts import get_object_or_404
from django.contrib import messages
from orders.models import Order, OrderedFood
import json as simplejson

# Create your views here.
@login_required(login_url='login')
def cprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method=='POST':
        profile_form=UserProfileForm(request.POST, request.FILES, instance=profile)
        user_form=UserInfoForm(request.POST, request.FILES, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, "profile updated successfully")
            return redirect('cprofile')
        else:
            print(profile_form.errors)
            print(user_form.errors)
            
    else:
        profile_form=UserProfileForm(instance=profile)
        user_form = UserInfoForm(instance=request.user)

    context = {
        'profile_form':profile_form,
        'user_form':user_form
    }

    return render(request, 'customers/cprofile.html', context)

def customer_my_orders(request):
    orders=Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders':orders
    }
    return render(request, 'customers/myorders.html', context)

def order_detail(request, order_number):
    try:
        order=Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_food=OrderedFood.objects.filter(order=order)
        sub_total=0
        for item in ordered_food:
            sub_total=item.price*item.quantity
        tax_data=simplejson.loads(order.tax_data)        
        context = {
            'order':order,
            'ordered_food':ordered_food,
            'sub_total':sub_total,
            'tax_data':tax_data
        }
        return render(request, 'customers/order_detail.html', context)
    except:
        return redirect('customer')