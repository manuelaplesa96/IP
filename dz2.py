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
	NEGACIJA = '!'
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
		elif znak == '/': #višelinijski komentari /* */, linijski //
			if lex.slijedi('/'):
				lex.pročitaj_do('\n')
			else:
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
		elif znak == '!':
			if lex.slijedi('='):
				yield lex.literal(NL.NJEDNAKO)
			else:
				yield lex.literal(NL.NEGACIJA)
		elif znak == '<':
			if lex.slijedi('='):
				yield lex.literal(NL.MJEDNAKO)
			else: yield lex.literal(NL.MANJE)
		elif znak == '>':
			if lex.slijedi('='):
				yield lex.literal(NL.VJEDNAKO)
			else: yield lex.literal(NL.VEĆE)
		elif znak == '=':
			if lex.slijedi('='):
				yield lex.literal(NL.JEDNAKO)
			else: yield lex.literal(NL.PRIDRUŽI)
		else: yield lex.literal(NL)


if __name__=='__main__':
	ulaz = '5 -1 //ja sam linijski komentar\n'
	print(ulaz)
	
	tokeni = list(nl_lex(ulaz))
	print(*tokeni) #'otpakirana' lista





