from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


from .views import EncodeApi, DecodeApi

urlpatterns = [
    path('encode/', EncodeApi.as_view()),
    path('decode/', DecodeApi.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)