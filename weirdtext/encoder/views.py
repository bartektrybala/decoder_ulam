from django.shortcuts import render
from django.http import Http404
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
    """
    def post(self, request, format=None):
        if not "original_text" in request.data.keys():
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        elif not isinstance(request.data['original_text'], str):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            encoded_text, word_list = weirdtext_encoder(request.data['original_text'])
            return Response(
                data={
                    "encoded_text": encoded_text,
                    "word_list": word_list,
                }
            )
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        


class DecodeApi(APIView):
    """
    Decode the given message.
    
    Parameters:
        :encoded_text - encoded text message
        :word_list - sorted list of original words, contains only words which were shuffled
        :original_text - original message to check if encoded correctly

    Return
        :decodeed_text - decoded text message
    """
    def post(self, request, format=None):
        if any(x not in request.data.keys() for x in ("encoded_text", "word_list", "original_text")):
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        elif not isinstance(request.data['encoded_text'], str) or not isinstance(request.data['word_list'], list):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded_text = weirdtext_decoder(request.data['encoded_text'], request.data['word_list'], request.data['original_text'])
            return Response(
                data={
                    "decoded_text": decoded_text,
                }
            )
        except ValueError:
            return Response("Incorrect encoded text", status=status.HTTP_400_BAD_REQUEST)
