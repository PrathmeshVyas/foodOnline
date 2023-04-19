from accounts.forms import UserForm
from vendor.forms import VendorForm
from accounts.models import User, UserProfile
from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .utils import detectUser
from django.core.exceptions import PermissionDenied
# Create your views here.

#restrict vendor from accessing cust dashboard
def check_role_vendor(user):
    if user.role==1:
        return True
    else:
        raise PermissionDenied

#restrict cust from accessing vendor dashboard
def check_role_customer(user):
    if user.role==2:
        return True
    else:
        raise PermissionDenied

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'already logged in')
        return redirect('dashboard')
    elif request.method == 'POST':
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
    if request.user.is_authenticated:
        messages.warning(request, 'already logged in')
        return redirect('dashboard')
    elif request.method == "POST":
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
    

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'already logged in')
        return redirect('myAccount')
    elif request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'logged in successfully')
            return redirect('myAccount')
        else:
            messages.error(request, 'invalid credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')   

def logout(request):
    auth.logout(request)
    messages.info(request, 'you are logged out')
    return redirect('login')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')

@login_required(login_url='login')
def myAccount(request):
    user=request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')