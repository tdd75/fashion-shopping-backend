from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import Http404

from custom_users.models import CustomUser

def chart(request):
    user = request.user
    token = RefreshToken.for_user(request.user).access_token
    if not user.is_staff or not token:
        raise Http404
    
    return render(request, 'chart/index.html', {
        'access': token
    })


def inbox(request):
    user = request.user
    token = RefreshToken.for_user(request.user).access_token
    if not user.is_staff or not token:
        raise Http404
    
    return render(request, 'inbox/index.html', {
        'access': token
    })
