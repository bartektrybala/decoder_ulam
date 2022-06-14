import copy
import json
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from encoder.views import EncodeApi, DecodeApi
from encoder.encoder import weirdtext_encoder, weirdtext_decoder,\
    SEPARATOR, extract_encoded_text


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


class TestEncoderMechanism(TestCase):
    """
    Test if encoder algorithm is implement with correct functionals.
    """
    def test_correct_words(self):
        """
        Test if encoder shuffle suitable words.
        """
        text_where_all_words_should_shuffled = "Text where words should shuffled"
        encoded_text, word_list = weirdtext_encoder(text_where_all_words_should_shuffled)
        original_words = text_where_all_words_should_shuffled.split()
        # check if all words from text are in result
        assert sorted(original_words, key=lambda s: s.lower()) == word_list
        # check if every word is shuffled
        assert not any(enc == org for enc, org in zip(encoded_text.split(), original_words))

    def test_three_letter_word(self):
        """
        Test if encoder doesn't shuffle three letter word.
        """
        three_letter_word = "cat"
        encoded_text, word_list = weirdtext_encoder(three_letter_word)
        assert encoded_text == SEPARATOR + three_letter_word + SEPARATOR
        assert word_list == []

    def test_one_letter_middle_repeated(self):
        """
        Test if encoder doesn't shuffle word with repeated
        the same letter in the middle.
        """
        repeated_one_letter_middle = "hoooot"
        encoded_text, word_list = weirdtext_encoder(repeated_one_letter_middle)
        assert encoded_text == SEPARATOR + repeated_one_letter_middle + SEPARATOR
        assert word_list == []

    def test_punctation_marks_string(self):
        """
        Test string with punctation marks.
        Check if word was shuffled correctly and punctation marks remained unchanged.
        """
        correct_word = "word"
        only_punctation_string = f"./,;']{correct_word}...,,,=-)()!\n\n!!"
        encoded_text, word_list = weirdtext_encoder(only_punctation_string)
        encoded_text = extract_encoded_text(encoded_text)

        # get shuffled word
        encoded_correct_word = extract_encoded_text(weirdtext_encoder(correct_word)[0])
        assert encoded_text == f"./,;']{encoded_correct_word}...,,,=-)()!\n\n!!"
        assert word_list == [correct_word]


class TestDecoderMechanism(TestCase):
    """
    Test if decoder algorithm is implement with correct functionals.
    """
    def test_correct_cycle_encode_decode(self):
        """
        Test if decoder correctly decodes encoded text.
        """
        encoded_text, word_list = weirdtext_encoder(TEST_ORIGINAL_TEXT)
        decoded_text = weirdtext_decoder(encoded_text, word_list, TEST_ORIGINAL_TEXT)
        assert decoded_text == TEST_ORIGINAL_TEXT

    def test_decode_with_punctation_marks(self):
        """
        Test if decoder correctly decodes text that contains punctation marks.
        """
        text_with_puncation = "This is (text), with many. puntation marks (e.i. big!)."
        encoded_text, word_list = weirdtext_encoder(text_with_puncation)
        decoded_text = weirdtext_decoder(encoded_text, word_list, text_with_puncation)
        assert decoded_text == text_with_puncation

    def test_raises_error_for_incorrect_input(self):
        """
        Test if decoder raises error when given encoded_text with word_list
        doesn't map on decoder output from original text.
        """
        # incorrect `word_list`
        encoded_text, word_list = weirdtext_encoder(TEST_ORIGINAL_TEXT)
        word_list.append("additional_word")
        with self.assertRaisesMessage(ValueError, "Incorrect encoded text."):
            weirdtext_decoder(encoded_text, word_list, TEST_ORIGINAL_TEXT)

        # incorrect `encoded_text`
        encoded_text, word_list = weirdtext_encoder(TEST_ORIGINAL_TEXT)
        encoded_text += "add"
        with self.assertRaisesMessage(ValueError, "Incorrect encoded text."):
            weirdtext_decoder(encoded_text, word_list, TEST_ORIGINAL_TEXT)
