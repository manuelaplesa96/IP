#jedan brojevni i jedan stringovni tip te jednostavna pridruživanja (varijabla poprima vrijednost izraza odgovarajućeg tipa)

#izraze koji sadrže brojevne operacije (četiri osnovne operacije, usporedbe<, >, ≤, ≥, =, != koje vraćaju broj, pretvaranje u string) te stringovne operacije (konkatenacija, test jednakosti koji vraća broj, pretvaranje u broj)

#grananja (sa i bez „inače”) i ograničene petlje (donja i gornja granica su zadane brojevnim izrazima)

#unos (s tipkovnice u brojevne i stringovne varijable), ispis (prijelaza u novi red i vrijednosti izraza)

#jednu vrstu komentara (linijski ili višelinijski)

from pj import *

class NL(enum.Enum):
	class STRING(Token):
		def vrijednost(self, _): 
			return self.sadržaj
	class BROJ(Token): 
		def vrijednost(self, _): 
			return int(self.sadržaj)
	class BREAK(Token): 
		literal = 'break'
		def izvrši(self, mem): raise Prekid
	class IME(Token): 
		def vrijednost(self, mem): 
			return pogledaj(mem, self)
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
		elif znak == '"':
			lex.pročitaj_do('"')
			yield lex.token(NL.STRING)
		elif znak.isalpha():
			lex.zvijezda(str.isalpha)
			yield lex.literal(NL.IME)	
		elif znak == '/': #višelinijski komentari /* */, linijski //
			if lex.slijedi('/'):
				lex.pročitaj_do('\n')
			elif lex.slijedi('*'):
				lex.pročitaj_do('*')
				if lex.slijedi('/'):
					lex.zanemari()
			else: yield lex.literal(NL.KROZ)	
		elif znak == '!':
			yield lex.token(NL.NJEDNAKO if lex.slijedi('=') else NL.NEGACIJA)
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
			yield lex.token(NL.JEDNAKO if lex.slijedi('=') else NL.PRIDRUŽI)
		elif znak == '+':
			if lex.slijedi('='):
				yield lex.literal(NL.PJEDNAKO)
			if lex.slijedi('+'):
				yield lex.literal(NL.PPLUS)
			else: yield lex.literal(NL.PLUS)

		elif znak == '&':
			if lex.slijedi('&'):
				yield lex.literal(NL.AND)
			else: raise lex.greška("U ovom jeziku nema samostalnog &! Pokušaj sa &&!")
		elif znak == '|':
			if lex.slijedi('|'):
				yield lex.literal(NL.OR)
			else: raise lex.greška("U ovom jeziku nema samostalnog |! Pokušaj sa ||!")
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



class NLParser(Parser):
	def start(self):
		naredbe = []
		while not self >> E.KRAJ: naredbe.append(self.naredba())
		return Program(naredbe)
	
	def naredba(self):
		if self >> NL.FOR: return self.petlja()
		elif self >> NL.COUT: return self.ispis()
		elif self >> {NL.IF, NL.WHILE}: return self.grananje()
		elif self >> NL.BREAK: return self.prekid()
		else: raise self.greška()

	def petlja(self):
		self.pročitaj(NL.OOTV) #već smo pročitali FOR
		i = self.pročitaj(NL.IME)
		self.pročitaj(NL.PRIDRUŽI)
		početak = self.pročitaj(NL.BROJ)
		self.pročitaj(NL.TOČKAZAREZ)

		i2 = self.pročitaj(NL.IME) 
		if i != i2: raise SemantičkaGreška('nisu podržane različite varijable')
		if self >> NL.MANJE:
			usporedba = self.zadnji
		elif self >> NL.MMANJE:
			usporedba = self.zadnji
		granica = self.pročitaj(NL.BROJ)
		self.pročitaj(NL.TOČKAZAREZ)

		if self >> NL.PPLUS:  #PREDINKREMENT
			inkrement = nenavedeno 
			i3 = self.pročitaj(NL.IME)
			if i != i3: raise SemantičkaGreška('nisu podržane različite varijable')
		elif self >> NL.IME: #POSTINKREMENT ili PJEDNAKO
			i3 = self.zadnji
			if i != i3: raise SemantičkaGreška('nisu podržane različite varijable')
			if self >> NL.PPLUS: 
				inkrement = nenavedeno
			elif self >> NL.PJEDNAKO: 
				inkrement = self.pročitaj(NL.BROJ)

		self.pročitaj(NL.OZATV)
		
		if self >> NL.VOTV:
		    blok = []
		    while not self >> NL.VZATV: blok.append(self.naredba())
		else: blok = [self.naredba()]
		return Petlja(i, početak, usporedba, granica, inkrement, blok)



	def prekid(self):
		br = self.zadnji
		self.pročitaj(NL.TOČKAZAREZ)
		return br



if __name__=='__main__':
	ulaz = '5 + 1++ && { } () - 6/7//ja sam linijski komentar\n'
	#ulaz = 'i=5'
	print(ulaz)
	
	tokeni = list(nl_lex(ulaz))
	print(*tokeni) #'otpakirana' lista

	print()

	ulaz2 = '''
		for( i = 0; i < 10; i++ ) {
			if( i < 9 ) 
				cout << i << endl;
			else break; 
		}
		'''
	
	print(ulaz2)
	
	tokeni2 = list(nl_lex(ulaz2))
	print(*tokeni2) #'otpakirana' lista





