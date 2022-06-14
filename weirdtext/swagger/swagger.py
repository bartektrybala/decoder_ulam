from drf_yasg.openapi import Info, Contact
from drf_yasg.views import get_schema_view


WEIRDTEXT_API_DESCRIPTION = "API description of Weirdtext decoder"

WeridTextSchema = get_schema_view(
   Info(
      title="Weirdtext API",
      default_version='v1',
      description=WEIRDTEXT_API_DESCRIPTION,
      contact=Contact(email="bartektrybalaa@gmail.com"),
   ),
   public=True,
   # empty for presentation
   authentication_classes=[],
   permission_classes=[],
)
