from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken

from custom_users.models import CustomUser

def chart(request):
    return render(request, 'chart/index.html', {
        'access': RefreshToken.for_user(request.user).access_token
    })


def inbox(request):
    print()
    return render(request, 'inbox/index.html', {
        'access': RefreshToken.for_user(request.user).access_token
    })
