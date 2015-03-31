from django.contrib.auth import authenticate, login as auth_login, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.utils.http import is_safe_url
from jumpstart import settings
from jumpstart.apps.accounts.forms import SignupForm, LoginForm
from jumpstart.apps.home.models import sort_ideas


def login(request):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(REDIRECT_FIELD_NAME,
                                   request.GET.get(REDIRECT_FIELD_NAME, ''))

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            # If user specifies remember me, allow their session to persist after closing the browser
            if form.remember_user():
                request.session.set_expiry(settings.SESSION_COOKIE_AGE)

            return HttpResponseRedirect(redirect_to)
    else:
        form = LoginForm(request)
    return get_started(request, login_form=form)


def signup(request):
    """
    Displays the signup form and handles the signup action
    """
    redirect_to = request.POST.get(REDIRECT_FIELD_NAME,
                                   request.GET.get(REDIRECT_FIELD_NAME, ''))

    if request.method == 'POST':
        form = SignupForm(data=request.POST)
        if form.is_valid():
            user = form.save()

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, user)

            return HttpResponseRedirect(redirect_to)
    else:
        form = SignupForm()
    return get_started(request, signup_form=form)

def get_started(request, login_form=None, signup_form=None):
    login_form = LoginForm(request) if not login_form else login_form
    signup_form = SignupForm() if not signup_form else signup_form
    return render(request, 'accounts/get_started.html', {
        'login_form': login_form,
        'signup_form': signup_form,
    })

def render_user(request, user):
    return render(request, 'accounts/user.html', {
        'user': user,
        'user_ideas': sort_ideas(user.ideas.all())
    })


def user(request, pk):
    u = get_object_or_404(User, pk=pk)
    return render_user(request, u)


@login_required(login_url='get_started')
def profile(request):
    return render_user(request, request.user)