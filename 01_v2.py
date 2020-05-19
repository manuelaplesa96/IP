from pj import *

class LS(enum.Enum):
	NEG, KONJ, DISJ, OTV, ZATV = '!&|()'
	KOND, BIKOND = '->', '<->'
	class PVAR(Token):
		#pass #zasad necemo raditi nista
		#interpretacija je neki dictionary ** raspakira
		def vrijednost(self, **interpretacija):
			return pogledaj(interpretacija, self)
		def optim(self):
			return self;


def ls_lex(kod):
	lex = Tokenizer(kod) #inicijalizacija leksera 
	for znak in iter(lex.čitaj, ''): #'' je kraj programa
		if znak == 'P':
			prvo = lex.čitaj()
			if not prvo.isdigit(): lex.greška('očekivana znamenka')
			if prvo != '0': lex.zvijezda(str.isdigit) 
			#necemo 01, nego 1, zvijezda-deri dok god ima znam
			yield lex.token(LS.PVAR)
		elif znak == '-':
			lex.pročitaj('>')
			yield lex.token(LS.KOND)
		elif znak == '<':
			lex.pročitaj('-')
			lex.pročitaj('>')
			yield lex.token(LS.BIKOND)
		else:
			yield lex.literal(LS) #reverse lookup o kojem tokenu se radi


### Beskontekstna gramatika:
# formula -> NEG formula | PVAR | OTV formula binvez formula ZATV
# binvez -> KONJ | DISJ | KOND | BIKOND

### Apstraktna sintakstna stabla
# PVAR (Token, odozgo): tip, sadržaj
# Negacija: ispod
# Binarna: veznik lijevo desno

#stablo ^ TIP (je li stablo tipa TIP - true/false)


#mora postojati start - tako pj.py zna da je pocetak
#citanje tokena >> cita ocekivani token 
#mozes vratiti gresku koristeci metodu .greška iz pj.py
#.zadnji vraca zadnji procitani token
class LSParser(Parser): #nasljeduje klasu Parser iz pj.py
	def formula(self):
		if self >> LS.PVAR: #je li iduce prop var?
			return self.zadnji #procitan je vec pa ga vrati
		elif self >> LS.NEG:
			ispod = self.formula()
			return Negacija(ispod)
		elif self >> LS.OTV:
			lijevo = self.formula()
			if self >> LS.KONJ:
				desno = self.formula()
				self.pročitaj(LS.ZATV)
				return Konjunkcija(lijevo,desno)
			elif self >> LS.DISJ:
				desno = self.formula()
				self.pročitaj(LS.ZATV)
				return Disjunkcija(lijevo,desno)
			elif self >> LS.KOND:
				desno = self.formula()
				self.pročitaj(LS.ZATV)
				return Kondicional(lijevo,desno)
			elif self >> LS.BIKOND:
				desno = self.formula()
				self.pročitaj(LS.ZATV)
				return Bikondicional(lijevo,desno)

		else:
			raise self.greška()

	start = formula #ovo nemoj zaboraviti!!!
	

class Negacija(AST('ispod')):
	#pass
	def vrijednost(formula, **interpretacija):
		return not formula.ispod.vrijednost(**interpretacija)
	def optim(self):
		ispod_opt = self.ispod.optim() #zasto je bitno opt ovo ispod?
		if ispod_opt ^ Negacija: 
			return ispod_opt.ispod #ako je opet ispod negacija
		else:
			return Negacija(ispod_opt) 


class Konjunkcija(AST('lijevo desno')):
	#pass
	def vrijednost(formula, **interpretacija):
		l = formula.lijevo.vrijednost(**interpretacija)
		d = formula.desno.vrijednost(**interpretacija)
		return l and d
	
	def optim(self):
		lijevo_opt = self.lijevo.optim()
		desno_opt = self.desno.optim()
		return Konjunkcija(lijevo_opt, desno_opt)

class Disjunkcija(AST('lijevo desno')):
	#pass
	def vrijednost(formula, **interpretacija):
		l = formula.lijevo.vrijednost(**interpretacija)
		d = formula.desno.vrijednost(**interpretacija)
		return l or d
	
	def optim(self):
		lijevo_opt = self.lijevo.optim()
		desno_opt = self.desno.optim()
		if desno_opt ^ Negacija:
			return Kondicional(lijevo_opt, Negacija(desno_opt).optim())
		else:
			return Disjunkcija(lijevo_opt, desno_opt)

class Kondicional(AST('lijevo desno')):
	#pass
	def vrijednost(formula, **interpretacija):
		l = formula.lijevo.vrijednost(**interpretacija)
		d = formula.desno.vrijednost(**interpretacija)
		return l <= d
	
	def optim(self):
		lijevo_opt = self.lijevo.optim()
		desno_opt = self.desno.optim()
		return Kondicional(lijevo_opt, desno_opt)

class Bikondicional(AST('lijevo desno')):
	#pass
	def vrijednost(formula, **interpretacija):
		l = formula.lijevo.vrijednost(**interpretacija)
		d = formula.desno.vrijednost(**interpretacija)
		return l == d
	
	def optim(self):
		lijevo_opt = self.lijevo.optim()
		desno_opt = self.desno.optim()
		return Bikondicional(lijevo_opt, desno_opt)

	
#ulaz u primjer u ovom .py doc		
if __name__=='__main__':
	ulaz = '!(P5&!!(P3->P0))'
	print(ulaz)
	
	tokeni = list(ls_lex(ulaz))
	print(*tokeni) #'otpakirana' lista

	fo=LSParser.parsiraj(tokeni)
	print(fo)
	print()
	
	fo = fo.optim()
	print(fo)
	print()
	
	print(fo.vrijednost(P0 = False, P3 = True, P5 = False)) #True
	print()
	
	ulaz2 = '(P1|!P2)'
	print(ulaz2)
	tokeni2 = list(ls_lex(ulaz2))
	print(*tokeni2)

	fo1=LSParser.parsiraj(tokeni2)
	print(fo1)
	print()
	
	fo1 = fo1.optim()
	print(fo1)
	print()

	print(fo1.vrijednost(P1 = True, P2 = False)) #False
	print()



#f V ne(G) = G->F





	
