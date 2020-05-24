# jedan brojevni i jedan stringovni tip te jednostavna pridruživanja (varijabla poprima vrijednost izraza odgovarajućeg tipa)

# izraze koji sadrže brojevne operacije (četiri osnovne operacije, usporedbe<, >, ≤, ≥, =, != koje vraćaju broj, pretvaranje u string) te stringovne operacije (konkatenacija, test jednakosti koji vraća broj, pretvaranje u broj)

# grananja (sa i bez „inače”) i ograničene petlje (donja i gornja granica su zadane brojevnim izrazima)

# unos (s tipkovnice u brojevne i stringovne varijable), ispis (prijelaza u novi red i vrijednosti izraza)

# jednu vrstu komentara (linijski ili višelinijski)

from pj import *


class NL(enum.Enum):
    class STRING(Token):
        def vrijednost(self, _):
            #s_navodnicima = self.sadržaj
            #sadrzaj = s_navodnicima[1:-1]
            #return sadrzaj
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
    COUT, CIN, ENDL = 'cout', 'cin', 'endl'
    FOR, IF, ELSE, WHILE, DO = 'for', 'if', 'else', 'while', 'do'
    AND, OR = '&&', '||'
    TOSTRING, TOINT = 'toStr', 'toInt'
    RETURN = 'return'


def nl_lex(kod):
    lex = Tokenizer(kod)
    for znak in iter(lex.čitaj, ''):  # čitaj do kraja programa
        if znak.isspace():
            lex.zanemari()
        elif znak.isdigit():
            lex.zvijezda(str.isdigit)
            p = lex.sadržaj
            if p == '0' or p[0] != '0':
                yield lex.token(NL.BROJ)
            else:
                raise lex.greška('Nisu podržane druge baze')
        elif znak == '"':
            lex.pročitaj_do('"')
            yield lex.token(NL.STRING)
        elif znak.isalpha():
            lex.zvijezda(str.isalpha)
            yield lex.literal(NL.IME)
        elif znak == '/':  # višelinijski komentari /* */, linijski //
            if lex.slijedi('/'):
                lex.pročitaj_do('\n')
            elif lex.slijedi('*'):
                lex.pročitaj_do('*')
                if lex.slijedi('/'):
                    lex.zanemari()
            else:
                yield lex.literal(NL.KROZ)
        elif znak == '!':
            yield lex.token(NL.NJEDNAKO if lex.slijedi('=') else NL.NEGACIJA)
        elif znak == '<':
            if lex.slijedi('='):
                yield lex.literal(NL.MJEDNAKO)
            elif lex.slijedi('<'):
                yield lex.literal(NL.MMANJE)
            else:
                yield lex.literal(NL.MANJE)
        elif znak == '>':
            if lex.slijedi('='):
                yield lex.literal(NL.VJEDNAKO)
            elif lex.slijedi('>'):
                yield lex.literal(NL.VVEĆE)
            else:
                yield lex.literal(NL.VEĆE)
        elif znak == '=':
            yield lex.token(NL.JEDNAKO if lex.slijedi('=') else NL.PRIDRUŽI)
        elif znak == '+':
            if lex.slijedi('='):
                yield lex.literal(NL.PJEDNAKO)
            elif lex.slijedi('+'):
                yield lex.literal(NL.PPLUS)
            else:
                yield lex.literal(NL.PLUS)
        elif znak == '&':
            if lex.slijedi('&'):
                yield lex.literal(NL.AND)
            else:
                raise lex.greška(
                    "U ovom jeziku nema samostalnog &! Pokušaj sa &&!")
        elif znak == '|':
            if lex.slijedi('|'):
                yield lex.literal(NL.OR)
            else:
                raise lex.greška(
                    "U ovom jeziku nema samostalnog |! Pokušaj sa ||!")
        else:
            yield lex.literal(NL)


