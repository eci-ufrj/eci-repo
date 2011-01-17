from eci.resources.models import *

STRIP_WORDS = ['um','e','pelo','de','em','no','na','ou','que','com','para']

def _prepare_words(search_text):
    words = search_text.split()
    for common in STRIP_WORDS:
        if common in words:
            words.remove(common)
    return words[0:5]