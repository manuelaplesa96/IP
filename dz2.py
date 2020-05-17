#jedan brojevni i jedan stringovni tip te jednostavna pridruživanja (varijabla poprima vrijednost izraza odgovarajućeg tipa)

#izraze koji sadrže brojevne operacije (četiri osnovne operacije, usporedbe<, >, ≤, ≥, =, != koje vraćaju broj, pretvaranje u string) te stringovne operacije (konkatenacija, test jednakosti koji vraća broj, pretvaranje u broj)

#grananja (sa i bez „inače”) i ograničene petlje (donja i gornja granica su zadane brojevnim izrazima)

#unos (s tipkovnice u brojevne i stringovne varijable), ispis (prijelaza u novi red i vrijednosti izraza)

#jednu vrstu komentara (linijski ili višelinijski)

from pj import *

class NL(enum.Enum):
	class STRING(Token): pass #string moze biti string kao tip i kao naziv varijable
	class BROJ(Token): pass #broj je broj ili vrijednost varijable
	MANJE, VEĆE = '<>'
	MJEDNAKO = '<='
	VJEDNAKO = '>='
	NJEDNAKO = '!='
	JEDNAKO = '=='
	PRIDRUŽI = '='
	PLUS, PUTA, MINUS, KROZ, OTVORENA, ZATVORENA, ZAREZ, TOČKAZAREZ = '+*-/(),;'
	ISPIŠI = 'ispiši'

def nl_lex(kod):
	lex = Tokenizer(kod)
	for znak in iter(lex.čitaj, ''): #čitaj do kraja programa
		if znak.isspace(): 
			lex.zanemari()
		elif znak.isdigit():
			lex.zvijezda(str.isdigit)
			yield lex.token(NL.BROJ)
		elif znak == '-': #linijski komentari --
			lex.pročitaj('-')
			lex.pročitaj_do('\n')
			lex.zanemari()
		elif znak == '/': #višelinijski komentari /* */
			lex.pročitaj('*')
			lex.pročitaj_do('*')
			if lex.slijedi('/'):
				lex.zanemari()
		elif znak == '"':
			lex.pročitaj_do('"')
			yield lex.literal(NL.STRING)	
		elif znak.isalpha():
		    lex.zvijezda(str.isalnum)
		    yield lex.literal(NL.STRING, case=False)
		else: yield lex.literal(NL)


if __name__=='__main__':
	ulaz = 'x = 5;'
	print(ulaz)
	
	tokeni = list(nl_lex(ulaz))
	print(*tokeni) #'otpakirana' lista





