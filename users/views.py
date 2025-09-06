from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

import orders
from carts.models import Cart
from shop import settings
from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm


# class LoginUser(LoginView):
#     form_class = LoginUserForm
#     template_name = 'users/login.html'
#     extra_context = {'title': 'Авторизация'}

    # def get_success_url(self):
    #     return reverse_lazy('home')



    # def get_success_url(self):
    #     return reverse_lazy('home')

def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])

            session_key = request.session.session_key

            if user:
                login(request, user)

                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)

                return HttpResponseRedirect(reverse('shop_app:home'))
    else:
        form = LoginUserForm()

    return render(request, 'users/login.html', {'form': form})




# class RegisterUser(CreateView):
#     form_class = RegisterUserForm
#     template_name = 'users/register.html'
#     extra_context = {'title': 'Регистрация'}

def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            session_key = request.session.session_key
            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = RegisterUserForm()
    return render(request, 'users/register.html', {'form': form})



# class RegisterUser(CreateView):
#     form_class = RegisterUserForm
#     template_name = 'users/register.html'
#     extra_context = {'title': 'Регистрация'}
#     success_url = reverse_lazy('users:login')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('shop_app:home'))

# def password_reset(request):
#     return render(request, 'users/password_reset_form.html', {'form': form})


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': "Профиль пользователя",
                     'default_image': settings.DEFAULT_USER_IMAGE,
    }

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
