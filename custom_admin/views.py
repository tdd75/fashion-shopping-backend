from django.shortcuts import render
from custom_users.models import CustomUser


from django.db import models
from django.db.models.functions import TruncMonth

from orders.models import Order


def chart(request):
    queryset = Order.objects.filter(stage=Order.Stage.COMPLETED)

    revenue_data = queryset.annotate(month=TruncMonth('created_at')).values(
        'month').annotate(value=models.Sum('transaction__paid_amount')).values('month', 'value')
    order_data = queryset.annotate(month=TruncMonth('created_at')).values(
        'month').annotate(value=models.Count('pk')).values('month', 'value')

    return render(request, 'chart/index.html', {
        'revenue': list(revenue_data),
        'order': list(order_data),
    })


def inbox(request):
    return render(request, 'inbox/index.html')
