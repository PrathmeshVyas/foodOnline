from django.shortcuts import render, redirect
from accounts.forms import UserProfileForm, UserInfoForm
from django.contrib.auth.decorators import login_required 
from accounts.models import UserProfile
from django.shortcuts import get_object_or_404
from django.contrib import messages


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