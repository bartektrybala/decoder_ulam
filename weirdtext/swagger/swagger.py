from drf_yasg.openapi import Info, Schema, Items, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.views import get_schema_view


WeridTextSchema = get_schema_view(
   Info(
      title="Weirdtext API",
      default_version='v1',
   ),
   public=True,
   # empty for presentation
)

enccode_request_body = Schema(
   type=TYPE_OBJECT,
   properties={
      "original_text": Schema(type=TYPE_STRING, description='text to encode'),
   }
)

decode_request_body = Schema(
   type=TYPE_OBJECT,
   properties={
      "encoded_text": Schema(type=TYPE_STRING, description='encoded text message'),
      "word_list": Schema(type=TYPE_ARRAY, items=Items(type=TYPE_STRING),\
         description='sorted list of original words, contains only words which were shuffled'),
      "original_text": Schema(type=TYPE_STRING,\
         description='original message to check if encoded correctly'),
   }
)
