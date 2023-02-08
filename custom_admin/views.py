from django.shortcuts import render
from custom_users.models import CustomUser


def chart(request):
    return render(request, 'chart/index.html', {
    })


def inbox(request):
    users = CustomUser.objects.all()
    return render(request, 'inbox/index.html', {
        'users': users,
    })