# Beskontekstna gramatika
# +start-> naredba naredbe
# +naredbe -> '' | naredba naredbe
# naredba-> pridruži | predinkrement | OOTV naredbe OZATV | petlja | grananje |
#            ispis TOČKAZAREZ| unos | BREAK TOČKAZAREZ | vrati | cast
# +pridruži-> IME ( PRIDRUŽI | PJEDNAKO ) izraz TOČKAZAREZ | IME PPLUS TOČKAZAREZ
# +petlja-> for naredba | for VOTV naredbe VZATV
# +for-> FOR OOTV IME PRIDRUŽI BROJ TOČKAZAREZ IME ( MANJE | MJEDNAKO | VEĆE | VJEDNAKO ) BROJ TOČKAZAREZ inkrement OZATV
# +inkrement-> IME PPLUS | PPLUS IME | IME PJEDNAKO BROJ
# +grananje-> ( IF | WHILE ) uvjet kod | IF uvjet kod ELSE kod |
#            DO kod WHILE uvjet
# +kod -> naredba | VOTV naredbe VZATV
# !!!uvjeti-> OOTV uvjet OZATV | ( NEGACIJA | ' ' ) OOTV uvjet OZATV log uvjeti.............nema
# +uvjet-> (NEGACIJA | '' ) ( BROJ aritm BROJ | STRING str STRING ) | izraz aritm izraz ##nije unutar zagrada
# +aritm-> JEDNAKO | MJEDNAKO | VJEDNAKO | NJEDNAKO | MANJE | VEĆE
# +str -> JEDNAKO
# +izraz-> ( BROJ | IME ) ( PLUS | MINUS | PUTA | KROZ ) ( BROJ | IME ) | (STRING | IME ) PLUS ( STRING | IME )  ##unutar zagrada
# +log -> AND | OR
# +ispis-> COUT ispisi | COUT ispisi MMANJE ENDL
# +ispisi-> '' | MMANJE IME ispisi 
# +unos-> CIN unosi TOČKAZAREZ ( mislim da nema endl)
# +unosi-> '' | VVEĆE IME unosi
# !!!1vrati-> RETURN IME TOČKAZAREZ................nema
# +cast -> TOSTRING OOTV IME, ( BROJ | IME ) OZATV TOČKAZAREZ | TOINT OOTV IME, (STRING | IME) OZATV TOČKAZAREZ



# stabla: Program +, Petlja +, IF_Grananje +, WHILE_Grananje +, DO_Grananje +, Blok ?, Ispis +, Pridruživanje +, Binarna +


