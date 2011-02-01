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





def remover_acentos(txt, codif='utf-8'):

    ''' Devolve cópia de uma str substituindo os caracteres 
        acentuados pelos seus equivalentes não acentuados.
    
    ATENÇÃO: carateres gráficos não ASCII e não alfa-numéricos,
    tais como bullets, travessões, aspas assimétricas, etc. 
    são simplesmente removidos!
    
    >>> remover_acentos('[ACENTUAÇÃO] ç: áàãâä! éèêë? íì&#297;îï, óòõôö; úù&#361;ûü.')
    '[ACENTUACAO] c: aaaaa! eeee? iiiii, ooooo; uuuuu.'
    
    '''
    return normalize('NFKD', txt.decode(codif)).encode('ASCII','ignore')
    
if __name__ == '__main__':
    from doctest import testmod
    testmod()
