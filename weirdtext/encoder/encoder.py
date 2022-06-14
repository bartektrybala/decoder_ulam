#!/usr/bin/env python3
import copy
import random
import re


ORIGINAL_TEXT = """This is a long looong test sentence,\nwith some big (biiiiig) words!"""
no_punctation_token = re.compile(r'(\w+)', re.U)
SEPARATOR = "\n--weird--\n"

def word_suitable_for_shuffle(word):
    """
    Filter out punctation marks and words that contain in the middle
    repeating one letter(e.g `biiiig`)
    """
    # 4 digits is minimum to make shuffle possibly
    # skip punctations marks
    if len(word) < 4 or re.match(no_punctation_token, word) is None:
        return False
    middle_of_the_word = word[1:-1]
    # check if middle of the word doesn't contains repeated one letter
    if middle_of_the_word == len(middle_of_the_word) * middle_of_the_word[0]:
        return False
    return True


def weirdtext_encoder(original_text):
    """
    Function shuffles the middle of every word in the original text.

    * In while loop check if shuffled word is different than original
    to ensure that every possible word is shuffled correctly.
    * random.seed(30) is set to ensure that the text will always be encoded the same
    because checks in `decoder` function require that.

    Returns shuffled text and sorted list of original words.
    """
    random.seed(30)
    words = re.split(no_punctation_token, original_text)
    shuffled_original_worlds = []
    for i, word in enumerate(words):
        if word_suitable_for_shuffle(word):
            middle_of_the_word = word[1:-1]
            original_word = copy.copy(word)
            while word == original_word:
                random_middle = ''.join(random.sample(middle_of_the_word, len(middle_of_the_word)))
                word = word[0] + random_middle + word[-1]
            words[i] = word
            shuffled_original_worlds.append(original_word)

    encoded_text = SEPARATOR + "".join(words) + SEPARATOR
    return encoded_text, sorted(shuffled_original_worlds, key=lambda s: s.lower())

def extract_encoded_text(encoded_text):
    """Return text between two separators."""
    return re.sub(SEPARATOR, '', encoded_text)

def weirdtext_decoder(encoded_text, word_list, original_text):
    """
    Function decodes given encoded_text based on given word_list.
    """
    # Check encoded_text looks like composite output of encoder
    if (encoded_text, word_list) != weirdtext_encoder(original_text):
        raise ValueError("Incorrect encoded text.")

    def _decode_with_map(word, word_list):
        """
        Auxliary function for decode word with mapping on given word_list.
        Funtion iterate through given original word_list and try to map
        encoded word on the original one based on conditions.

        Base conditions to map two words (must always occur):
            - the same letters on the edges,
            - the same length
        Case 1:
            - any of the remaining words with the same length
            doesn't have the same letters one the edges
        Case 2:
            - middle of two words contains the same letters
        Any other cases return False
        """
        for possible_word in word_list:
            # if first and last letter in word are equal but not in the rest of the words with the same length
            if word[0] == possible_word[0] and word[-1] == possible_word[-1] and len(word) == len(possible_word):
                if not any((word[0] == w[0] and word[-1] == w[-1])\
                    for w in word_list if w != possible_word and len(word) == len(w)):
                    return possible_word, True
                else:
                    # compare middle of the word contains the same letters
                    middle_word, middle_possible_word = word[1:-1], possible_word[1:-1]
                    if sorted(middle_word) == sorted(middle_possible_word):
                        return possible_word, True
        return "", False

    encoded_text = extract_encoded_text(encoded_text)
    encoded_words = re.split(no_punctation_token, encoded_text)
    for i, e_word in enumerate(encoded_words):
        if word_suitable_for_shuffle(e_word):
            possible_encoded_word, _found = _decode_with_map(e_word, word_list)
            if _found:
                encoded_words[i] = possible_encoded_word
                word_list.remove(encoded_words[i])
    decoded_text = "".join(encoded_words)
    return decoded_text


if __name__ == "__main__":
    encoded_text, word_list = weirdtext_encoder(ORIGINAL_TEXT)
    print(ORIGINAL_TEXT)
    print("Encoded Text::")
    print(encoded_text)
    print(word_list)
    decoded_text = weirdtext_decoder(encoded_text, word_list, ORIGINAL_TEXT)
    print("\n\nDecoded Text::\n")
    print(decoded_text)