class NLParser(Parser):
    def start(self):
        naredbe = []
        while not self >> E.KRAJ:
            naredbe.append(self.naredba())
        return Program(naredbe)

    def naredba(self):
        if self >> NL.FOR:
            return self.petlja()  # +
        elif self >> NL.IF:
            return self.if_grananje()  # +
        elif self >> NL.WHILE:
            return self.while_grananje() # +
        elif self >> NL.DO:
            return self.do_grananje() # +
        elif self >> NL.COUT:
            return self.ispis() # +
        elif self >> NL.BREAK:
            return self.prekid()  # +
        elif self >> NL.IME:
            return self.pridruživanje() #+
        elif self >> NL.CIN:
            return self.unos() # -
        #elif self >> NL.RETURN:  #nisan ovo dobro
        #    return self.vrati()
        elif self >> {NL.TOINT, NL.TOSTRING}:
            return self.cast() # -
        #elif self >> NL.TOSTRING:
        #    return self.castString() # -
        elif self >> NL.PPLUS:
            return self.predinkrement()
        else:
            raise self.greška()
    
    def pridruživanje(self):
        ime = self.zadnji
        if self >> {NL.PRIDRUŽI, NL.PJEDNAKO}:
            operator = self.zadnji
            pridruženo = self.izraz()
            self.pročitaj(NL.TOČKAZAREZ)
            return Pridruživanje(ime, pridruženo, operator)
        elif self >> NL.PPLUS: #postinkrement
            operator = self.zadnji
            self.pročitaj(NL.TOČKAZAREZ)
            return Pridruživanje(ime, nenavedeno, operator)
    
    def predinkrement(self):
        operator = self.zadnji
        ime = self.pročitaj(NL.IME)
        self.pročitaj(NL.TOČKAZAREZ)
        return Pridruživanje(ime, nenavedeno, operator)
        
    def if_grananje(self):
        self.pročitaj(NL.OOTV)
        neg = 0
        if self >> NL.NEGACIJA:
            neg += 1
            while self >> NL.NEGACIJA:
                neg += 1
            self.pročitaj(NL.OOTV)
            ispod = self.uvjet() # prvi uvjet negiran
            self.pročitaj(NL.OZATV)
            if neg%2 == 0: # paran broj ! => nije negiran izraz
                uvjet = ispod
            else: # neparan broj ! => negiran je
                uvjet=Negacija(ispod) #dodamo taj prvi negirani uvjet
 
        else:    
            uvjet=self.uvjet() # dodamo taj prvi uvjet
        
        self.pročitaj(NL.OZATV)  # kraj uvjeta

        if self >> NL.VOTV:  # blok naredbi
            if_blok = []
            while not self >> NL.VZATV:
                if_blok.append(self.naredba())
        else:
            if_blok = [self.naredba()]

        if self >> NL.ELSE:
            if self >> NL.VOTV:
                else_blok = []
                while not self >> NL.VZATV:
                    else_blok.append(self.naredba())
            else:
                else_blok = [self.naredba()]
        else:
            else_blok = []  # izvrši prazan blok

        return IF_Grananje(uvjet, if_blok, else_blok)

    def while_grananje(self):
        self.pročitaj(NL.OOTV)
        neg = 0
        if self >> NL.NEGACIJA:
            neg += 1
            while self >> NL.NEGACIJA:
                neg += 1
            self.pročitaj(NL.OOTV)
            ispod = self.uvjet() # prvi uvjet negiran
            self.pročitaj(NL.OZATV)
            if neg%2 == 0: # paran broj ! => nije negiran izraz
                uvjet = ispod
            else: # neparan broj ! => negiran je
                uvjet=Negacija(ispod) #dodamo taj prvi negirani uvjet
 
        else:    
            uvjet=self.uvjet() # dodamo taj prvi uvjet
        
        self.pročitaj(NL.OZATV)  # kraj uvjeta

        if self >> NL.VOTV:  # blok naredbi
            blok = []
            while not self >> NL.VZATV:
                blok.append(self.naredba())
        else:
            blok = [self.naredba()]

        return WHILE_Petlja(uvjet, blok)

    def do_grananje(self):
        self.pročitaj(NL.VOTV)  # blok naredbi
        blok = []
        while not self >> NL.VZATV:
            blok.append(self.naredba())
        #else:
        #    blok = [self.naredba()]
        
        self.pročitaj(NL.WHILE)
        self.pročitaj(NL.OOTV)
        neg = 0
        if self >> NL.NEGACIJA:
            neg += 1
            while self >> NL.NEGACIJA:
                neg += 1
            self.pročitaj(NL.OOTV)
            ispod = self.uvjet() # prvi uvjet negiran
            self.pročitaj(NL.OZATV)
            if neg%2 == 0: # paran broj ! => nije negiran izraz
                uvjet = ispod
            else: # neparan broj ! => negiran je
                uvjet=Negacija(ispod) #dodamo taj prvi negirani uvjet
        else:    
            uvjet=self.uvjet() # dodamo taj prvi uvjet
        
        self.pročitaj(NL.OZATV)  # kraj uvjeta
        self.pročitaj(NL.TOČKAZAREZ) #kraj naredbe

        return DO_Petlja(uvjet, blok)

    def uvjet(self):      
        if self >> NL.BROJ: 
            prvi = self.zadnji
            if self >> {NL.JEDNAKO, NL.NJEDNAKO, NL.MJEDNAKO, NL.MANJE, NL.VJEDNAKO, NL.VEĆE}:
                op = self.zadnji
            
            if self >> NL.OOTV: # broj == izraz -
                drugi = self.izraz()
                self.pročitaj(NL.OZATV)
            elif self >> NL.IME: ## pretp da je ime broja broj == ime +
                drugi = self.zadnji
            else:
                drugi = self.pročitaj(NL.BROJ) # broj == broj +
        elif self >> NL.STRING: # string == string 
            prvi = self.zadnji
            if self >> NL.JEDNAKO:
                op = self.zadnji
            
            #if self >> NL.OOTV: #ne znam ima li smisla string==izraz 
            #    drugi = self.izraz()
            #    self.pročitaj(NL.OZATV)
            #else:
            if self >> NL.IME:
                drugi = self.zadnji
            else:
                drugi = self.pročitaj(NL.STRING)
        elif self >> NL.IME: ## pretpostavimo da je cast obavljen ako je ime string ili je koristeno samo jednakost
            prvi = self.zadnji
            if self >> {NL.NJEDNAKO, NL.MJEDNAKO, NL.MANJE, NL.VJEDNAKO, NL.VEĆE, NL.JEDNAKO}:
                op = self.zadnji
            
            if self >> NL.OOTV: # ime == izraz
                drugi = self.izraz()
                self.pročitaj(NL.OZATV)
            elif self >> NL.BROJ: # ime == broj
                drugi = self.zadnji
            elif self >> NL.STRING: #ime == string
                drugi = self.zadnji
            else: # ime == ime
                drugi = self.pročitaj(NL.IME)
            
        elif self >> NL.OOTV: # izraz==izraz, izraz==broj
            prvi = self.izraz()
            self.pročitaj(NL.OZATV)
            if self >> {NL.JEDNAKO, NL.NJEDNAKO, NL.MJEDNAKO, NL.MANJE, NL.VJEDNAKO, NL.VEĆE}:
                op = self.zadnji
            
            if self >> NL.OOTV:
                drugi = self.izraz()
                self.pročitaj(NL.OZATV)
            else:
                drugi = self.pročitaj(NL.BROJ)

        return Uvjet(op,prvi,drugi)
            
    def petlja(self):
        self.pročitaj(NL.OOTV)  # već smo pročitali FOR
        i = self.pročitaj(NL.IME)
        self.pročitaj(NL.PRIDRUŽI)
        početak = self.pročitaj(NL.BROJ)
        self.pročitaj(NL.TOČKAZAREZ)

        i2 = self.pročitaj(NL.IME)
        if i != i2:
            raise SemantičkaGreška('nisu podržane različite varijable')
        if self >> {NL.MANJE, NL.VEĆE, NL.MJEDNAKO, NL.VJEDNAKO}:
            usporedba = self.zadnji
        granica = self.pročitaj(NL.BROJ)
        self.pročitaj(NL.TOČKAZAREZ)

        if self >> NL.PPLUS:  # PREDINKREMENT
            inkrement = nenavedeno
            i3 = self.pročitaj(NL.IME)
            if i != i3:
                raise SemantičkaGreška('nisu podržane različite varijable')
        elif self >> NL.IME: # POSTINKREMENT ili +=
            i3 = self.zadnji
            if i != i3:
                raise SemantičkaGreška('nisu podržane različite varijable')
            elif self >> NL.PPLUS:
                inkrement = nenavedeno
            elif self >> NL.PJEDNAKO: 
                inkrement = self.pročitaj(NL.BROJ)
        self.pročitaj(NL.OZATV)

        if self >> NL.VOTV:
            blok = []
            while not self >> NL.VZATV:
                blok.append(self.naredba())
        else:
            blok = [self.naredba()]
        return Petlja(i, početak, usporedba, granica, inkrement, blok)

    def ispis(self):
        ispisi = []
        novired = False
        while self >> NL.MMANJE:
            if self >> {NL.IME, NL.STRING, NL.BROJ}: ispisi.append(self.zadnji)
            elif self >> NL.ENDL:
                novired = True
                break
        self.pročitaj(NL.TOČKAZAREZ)
        return Ispis(ispisi, novired)

    def prekid(self):
        br = self.zadnji
        self.pročitaj(NL.TOČKAZAREZ)
        return br
 
    def izraz(self):
        if self >> NL.MINUS: #negativan broj
            op = self.zadnji
            prvi = self.pročitaj(NL.BROJ)
            prvi = Unarna(op, prvi)
            
            op = nenavedeno
            if self >> {NL.PLUS, NL.MINUS, NL.PUTA, NL.KROZ} or self >> {NL.JEDNAKO, NL.NJEDNAKO, NL.MJEDNAKO, NL.MANJE, NL.VJEDNAKO, NL.VEĆE}: # drugi dio opcionalan (v. Binarna)
                op = self.zadnji
            if(op == nenavedeno): # broj
                return prvi
            elif self >> NL.IME: # broj+ime
                drugi = self.zadnji
                #return Binarna(op, prvi, drugi)
            else:
                drugi = self.pročitaj(NL.BROJ)
                #return Binarna(op, prvi, drugi)
        elif self >> NL.BROJ: # broj+broj 
            prvi = self.zadnji

            op = nenavedeno
            if self >> {NL.PLUS, NL.MINUS, NL.PUTA, NL.KROZ} or self >> {NL.JEDNAKO, NL.NJEDNAKO, NL.MJEDNAKO, NL.MANJE, NL.VJEDNAKO, NL.VEĆE}: # drugi dio opcionalan (v. Binarna)
                op = self.zadnji
            if(op == nenavedeno): # broj
                return prvi
            elif self >> NL.IME: # broj+ime
                drugi = self.zadnji
                #return Binarna(op, prvi, drugi)
            else:
                drugi = self.pročitaj(NL.BROJ)
                #return Binarna(op, prvi, drugi)
        elif self >> NL.STRING: # string+string & string+ime
            prvi = self.zadnji
            op = nenavedeno
            if self >> NL.PLUS:
                op = self.zadnji
            if(op == nenavedeno): # string
                return prvi
            elif self >> NL.IME:
                drugi = self.zadnji
                #return Binarna(op,prvi,drugi)
            else:
                drugi = self.pročitaj(NL.STRING)
                #return Binarna(op, prvi, drugi)
        elif self >> NL.IME: # ime+broj & ime+string & ime+ime ......napravljeno da podrazumijevamo da osoba zna da
                             # string ima samo +  (i da ne može ići string + broj i broj + string bez prethodnog castanja)
            prvi = self.zadnji
        
            op = nenavedeno
            if self >> {NL.PLUS, NL.MINUS, NL.PUTA, NL.KROZ}:
                op = self.zadnji
              
            if(op == nenavedeno):
                return prvi
            elif self >> NL.IME:
                drugi = self.zadnji
                #return Binarna(op, prvi, drugi)
            elif self >> NL.BROJ: # vjerujemo da osoba pazi da string ima samo +
                drugi = self.zadnji
                #return Binarna(op, prvi, drugi)
            else:
                drugi = self.pročitaj(NL.STRING)
                #return Binarna(op, prvi, drugi)
        
        #prvi, drugi = prvi.vrijednost, drugi.optim()
        nula = Token(NL.BROJ, '0')
        jedan = Token(NL.BROJ, '1')


        if op ^ NL.PLUS:
            if prvi == nula:
                return drugi
            elif drugi == nula:
                return prvi
            else:
                return Binarna(op,prvi,drugi)
        elif op ^ NL.MINUS:
            if drugi == nula:
                return prvi
            else:
                return Binarna(op,prvi,drugi)
        elif op ^ NL.PUTA:
            if prvi == jedan:
                return drugi
            elif prvi == jedan:
                return drugi
            elif prvi == nula or drugi == nula:
                return nula
            else:
                return Binarna(op,prvi,drugi)
        elif op ^ NL.KROZ:
            if drugi == jedan:
                return prvi
            elif drugi == nula:
                raise self.greška()
            elif prvi == nula:
                return nula
            else:
                return Binarna(op,prvi,drugi)

    def unos(self):
        unosi = []
        while self >> NL.VVEĆE:
            if self >> NL.IME: unosi.append(self.zadnji)
        self.pročitaj(NL.TOČKAZAREZ)
        return Unos(unosi)

    def cast(self):                         # mogući pozivi: cast(ime, vrijednost); ime1 = vrijednost; cast(ime2, ime1); 
        operator = self.zadnji              # gdje je vrijednost int ili string, a cast naredba toInt ili toStr
        self.pročitaj(NL.OOTV)
        ime = self.pročitaj(NL.IME)
        self.pročitaj(NL.ZAREZ)
        if self >> {NL.BROJ, NL.STRING, NL.IME}:
            stari = self.zadnji
        self.pročitaj(NL.OZATV)
        self.pročitaj(NL.TOČKAZAREZ)
        return Pridruživanje(ime, stari, operator)



