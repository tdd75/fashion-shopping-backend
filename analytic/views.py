from django.db.models import Count
from django.utils import timezone
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from orders.models import Order


class AnalyticAdminAPIView(views.APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        queryset = Order.objects.filter(transaction__isnull=False)

        return Response({
            'revenue': [
                {
                    'month': timezone.datetime.now(),
                    'value': 100,
                }
            ]
        }, status=status.HTTP_200_OK)
