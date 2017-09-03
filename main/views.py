# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
import re

# Create your views here.
def main(request):
    if (request.user.is_authenticated()):
        user=request.user
        email=user.email
        tail = email.split('@')[1]
        if not re.match(tail, 'pilani.bits-pilani.ac.in'):
            logout(request)
            return HttpResponseRedirect('/')
            
        else:
            return render(request,'main/front.html')
    else:
        return render(request,'main/front.html')