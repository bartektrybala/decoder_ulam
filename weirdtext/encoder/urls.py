from django.urls import path

from .views import EncodeApi, DecodeApi

urlpatterns = [
    path('encode/', EncodeApi.as_view()),
    path('decode/', DecodeApi.as_view()),
]
