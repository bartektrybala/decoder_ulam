from drf_yasg.openapi import Info, Contact, Parameter, Items, IN_QUERY, TYPE_STRING, TYPE_ARRAY
from drf_yasg.views import get_schema_view


WEIRDTEXT_API_DESCRIPTION = "API description of Weirdtext decoder"

schema_view = get_schema_view(
   Info(
      title="Weirdtext API",
      default_version='v1',
      description=WEIRDTEXT_API_DESCRIPTION,
      contact=Contact(email="bartektrybalaa@gmail.com"),
   ),
   public=True,
   authentication_classes=[], # empty for presentation.
)

encoded_text_param = Parameter('encoded_text_param', IN_QUERY,\
        description="encoded text message", type=TYPE_STRING, required=True)
word_list = Parameter('word_list', IN_QUERY,\
    description="sorted list of original words, contains only words which were shuffled",\
    type=TYPE_ARRAY, items=Items(type=TYPE_STRING), required=True)
original_text = Parameter('original_text', IN_QUERY,\
    description="original message to check if encoded correctly", type=TYPE_STRING, required=True)