class Prekid(Exception): pass

class Blok(AST('blok')):
    pass

class Program(AST('naredbe')):
    def izvrši(self):
        memorija = {}
        for naredba in self.naredbe:
                naredba.izvrši(memorija)

class Ispis(AST('ispisi novired')):
    def izvrši(self, mem):
        for ispis in self.ispisi:
            if isinstance(ispis.vrijednost(mem), str): #string cuvaj s " " a ispisuj ga bez
                #if ispis.vrijednost(mem)[:1] == '"': #ako pocinje s navodnicima - nije dobro ako je trenutni int
                bez_navodnika = ispis.vrijednost(mem)[1:-1]
                print(bez_navodnika, end=' ')
            else:
                print(ispis.vrijednost(mem), end=' ')
        if self.novired: print()

class Unos(AST('unosi')):
    def izvrši(self, mem):
        for unos in self.unosi:
            novavar = input() #on automatski napravi str od unosa
            if novavar.isdigit():
                novibroj = int(novavar)
                mem[unos.sadržaj] = novibroj
            else:
                mem[unos.sadržaj] = novavar

class Pridruživanje(AST('ime pridruženo operator')):
    def izvrši(self, mem):
        if self.operator ^ NL.PRIDRUŽI:
            mem[self.ime.sadržaj] = self.pridruženo.vrijednost(mem)
        elif self.operator ^ NL.PJEDNAKO:
            mem[self.ime.sadržaj] += self.pridruženo.vrijednost(mem)
        elif self.operator ^ NL.PPLUS:
            mem[self.ime.sadržaj] = mem[self.ime.sadržaj] +1
        elif self.operator ^ NL.TOINT:
            trenutni = self.pridruženo.vrijednost(mem)
            len_tren = len(trenutni) - 1
            novi = trenutni[1:len_tren]
            mem[self.ime.sadržaj] = int(novi)
        elif self.operator ^ NL.TOSTRING:
            novi = str(self.pridruženo.vrijednost(mem))
            novi = '"' + novi + '"'
            mem[self.ime.sadržaj] = novi

