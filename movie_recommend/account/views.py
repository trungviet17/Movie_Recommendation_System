from django.shortcuts import render
from .form import UserEditForm, UserRegistrationForm, ProfileForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.


"""Hàm view cho màn hình đăng kí tài khoản của người dùng """
def register(request) :
    
    if request.method == 'POST': 
        userform  = UserRegistrationForm(request.POST)

        if userform.is_valid() : 

            new_user = userform.save(commit = False)
            new_user.set_password(userform.cleaned_data['password'])
            new_user.save()

            Profile.objects.create(user = new_user)

            return render(request, 'account/register_done.html', {'new_user' : new_user})


    else : 
        userform = UserRegistrationForm()

    return render(request, 'account/register.html', {'userform' : userform})

    


@login_required
def edit(request): 

    if request.method == 'POST': 
        user_form = UserEditForm(instance=request.user, data = request.POST)
        profile_form = ProfileForm(instance = request.user.profile, 
                                   data = request.POST, 
                                   files = request.FILE)

        if user_form.is_valid() and profile_form.is_valid() : 
            user_form.save()
            profile_form.save()

            messages.success(request, 'Profile update sucessfully')

        else : 
            messages.error(request, "Error updating your profile")

    else : 
        user_form = UserEditForm(instance=request.user)
        profile_form  = ProfileForm(instance=request.user)

    context = {'user_form' : user_form, 'profile_form' : profile_form}

    return render(request, 'account/edit.html',  context)


    

def dashboard(request): 
    
    return render(request, 'account/dashboard.html')