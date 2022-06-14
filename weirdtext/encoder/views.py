from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .encoder import weirdtext_encoder, weirdtext_decoder


class EncodeApi(APIView):
    """
    Encode the given message.

    Parameters:
        :original_text - text to encode

    Return
        :encoded_text - encoded text message
        :word_list - sorted list of original words, contains only words which were shuffled

    Example:
        POST /v1/encode/
        "original_text": "This is a long looong test sentence,\nwith some big (biiiiig) words!"
    """
    @swagger_auto_schema(
        responses={
            422: 'missing data parameters',
            400: 'incorrect data',
            201: 'encoded text message and sorted list of original words'
        }
    )
    def post(self, request):
        if not "original_text" in request.data.keys():
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if not isinstance(request.data['original_text'], str):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        encoded_text, word_list = weirdtext_encoder(request.data['original_text'])
        return Response(
            data={
                "encoded_text": encoded_text,
                "word_list": word_list,
            }
        )



class DecodeApi(APIView):
    """
    Decode the given message.

    Parameters:
        :encoded_text - encoded text message
        :word_list - sorted list of original words, contains only words which were shuffled
        :original_text - original message to check if encoded correctly

    Return
        :decoded_text - decoded text message

    Example:
        POST /v1/decode/
        "encoded_text": "\n--weird--\nTihs is a lnog loonog tset seentcne,\nwtih\
            smoe big (biiiiig) wrods!\n--weird--\n",
        "word_list": [
            "long",
            "looong",
            "sentence",
            "some",
            "test",
            "This",
            "with",
            "words"
        ]
        "original_text": "This is a long looong test sentence,\nwith some big (biiiiig) words!",
    """
    @swagger_auto_schema(
        responses={
            422: 'missing data parameters',
            400: 'incorrect data',
            201: 'decoded text message'
        }
    )
    def post(self, request):
        if any(x not in request.data.keys()\
            for x in ("encoded_text", "word_list", "original_text")):
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if not isinstance(request.data['encoded_text'], str)\
            or not isinstance(request.data['word_list'], list)\
            or not isinstance(request.data['original_text'], str):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded_text = weirdtext_decoder(request.data['encoded_text'],\
                request.data['word_list'], request.data['original_text'])
            return Response(
                data={
                    "decoded_text": decoded_text,
                }
            )
        except ValueError:
            return Response("Incorrect encoded text", status=status.HTTP_400_BAD_REQUEST)