class Unarna(AST('op ispod')):
    def vrijednost(self, env):
        o, z = self.op, self.ispod.vrijednost(env)
        if o ^ NL.MINUS: return -z

class Binarna(AST('op lijevo desno')):
    def vrijednost(self, mem):
        o = self.op
        if self.lijevo ^ NL.STRING:
            lijevi_string = self.lijevo.vrijednost(mem)
            desni_string = self.desno.vrijednost(mem)
            len_lijevo = len(lijevi_string) - 1
            final_lijevo = lijevi_string[:len_lijevo]  # string bez zadnjeg char-a (")
            final_desno = desni_string[1:]  # string bez prvog char-a (")
            try:
                if o ^ NL.PLUS: return final_lijevo + final_desno
                else: assert False, 'nepokriveni slučaj binarnog operatora' + str(o)
            except ArithmeticError as ex: o.problem(*ex.args)
        else:
            x,y = self.lijevo.vrijednost(mem), self.desno.vrijednost(mem)
        try:
            if o ^ NL.PLUS: return x + y
            elif o ^ NL.MINUS: return x - y
            elif o ^ NL.PUTA: return x * y
            elif o ^ NL.KROZ: return x / y

            #opcionalno (ako želimo moć ispisat npr y=2<3, pa da tu ispiše 1, je li se ovo kosi s gramatikom?): 
            elif o ^ NL.JEDNAKO: return int(x == y)
            elif o ^ NL.NJEDNAKO: return int(x != y)
            elif o ^ NL.MJEDNAKO: return int(x <= y)
            elif o ^ NL.MANJE: return int(x < y)
            elif o ^ NL.VJEDNAKO: return int(x >= y)
            elif o ^ NL.VEĆE: return int(x > y)

            else: assert False, 'nepokriveni slučaj binarnog operatora' + str(o)
        except ArithmeticError as ex: o.problem(*ex.args)

