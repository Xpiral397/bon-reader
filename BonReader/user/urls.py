from django.urls import path
from .views import CustomActivationView

urlpatterns = [
    path('activate/', CustomActivationView.as_view(), name='custom-activate'),
]


