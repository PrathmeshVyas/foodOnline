from accounts.forms import UserForm
from vendor.forms import VendorForm
from accounts.models import User, UserProfile
from django.contrib import messages
from django.shortcuts import render, redirect
# Create your views here.


def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # create user using create user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(
                first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            # create user using form
            # password = form.cleaned_data['password']
            # user=form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()
            messages.success(
                request, 'your account has been register successfully')
            return redirect('registerUser')
        else:
            print('invalid')
            print(form.errors)
    else:
        form = UserForm()

    context = {'form': form}
    return render(request, 'accounts/registerUser.html', context)


def registerVendor(request):
    if request.method == "POST":
        # store data and create User
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        print(v_form.data)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, 'your account has been register successfully! please wait for approval.')
            return redirect('registerVendor')
        else:
            print('invalid form')
            print(v_form.errors)
    else:   
        form = UserForm()
        v_form = VendorForm()       

    context = {'form': form, 'v_form': v_form}      

    return render(request, 'accounts/registerVendor.html', context)
    