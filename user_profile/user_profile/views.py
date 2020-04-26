from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


def home(request):
    """Home page"""
    # if request.user.is_authenticated():
        # return HttpResponseRedirect(reverse('accounts:profile'))
    return render(request, 'home.html')
