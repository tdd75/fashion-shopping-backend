from django.shortcuts import render


def chart(request):
    return render(request, 'chart/index.html')


def inbox(request):
    return render(request, 'inbox/index.html')
