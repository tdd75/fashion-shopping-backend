from django.urls import path

from .views import chart, inbox

urlpatterns = [
    path('chart/', chart, name='chart'),
    path('inbox/', inbox, name='inbox'),
]