class Uvjet(AST('op lijevo desno')):
    def vrijednost(self, mem):
        o,x,y = self.op, self.lijevo.vrijednost(mem), self.desno.vrijednost(mem)
        try:
            if o ^ NL.JEDNAKO: return x == y
            elif o ^ NL.NJEDNAKO: return x != y
            elif o ^ NL.MJEDNAKO: return x <= y
            elif o ^ NL.MANJE: return x < y
            elif o ^ NL.VJEDNAKO: return x >= y
            elif o ^ NL.VEĆE: return x > y
            else: assert False, 'nepokriveni slučaj binarnog operatora' + str(o)
        except ArithmeticError as ex: o.problem(*ex.args)

class IF_Grananje(AST('uvjet if_blok else_blok')):
    def izvrši(self, mem):
        if self.uvjet.vrijednost(mem):
            for naredba in self.if_blok:
                naredba.izvrši(mem)
        else:
            if len(self.else_blok) > 0:
                for naredba in self.else_blok:
                    naredba.izvrši(mem)
            else:
                pass

class WHILE_Petlja(AST('uvjet blok')):
    def izvrši(self, mem):
        while self.uvjet.vrijednost(mem):
            for naredba in self.blok:
                naredba.izvrši(mem)

class DO_Petlja(AST('uvjet blok')):
    def izvrši(self, mem):
        while 1:
            for naredba in self.blok:
                naredba.izvrši(mem)
            if not self.uvjet.vrijednost(mem):
                break;       
          
