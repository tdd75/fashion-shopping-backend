from django.db.models import Count
from django.utils import timezone
from django.db import models
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.db.models.functions import TruncMonth

from orders.models import Order


class AnalyticAdminAPIView(views.APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        queryset = Order.objects.filter(stage=Order.Stage.COMPLETED)
    
        revenue_data = queryset.annotate(month=TruncMonth('created_at')).values(
            'month').annotate(value=models.Sum('amount')).values('month', 'value')
        order_data = queryset.annotate(month=TruncMonth('created_at')).values(
            'month').annotate(value=models.Count('pk')).values('month', 'value')

        return Response({
            'revenue': revenue_data,
            'order': order_data,
        }, status=status.HTTP_200_OK)
