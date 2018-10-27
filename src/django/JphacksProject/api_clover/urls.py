from django.urls import path, include
from . import views

urlpatterns = [
    path(' ', views.clova, name='api_clover')
]