class Negacija(AST('ispod')):
    def vrijednost(self, mem):
        return not self.ispod.vrijednost(mem)

class Petlja(AST('varijabla početak usporedba granica inkrement blok')):
    def izvrši(self, mem):
        kv = self.varijabla.sadržaj
        mem[kv] = self.početak.vrijednost(mem)
        usp = self.usporedba
        if usp ^ NL.MANJE:
            while mem[kv] < self.granica.vrijednost(mem):
                try:
                    for naredba in self.blok: naredba.izvrši(mem)
                except Prekid: break
                inkr = self.inkrement
                if inkr is nenavedeno: inkr = 1
                else: inkr = inkr.vrijednost(mem)
                mem[kv] += inkr 
        elif usp ^ NL.MJEDNAKO:
            while mem[kv] <= self.granica.vrijednost(mem):
                try:
                    for naredba in self.blok: naredba.izvrši(mem)
                except Prekid: break
                inkr = self.inkrement
                if inkr is nenavedeno: inkr = 1
                else: inkr = inkr.vrijednost(mem)
                mem[kv] += inkr
        elif usp ^ NL.VEĆE:
            while mem[kv] > self.granica.vrijednost(mem):
                try:
                    for naredba in self.blok: naredba.izvrši(mem)
                except Prekid: break
                inkr = self.inkrement
                if inkr is nenavedeno: inkr = 1
                else: inkr = inkr.vrijednost(mem)
                mem[kv] -= inkr 
        elif usp ^ NL.VJEDNAKO:
            while mem[kv] > self.granica.vrijednost(mem):
                try:
                    for naredba in self.blok: naredba.izvrši(mem)
                except Prekid: break
                inkr = self.inkrement
                if inkr is nenavedeno: inkr = 1
                else: inkr = inkr.vrijednost(mem)
                mem[kv] -= inkr 


