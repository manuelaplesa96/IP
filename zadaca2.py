""" 
Podržane naredbe                         
ako je uvjet naredba inače naredba  ###ime = izraz
ako je uvjet naredba                ###ime = uvjet
ako nije uvjet naredba              vrati = izraz    
dok je uvjet naredba                vrati = uvjet
dok nije uvjet naredba              (naredba1, naredba2, ...)

pretvori u broj
pretvori u string

Podržani aritmetički izrazi         Podržani stringovski izrazi
broj                                string
izraz + izraz                       izraz+izraz (konkatenacija)
izraz - izraz                       
izraz * izraz
izraz / izraz

Podržani logički izrazi
izraz < izraz
izraz > izraz
izraz <= izraz
izraz >= izraz
izraz = izraz
izraz != izraz
"""

from py import *

class DZ2():
    AKO, DOK, INAČE, VRATI = 'ako', 'dok', 'inače', 'vrati'
    JE, NIJE = 'je','nije'
    OTV, ZATV, ZAREZ, JEDNAKO, MANJE, VEĆE = '(),=<>'
    NJEDNAKO, MJEDNAKO, VJEDNAKO = '!=', '<=', '>='
    PLUS, MINUS, PUTA, KROZ = '+-*/'
