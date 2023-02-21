from django.urls import path

from .views import AnalyticAdminAPIView

urlpatterns = [
    path('', AnalyticAdminAPIView.as_view(), name='analytic'),
]
