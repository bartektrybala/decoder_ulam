from django.urls import re_path
from .swagger import WeridTextSchema


urlpatterns = [
    re_path(r'^swagger/$', WeridTextSchema.with_ui('swagger', cache_timeout=0)),
]
