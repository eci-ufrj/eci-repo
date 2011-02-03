# -*- coding: utf-8 -*-
from unicodedata import normalize
from eci.resources.models import *

STRIP_WORDS = ['um','e','pelo','de','em','no','na','ou','que','com','para']

def _prepare_words(search_text):
    words = search_text.split()
    for common in STRIP_WORDS:
        if common in words:
            words.remove(common)
    return words[0:5]


_table = { 
    "á" : "a", "à" : "a", "â" : "a", "ä" : "a", "ã" : "a", "å" : "a",
    "é" : "e", "è" : "e", "ê" : "e", "ë" : "e",
    "í" : "i", "ì" : "i", "î" : "i", "ï" : "i",
    "ó" : "o", "ò" : "o", "ô" : "o", "ö" : "o", "õ" : "o", "ø" : "o", 
    "ú" : "u", "ù" : "u", "û" : "u", "ü" : "u",
    "ñ" : "n", "ç" : "c",
    "Á" : "A", "À" : "A", "Â" : "A", "Ä" : "A", "Ã" : "A", "Å" : "A",
    "É" : "E", "È" : "E", "Ê" : "E", "Ë" : "E", 
    "Í" : "I", "Ì" : "I", "Î" : "I", "Ï" : "I", 
    "Ó" : "O", "Ò" : "O", "Ô" : "O", "Ö" : "O", "Õ" : "O", "Ø" : "O",
    "Ú" : "U", "Ù" : "U", "Û" : "U", "Ü" : "U", 
    "Ñ" : "N", "Ç" : "C",
    "ß" : "ss", "Þ" : "d" , "æ" : "ae"
}


def asciize(s):
    """ 
    Converts a entire string to a ASCII only string.
   
    string
        The string to be converted.
    """
    for original, plain in _table.items():
        s = s.replace(original, plain)
    return s