if __name__ == '__main__':
    ulaz = '5 + 1++ && { } () - 6/7//ja sam linijski komentar\n'
    # ulaz = 'i=5'
    print(ulaz)

    tokeni = list(nl_lex(ulaz))
    print(*tokeni)  # 'otpakirana' lista

    print()

    ulaz2 = '''
    for( i = 0; i <= 10; i+=2 ) {
        if( i < 9 ) 
            cout << i << endl;
        else break; 
    }
    for( i = 10; i >= 0; i+=2 ) {
            cout << i << endl;
    }
    '''

    print(ulaz2)

    tokeni2 = list(nl_lex(ulaz2))
    nl = NLParser.parsiraj(tokeni2)
    print(nl)
    nl.izvrši()

    ulaz3 = '''
        x = "kata" + "rina";  
        cout << x << endl; 
    '''
    #ovo ispisuje "kata""rina", KATARINAAAAA! :)))

    print(ulaz3)

    tokeni3 = list(nl_lex(ulaz3))
    nl = NLParser.parsiraj(tokeni3)
    print(nl)

    nl.izvrši()

    ulaz31 = '''
	y = "rina";
        x = "kata" + y;  
        cout << x << endl; 
    '''

    print(ulaz31)

    tokeni31 = list(nl_lex(ulaz31))
    nl = NLParser.parsiraj(tokeni31)
    print(nl)

    nl.izvrši()

    ulaz4 = '''
        x = 3+2;
        cout << x << endl;
    '''

    print(ulaz4)

    tokeni4 = list(nl_lex(ulaz4))
    nl = NLParser.parsiraj(tokeni4)
    print(nl)

    nl.izvrši()

    ulaz5 = '''
        x = 5;
        y = 6;
        if( (x+1) > (6+x) ) 
        {
            x = 1;
            cout << x << endl;
        }
        else
        {
            x = x+1;
            cout << x <<endl; 
        }
      
    '''

    print(ulaz5)

    tokeni5 = list(nl_lex(ulaz5))
    #print(*tokeni5)
    nl = NLParser.parsiraj(tokeni5)
    print(nl)

    nl.izvrši()  



    ulaz6 = '''
        x = 5;
        y = 6;
        while(x<7)
            x = x+1;
        
        cout << x <<endl;
      
    '''

    print(ulaz6)

    tokeni6 = list(nl_lex(ulaz6))
    #print(*tokeni5)
    nl = NLParser.parsiraj(tokeni6)
    print(nl)

    nl.izvrši()    

    ulaz7 = '''
        i=0; 
        do
        {
            cout << i << i <<endl;
            i = i+1;
        }while(i<6);
    '''

    print(ulaz7)
    tokeni7 = list(nl_lex(ulaz7))
    #print(*tokeni5)
    nl = NLParser.parsiraj(tokeni7)
    print(nl)
    nl.izvrši()    


    ulaz8 = '''
	cin >> novavar;
        cout << novavar;
    '''

    print(ulaz8)
    tokeni8 = list(nl_lex(ulaz8))
    #print(*tokeni5)
    nl = NLParser.parsiraj(tokeni8)
    print(nl)
    nl.izvrši()   

    ulaz9 = '''
        i=1;
	i+=1;
        cout << i << endl;
        i++;
        cout << i << endl;
        ++i;
        cout << i << endl;
    '''

    print(ulaz9)
    tokeni9 = list(nl_lex(ulaz9))
    #print(*tokeni5)
    nl = NLParser.parsiraj(tokeni9)
    print(nl)
    nl.izvrši()   


    ulaz10 = '''
    y = "15";
    toInt(x,y);
    cout << x << endl;

    toStr(x,15);
    cout << x << endl;
    '''

    print(ulaz10)
    tokeni = list(nl_lex(ulaz10))
    #print(*tokeni5)
    nl = NLParser.parsiraj(tokeni)
    print(nl)
    nl.izvrši() 

    ulaz11 = ''' 
    y = -15+2;
    z = 15;
    if(!!!(y>z)) 
        cout << "y je manji od z:";

    cout << y << z << endl;
    '''

    print(ulaz11)
    tokeni = list(nl_lex(ulaz11))
    #print(*tokeni5)
    nl = NLParser.parsiraj(tokeni)
    print(nl)
    nl.izvrši() 


    ulaz12 = ''' 
    a = 0 + 5;
    b = 15 + 0;
    c = 9 - 0;
    d = 5 * 1;
    e = 1 * 6;
    f = 5 / 1;
    g = 0 / 5;
    //h = 5 / 0; 
    
    cout << "Optimizacija zbrajanja: " << a << b << endl;
    cout << "Optimizacija oduzimanja: " << c << endl;
    cout << "Optimizacija množenja: " << d << e << endl;
    cout << "Optimizacija dijeljenja: " << f << g << endl;
    

    '''

    print(ulaz12)
    tokeni = list(nl_lex(ulaz12))
    #print(*tokeni5)
    nl = NLParser.parsiraj(tokeni)
    print(nl)
    nl.izvrši() 

