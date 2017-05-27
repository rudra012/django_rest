from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect

from users.forms_website import RegistrationForm
from users.models import User


def home(request):
    context = {
    }
    return render(request, 'website/home.html', context)

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response(
        'website/register.html',
        variables,
    )


def login(request):
    context = {
    }
    return render(request, 'website/login.html', context)
