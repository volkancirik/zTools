from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from cross_order.helper_functions import render_response
from zerd_app.userprofile.forms import RegisterForm, LoginForm
from zerd_app.userprofile.models import Profile

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['email'] , form.cleaned_data['email'], form.cleaned_data['password'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.is_active = False
            user.save()
            profile = Profile(user=user)
            profile.save()
            
            return render_response(request, 'userprofile/login_or_register.html', {'register_form': form, 'login_form':LoginForm(),'register_success':True})
        else:
            return render_response(request, 'userprofile/login_or_register.html', {'register_form': form, 'login_form':LoginForm()})
    else:
        return render_response(request, 'userprofile/login_or_register.html', {'register_form': RegisterForm(), 'login_form':LoginForm()})

def user_login(request):
    if request.user.is_authenticated():
        return redirect('/cross_order/list_supplier/')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email'].strip()
            password = request.POST['password']

            user = authenticate(email=email, password=password)

            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('/cross_order/list_supplier/')
                else:
                    return render_response(request, 'userprofile/login_or_register.html', {'user_inactive': True,'register_form': RegisterForm(), 'login_form':LoginForm()})
        else:
            return render_response(request, 'userprofile/login_or_register.html',{'register_form': RegisterForm(), 'login_form':form})
    else:
        return render_response(request, 'userprofile/login_or_register.html', {'register_form': RegisterForm(), 'login_form':LoginForm()})