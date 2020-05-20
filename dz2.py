#jedan brojevni i jedan stringovni tip te jednostavna pridruživanja (varijabla poprima vrijednost izraza odgovarajućeg tipa)

#izraze koji sadrže brojevne operacije (četiri osnovne operacije, usporedbe<, >, ≤, ≥, =, != koje vraćaju broj, pretvaranje u string) te stringovne operacije (konkatenacija, test jednakosti koji vraća broj, pretvaranje u broj)

#grananja (sa i bez „inače”) i ograničene petlje (donja i gornja granica su zadane brojevnim izrazima)

#unos (s tipkovnice u brojevne i stringovne varijable), ispis (prijelaza u novi red i vrijednosti izraza)

#jednu vrstu komentara (linijski ili višelinijski)

from pj import *

class NL(enum.Enum):
	class STRING(Token): pass # string moze biti string kao tip i kao naziv varijable
	class BROJ(Token): pass # broj je broj ili vrijednost varijable
	class BREAK(Token): pass # za izlazak iz petlje breakom
	class IME(Token): pass # imena varijabli
	MANJE, VEĆE = '<>'
	PPLUS = '++'
	MJEDNAKO, VJEDNAKO, NJEDNAKO, JEDNAKO, PJEDNAKO = '<=', '>=', '!=', '==', '+='
	MMANJE, VVEĆE = '<<', '>>'
	NEGACIJA, PRIDRUŽI = '!', '='
	PLUS, PUTA, MINUS, KROZ, ZAREZ, TOČKAZAREZ, OOTV, OZATV, VOTV, VZATV = '+*-/,;(){}'
	COUT, CIN, RETURN,  = 'cout', 'cin','return'
	FOR, IF, ELSE, WHILE, DO = 'for', 'if', 'else', 'while', 'do'
	AND, OR = '&&', '||'
	TOSTRING, TOINT = 'toStr', 'toInt'
 
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
			elif lex.slijedi('*'):
				lex.pročitaj_do('*')
				if lex.slijedi('/'):
					lex.zanemari()
			else: yield lex.literal(NL.KROZ)
		elif znak == '"':
			lex.pročitaj_do('"')
			yield lex.literal(NL.STRING)	
		elif znak == '!':
			if lex.slijedi('='):
				yield lex.literal(NL.NJEDNAKO)
			else:
				yield lex.literal(NL.NEGACIJA)
		elif znak == '<':
			if lex.slijedi('='):
				yield lex.literal(NL.MJEDNAKO)
			elif lex.slijedi('<'):
				yield lex.literal(NL.MMANJE)
			else: yield lex.literal(NL.MANJE)
		elif znak == '>':
			if lex.slijedi('='):
				yield lex.literal(NL.VJEDNAKO)
			elif lex.slijedi('>'):
				yield lex.literal(NL.VVEĆE)
			else: yield lex.literal(NL.VEĆE)
		elif znak == '=':
			if lex.slijedi('='):
				yield lex.literal(NL.JEDNAKO)
			else: yield lex.literal(NL.PRIDRUŽI)
		elif znak == '+':
			if lex.slijedi('='):
				yield lex.literal(NL.PJEDNAKO)
			if lex.slijedi('+'):
				yield lex.literal(NL.PPLUS)
			else: yield lex.literal(NL.PLUS)
		elif znak.isalpha():
			lex.zvijezda(str.isalpha)
			yield lex.literal(NL.IME)
		elif znak == '&':
			if lex.slijedi('&'):
				yield lex.literal(NL.AND)
			else: raise lex.greška("Krivi unos!")
		elif znak == '|':
			if lex.slijedi('|'):
				yield lex.literal(NL.OR)
			else: raise lex.greška("Krivi unos!")
		else: yield lex.literal(NL)



###Beskontekstna gramatika
# start		-> naredba naredbe 
# naredbe 	-> '' | naredba naredbe
# naredba	-> pridruži | OOTV naredbe OZATV | petlja | grananje |
#			   ispis | unos | BREAK TOČKAZAREZ | vrati | cast
# pridruži	-> IME PRIDRUŽI ( BROJ | STRING ) TOČKAZAREZ | IME PRIDRUŽI izraz TOČKAZAREZ
# petlja	-> for naredba | for VOTV naredbe VZATV
# for		-> FOR OOTV IME PRIDRUŽI BROJ TOČKAZAREZ IME ( MANJE | MJEDNAKO ) BROJ TOČKAZAREZ inkrement OZATV
# inkrement	-> IME PPLUS | PPLUS IME | IME PJENDAKO BROJ 
# grananje	-> ( IF | WHILE ) OOTV uvjeti OZATV kod | IF OOTV uvjeti OZATV kod ELSE kod |
#			   DO kod WHILE OOTV uvjeti OZATV
# kod 		-> naredba | VOTV naredbe VZATV 
# uvjeti	-> OOTV uvjet OZATV log uvjeti | OOTV uvjet OZATV 
# uvjet		-> (NEGACIJA | '' ) ( BROJ aritm BROJ | STRING str STRING ) | izraz aritm izraz
# aritm		-> JEDNAKO | MJEDNAKO | VJEDNAKO | NJEDNAKO | MANJE | VEĆE
# str 		-> JEDNAKO
# izraz 	-> BROJ ( PLUS | MINUS | PUTA | KROZ ) BROJ | STRING PLUS STRING | BROJ 
# log 		-> AND | OR
# ispis		-> COUT ispisi TOČKAZAREZ | COUT ispisi MMANJE ENDL TOČKAZAREZ
# ispisi	-> '' | MMANJE IME ispisi TOČKAZAREZ
# unos		-> CIN unosi TOČKAZAREZ | CIN unosi VVEĆE ENDL TOČKAZAREZ
# unosi		-> '' | VVEĆE IME unosi
# vrati		-> RETURN IME TOČKAZAREZ  ??? vraćanje polja
# cast 		-> TOSTRING OOTV BROJ OZATV TOČKAZAREZ | TOINT OOTV STRING OZATV TOČKAZAREZ


##parsiranje

	
		

if __name__=='__main__':
	ulaz = '5 + 1++ && { } () - 6/7//ja sam linijski komentar\n'
	#ulaz = 'i=5'
	print(ulaz)
	
	tokeni = list(nl_lex(ulaz))
	print(*tokeni) #'otpakirana' lista

	print()

	ulaz2 = 'for( i = 0; i < 10; i++ ){ if( i < 9 ) ispiši(i); else break; }'
	#ulaz = 'if( i == 5 ) break;'
	print(ulaz2)
	
	tokeni2 = list(nl_lex(ulaz2))
	print(*tokeni2) #'otpakirana' lista





