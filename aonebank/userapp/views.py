from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from .forms import SignUpForm, User_form, ProfileForm
from .models import Profiles
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponsePermanentRedirect
from django.db import transaction
from django.contrib import messages


# Create your views here.
class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    
@login_required
def user_profile(request, userId):
    profile = Profiles.objects.all().filter(user_id = userId)
    return render(
        request = request, 
        template_name= "userapp/my_profile.html", 
        context ={"my_profile": profile}
    )
@login_required
@transaction.atomic
def edit_profile(request, userId):
    user = get_object_or_404(User, id= userId)
    if request.method == "POST":
        user_form = User_form(request.POST, instance = user)
        profile_form = ProfileForm(request.POST or None, request.FILES or None, instance = user.profiles)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            if profile_form.cleaned_data["staff"]:
                user.is_staff = True
            else:
                user.is_staff = False
                user.save()
            messages.success(request, ("Your profile was successfully update"))
            return HttpResponsePermanentRedirect(reverse("profile", args=(userId,)))
        
    else:
            user_form = User_form(instance = user)
            profile_form = ProfileForm(instance = user.profiles)
            return render (request, "userapp/profile_edit_form.html", {"user_form": user_form, "profile_form": profile_form})
        
        
def deactivate_profile(request, userId):
    user = User.objects.get(id=userId)
    if user.is_active:
        User.objects.filter(id=userId).update(is_active = False)
    else:
        User.objects.filter(id=userId).update(is_active = True)
    messages.success(request, ("Your profile was successfully updated"))
    return HttpResponsePermanentRedirect(reverse("profile", args=(userId)))

user_status = ""
@login_required
def display_users(request, status):
    global user_status
    user_status = status
    if status == "staff":
        allUsers = Profiles.objects.filter(staff= True)
    else:
        allUsers = Profiles.objects.filter(staff = False)
    return render(request, "userApp/display_users.html", {"allusers": allUsers, "status": status})

@login_required
def delete_profile(request, userId):
    Profiles.objects.filter(user_id = userId).delete()
    User.objects.filter(id= userId).delete()
    messages.success(request, ("Profile deleted succesfully!"))
    
    return HttpResponsePermanentRedirect(reverse("view_customers", args ={user_status,}))

        
        