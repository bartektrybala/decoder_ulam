#!/usr/bin/env python3
import copy
import random
import re


ORIGINAL_TEXT = """This is a long looong test sentence,\nwith some big (biiiiig) words!"""
no_punctation_token = re.compile(r'(\w+)', re.U)


def encode(original_text):
    """
    Function shuffles the middle of every word in the original text.

    * In while loop check if shuffled word is different than original
    to ensure that every possible word is shuffled correctly.

    Returns shuffled text and sorted list of original words.
    """
    words = re.split(no_punctation_token, original_text)
    shuffled_original_worlds = []
    for i, word in enumerate(words):
        # 4 digits is minimum to make shuffle possibly
        # skip punctations marks
        if len(word) < 4 or re.match(no_punctation_token, word) is None:
            continue
        middle_of_the_word = word[1:-1]
        # check if middle of the word doesn't contains repeated one letter
        if middle_of_the_word == len(middle_of_the_word) * middle_of_the_word[0]:
            continue

        original_word = copy.copy(word)
        while word == original_word:
            random_middle = ''.join(random.sample(middle_of_the_word, len(middle_of_the_word)))
            word = word[0] + random_middle + word[-1]
        words[i] = word
        shuffled_original_worlds.append(original_word)

    encoded_text = "".join(words)
    return encoded_text, sorted(shuffled_original_worlds, key=lambda s: s.lower())


def decode(encoded_text, world_list):
    decoded_text = ""
    return decoded_text


if __name__ == "__main__":
    encoded_text, word_list = encode(ORIGINAL_TEXT)
    print(ORIGINAL_TEXT)
    print("Encoded Text:")
    print("\n--weird--\n")
    print(encoded_text)
    print("\n--weird--\n")
    print(word_list)
    decoded_text = decode(encoded_text, word_list)
    print("Decoded Text::\n")
    print(decoded_text)
