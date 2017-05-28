from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from users.forms_website import RegistrationForm
from users.models import User


def index(request):

    numbers_list = range(1, 1000)
    page = request.GET.get('page', 1)
    paginator = Paginator(numbers_list, 20)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)
    context = {
            'numbers': numbers
        }
    return render(request, 'website/index.html', context)


def login(request):
    context = {
    }
    return render(request, 'website/login.html', context)


def social_login(request):
    context = {
    }
    return render(request, 'website/login.html', context)


def logout(request):
    context = {
    }
    return render(request, 'website/logout.html', context)


def home(request):
    context = {
    }
    return render(request, 'website/home.html', context)


@csrf_exempt
# @csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/registration/success/')
        else:
            print(form.errors)
    else:
        form = RegistrationForm()
    context = RequestContext(request, {
        'form': form
    })

    return render_to_response(
        'website/registration/register.html',
        context,
    )


def register_success(request):
    context = {
    }
    return render(request, 'website/registration/success.html', context)
