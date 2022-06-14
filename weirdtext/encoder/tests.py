import json
import copy
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from encoder.views import EncodeApi, DecodeApi
from encoder.encoder import weirdtext_encoder, weirdtext_decoder


TEST_ORIGINAL_TEXT = "This is a short (test) sentence,\nbut different than in task.\
    Sentence doesn't contain important words big and biiig!"


class ApiEncodeTest(TestCase):
    """
    Test if enccode views response correct data and handles errors.
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = EncodeApi.as_view()
        self.encoded_text, self.word_list = weirdtext_encoder(TEST_ORIGINAL_TEXT)

    def test_encode_api(self):
        """
        Test encode api endpoint for test text.
        Check validation for data in response.
        """
        data = {
            "original_text": TEST_ORIGINAL_TEXT
        }
        request = self.factory.post("/v1/encode/", json.dumps(data),\
            content_type="application/json")
        response = self.view(request)

        assert response.status_code == 200
        assert 'encoded_text' in response.data
        assert isinstance(response.data['encoded_text'], str)
        assert 'word_list' in response.data
        assert isinstance(response.data['word_list'], list)
        assert self.encoded_text, self.word_list == weirdtext_encoder(TEST_ORIGINAL_TEXT)

    def test_error_raises(self):
        """
        Test if endpoint response raises correct errors for invalid data.
        """
        # without `original_text`
        request = self.factory.post("/v1/encode/", {}, content_type="application/json")
        response = self.view(request)
        assert response.status_code == 422

        # with incorrect `original_text`
        request = self.factory.post("/v1/encode/", {"original_mtext": 1},\
            content_type="application/json")
        response = self.view(request)
        assert response.status_code == 400


class ApiDecodeTest(TestCase):
    """
    Test if decode views response correct data and handles errors.
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = DecodeApi.as_view()
        self.encoded_text, self.word_list = weirdtext_encoder(TEST_ORIGINAL_TEXT)
        self.data = {
            "encoded_text": self.encoded_text,
            "word_list": self.word_list,
            "original_text": TEST_ORIGINAL_TEXT,
        }

    def test_decode(self):
        """
        Test encode api endpoint for test text.
        Check validation for data in response.
        """
        request = self.factory.post("/v1/decode/", json.dumps(self.data),\
            content_type="application/json")
        response = self.view(request)

        assert response.status_code == 200
        assert 'decoded_text' in response.data
        assert isinstance(response.data['decoded_text'], str)
        assert response.data['decoded_text'] == \
        weirdtext_decoder(self.encoded_text, self.word_list, TEST_ORIGINAL_TEXT)

    def test_error_raises_encoded_text(self):
        """
        Test if endpoint response raises correct errors for invalid data.
        """
        # without `encoded_text`
        data_without_encoded_text = copy.copy(self.data)
        data_without_encoded_text.pop("encoded_text")
        request = self.factory.post("/v1/encode/", json.dumps(data_without_encoded_text),\
            content_type="application/json")
        response = self.view(request)
        assert response.status_code == 422

        # with incorrect `encoded_text`
        data_without_encoded_text['encoded_text'] = 1
        request = self.factory.post("/v1/encode/", json.dumps(data_without_encoded_text),\
            content_type="application/json")
        response = self.view(request)
        assert response.status_code == 400

    def test_error_raises_word_list(self):
        # without `word_list`
        data_without_word_list = copy.copy(self.data)
        data_without_word_list.pop("word_list")
        request = self.factory.post("/v1/encode/", json.dumps(data_without_word_list),\
            content_type="application/json")
        response = self.view(request)
        assert response.status_code == 422

        # with incorrect `word_list`
        data_without_word_list['word_list'] = "string"
        request = self.factory.post("/v1/encode/", json.dumps(data_without_word_list),\
            content_type="application/json")
        response = self.view(request)
        assert response.status_code == 400

    def test_error_raises_original_text(self):
        # without `original_text`
        data_without_original_text = copy.copy(self.data)
        data_without_original_text.pop("original_text")
        request = self.factory.post("/v1/encode/", json.dumps(data_without_original_text),\
        content_type="application/json")
        response = self.view(request)
        assert response.status_code == 422

        # with incorrect `encoded_text`
        data_without_original_text['original_text'] = {"12": 12}
        request = self.factory.post("/v1/encode/", json.dumps(data_without_original_text),\
        content_type="application/json")
        response = self.view(request)
        assert response.status_code == 400
