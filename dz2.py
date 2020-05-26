# jedan brojevni i jedan stringovni tip te jednostavna pridruživanja (varijabla poprima vrijednost izraza odgovarajućeg tipa)

# izraze koji sadrže brojevne operacije (četiri osnovne operacije, usporedbe<, >, ≤, ≥, =, != koje vraćaju broj, pretvaranje u string) te stringovne operacije (konkatenacija, test jednakosti koji vraća broj, pretvaranje u broj)

# grananja (sa i bez „inače”) i ograničene petlje (donja i gornja granica su zadane brojevnim izrazima)

# unos (s tipkovnice u brojevne i stringovne varijable), ispis (prijelaza u novi red i vrijednosti izraza)

# jednu vrstu komentara (linijski ili višelinijski)

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
    PPLUS , MMINUS = '++', '--'
    MJEDNAKO, VJEDNAKO, NJEDNAKO, JEDNAKO, PJEDNAKO, MIJEDNAKO = '<=', '>=', '!=', '==', '+=', '-='
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
            lex.zvijezda(str.isalnum)
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
        elif znak == '-':
            if lex.slijedi('='):
                yield lex.literal(NL.MIJEDNAKO)
            elif lex.slijedi('-'):
                yield lex.literal(NL.MMINUS)
            else:
                yield lex.literal(NL.MINUS)
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
# start -> naredba naredbe
# naredbe -> '' | naredba naredbe
# naredba -> pridruži | predinkrement | predekrement | naredbe | petlja | grananje |
#            ispis | unos | BREAK TOČKAZAREZ | cast
# pridruži-> IME ( PRIDRUŽI | PJEDNAKO | MIJEDNAKO ) izraz TOČKAZAREZ | IME ( PPLUS | MMINUS ) TOČKAZAREZ
# predinkrement -> PPLUS IME TOČKAZAREZ
# preddekrement -> MMINUS IME TOČKAZAREZ
# petlja -> for naredba | for VOTV naredbe VZATV | WHILE (NEGACIJA | '' ) uvjet kod | DO kod WHILE (NEGACIJA | '' ) uvjet
# for -> FOR OOTV IME PRIDRUŽI BROJ TOČKAZAREZ IME ( MANJE | MJEDNAKO | VEĆE | VJEDNAKO ) BROJ TOČKAZAREZ prirast OZATV
# prirast -> ( PPLUS | MMINUS ) IME | IME ( PPLUS | MMINUS ) | IME ( PJEDNAKO | MIJEDNAKO ) BROJ
# grananje -> IF (NEGACIJA | '' ) uvjet kod | IF (NEGACIJA | '' ) uvjet kod ELSE kod 
# kod -> naredba | VOTV naredbe VZATV
# uvjet-> BROJ aritm ( BROJ | OOTV izraz OZATV | IME ) | STRING str ( STRING | IME | OOTV izraz OZATV ) | 
#         OOTV izraz OZATV aritm ( OOTV izraz OZATV | BROJ | STRING | IME )  | IME ( OOTV izraz OZATV | BROJ | STRING | IME )
# aritm -> JEDNAKO | MJEDNAKO | VJEDNAKO | NJEDNAKO | MANJE | VEĆE
# izraz-> ( MINUS | '' ) ( BROJ | IME ) ( PLUS | MINUS | PUTA | KROZ ) predznak ( BROJ | IME ) | (STRING | IME ) PLUS ( STRING | IME )  
# predznak -> OOTV MINUS OZATV | ''
# ispis -> COUT MMANJE ispisi TOČKAZAREZ | COUT MMANJE ispisi MMANJE ENDL TOČKAZAREZ
# ispisi -> '' | IME ispisi 
# unos -> CIN VVEĆE IME TOČKAZAREZ 
# cast -> TOSTRING OOTV IME ZAREZ ( BROJ | IME ) OZATV TOČKAZAREZ | TOINT OOTV IME ZAREZ (STRING | IME) OZATV TOČKAZAREZ


# stabla: Prekid, Blok, Program, Ispis, Unos, Pridruživanje, Negativni_broj, Operacije, 
#         Uvjet, IF_Grananje, WHILE_Petlja, DO_Petlja, Negacija, FOR_Petlja


class NLParser(Parser):
    def start(self):
        naredbe = []
        while not self >> E.KRAJ:
            naredbe.append(self.naredba())
        return Program(naredbe)

    def naredba(self):
        if self >> NL.FOR:
            return self.for_petlja()  
        elif self >> NL.IF:
            return self.if_grananje()  
        elif self >> NL.WHILE:
            return self.while_petlja() 
        elif self >> NL.DO:
            return self.do_petlja() 
        elif self >> NL.COUT:
            return self.ispis() 
        elif self >> NL.BREAK:
            return self.prekid()  
        elif self >> NL.IME:
            return self.pridruživanje()
        elif self >> NL.CIN:
            return self.unos() 
        elif self >> {NL.TOINT, NL.TOSTRING}:
            return self.cast()
        elif self >> NL.PPLUS:
            return self.predinkrement()
        elif self >> NL.MMINUS:
            return self.preddekrement()
        else:
            raise self.greška()
    
    def pridruživanje(self):
        ime = self.zadnji
        if self >> {NL.PRIDRUŽI, NL.PJEDNAKO, NL.MIJEDNAKO}:
            operator = self.zadnji
            pridruženo = self.izraz()
            self.pročitaj(NL.TOČKAZAREZ)
            return Pridruživanje(ime, pridruženo, operator)
        elif self >> {NL.PPLUS, NL.MMINUS}: #postinkrement
            operator = self.zadnji
            self.pročitaj(NL.TOČKAZAREZ)
            return Pridruživanje(ime, nenavedeno, operator)
    
    def predinkrement(self):
        operator = self.zadnji
        ime = self.pročitaj(NL.IME)
        self.pročitaj(NL.TOČKAZAREZ)
        return Pridruživanje(ime, nenavedeno, operator)
    
    def preddekrement(self):
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
            ispod = self.uvjet()
            self.pročitaj(NL.OZATV)
            if neg%2 == 0: # paran broj ! => nije negiran uvjet
                uvjet = ispod
            else: # neparan broj ! => negiran je
                uvjet=Negacija(ispod)
 
        else:    
            uvjet=self.uvjet() 
        
        self.pročitaj(NL.OZATV)  

        if self >> NL.VOTV:  # if_blok naredbi
            if_blok = []
            while not self >> NL.VZATV:
                if_blok.append(self.naredba())
        else:
            if_blok = [self.naredba()] # samo jedna naredba

        if self >> NL.ELSE:
            if self >> NL.VOTV: # else_blok naredbi
                else_blok = []
                while not self >> NL.VZATV:
                    else_blok.append(self.naredba())
            else:
                else_blok = [self.naredba()]
        else:
            else_blok = []  # prazan else_blok

        return IF_Grananje(uvjet, if_blok, else_blok)

    def while_petlja(self):
        self.pročitaj(NL.OOTV)
        neg = 0
        if self >> NL.NEGACIJA:
            neg += 1
            while self >> NL.NEGACIJA:
                neg += 1
            self.pročitaj(NL.OOTV)
            ispod = self.uvjet() 
            self.pročitaj(NL.OZATV)
            if neg%2 == 0: # paran broj ! => nije negiran uvjet
                uvjet = ispod
            else: # neparan broj ! => negiran je
                uvjet=Negacija(ispod) 
 
        else:    
            uvjet=self.uvjet() 
        
        self.pročitaj(NL.OZATV)  

        if self >> NL.VOTV:  # blok naredbi
            blok = []
            while not self >> NL.VZATV:
                blok.append(self.naredba())
        else:
            blok = [self.naredba()] # samo jedna naredba

        return WHILE_Petlja(uvjet, blok)

    def do_petlja(self):
        self.pročitaj(NL.VOTV)  # blok naredbi
        blok = []
        while not self >> NL.VZATV:
            blok.append(self.naredba())
        
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
            if neg%2 == 0: # paran broj ! => nije negiran uvjet
                uvjet = ispod
            else: # neparan broj ! => negiran je
                uvjet=Negacija(ispod) 
        else:    
            uvjet=self.uvjet() 
        self.pročitaj(NL.OZATV)  
        self.pročitaj(NL.TOČKAZAREZ) 

        return DO_Petlja(uvjet, blok)

    def uvjet(self):      
        if self >> NL.BROJ: 
            prvi = self.zadnji
            if self >> {NL.JEDNAKO, NL.NJEDNAKO, NL.MJEDNAKO, NL.MANJE, NL.VJEDNAKO, NL.VEĆE}:
                op = self.zadnji
            
            if self >> NL.OOTV: # broj op izraz 
                drugi = self.izraz()
                self.pročitaj(NL.OZATV)
            elif self >> NL.IME: # broj op ime 
                drugi = self.zadnji
            else:
                drugi = self.pročitaj(NL.BROJ) # broj op broj 
        elif self >> NL.STRING: 
            prvi = self.zadnji
            if self >> NL.JEDNAKO:
                op = self.zadnji
 
            if self >> NL.IME: # string == ime
                drugi = self.zadnji
            elif self >> NL.OOTV: # string == izraz 
                drugi = self.izraz()
                self.pročitaj(NL.OZATV)
            else: # string == string 
                drugi = self.pročitaj(NL.STRING)
        elif self >> NL.IME: 
            prvi = self.zadnji
            if self >> {NL.NJEDNAKO, NL.MJEDNAKO, NL.MANJE, NL.VJEDNAKO, NL.VEĆE, NL.JEDNAKO}:
                op = self.zadnji
            
            if self >> NL.OOTV: # ime op izraz
                drugi = self.izraz()
                self.pročitaj(NL.OZATV)
            elif self >> NL.BROJ: # ime op broj
                drugi = self.zadnji
            elif self >> NL.STRING: #ime op string
                drugi = self.zadnji
            else: # ime op ime
                drugi = self.pročitaj(NL.IME)        
        elif self >> NL.OOTV: 
            prvi = self.izraz()
            self.pročitaj(NL.OZATV)
            if self >> {NL.JEDNAKO, NL.NJEDNAKO, NL.MJEDNAKO, NL.MANJE, NL.VJEDNAKO, NL.VEĆE}:
                op = self.zadnji
            
            if self >> NL.OOTV: # izraz op izraz
                drugi = self.izraz()
                self.pročitaj(NL.OZATV) 
            elif self >> NL.STRING: # izraz == string
                drugi = self.zadnji
            elif self >> NL.IME: # izraz op ime
                drugi = self.zadnji
            else: # izraz op broj
                drugi = self.pročitaj(NL.BROJ)

        return Uvjet(op,prvi,drugi)
            
    def for_petlja(self):
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

        if self >> {NL.PPLUS, NL.MMINUS}:               # PREDINKREMENT i PREDDEKREMENT
            inkrement = nenavedeno
            i3 = self.pročitaj(NL.IME)
            if i != i3:
                raise SemantičkaGreška('nisu podržane različite varijable')
        elif self >> NL.IME:
            i3 = self.zadnji
            if i != i3:
                raise SemantičkaGreška('nisu podržane različite varijable')
            elif self >> {NL.PPLUS, NL.MMINUS}:         # POSTINKREMENT I POSTDEKREMENT
                inkrement = nenavedeno
            elif self >> {NL.PJEDNAKO, NL.MIJEDNAKO}:   # += i -= 
                inkrement = self.pročitaj(NL.BROJ)
        self.pročitaj(NL.OZATV)

        if self >> NL.VOTV:
            blok = []
            while not self >> NL.VZATV:
                blok.append(self.naredba())
        else:
            blok = [self.naredba()]
        return FOR_Petlja(i, početak, usporedba, granica, inkrement, blok)

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
        if self >> NL.MINUS: # prvi je negativan broj
            op = self.zadnji
            if self >> {NL.BROJ, NL.IME}:
                prvi = self.zadnji
            prvi = Negativni_broj(op, prvi)
            
            op = nenavedeno
            if self >> {NL.PLUS, NL.MINUS, NL.PUTA, NL.KROZ}:
                op = self.zadnji
            if(op == nenavedeno): # upisali smo samo jedan broj
                return prvi
            elif self >> {NL.IME, NL.BROJ}: 
                drugi = self.zadnji
            elif self >> NL.OOTV: # negativan broj na drugom mjestu mora doći u zagradama
                pom_op = self.pročitaj(NL.MINUS)
                if self >> {NL.IME, NL.BROJ}:
                    drugi = self.zadnji
                drugi = Negativni_broj(pom_op, drugi)
                self.pročitaj(NL.OZATV)

        elif self >> {NL.BROJ,NL.IME}:
            prvi = self.zadnji

            op = nenavedeno
            if self >> {NL.PLUS, NL.MINUS, NL.PUTA, NL.KROZ}:
                op = self.zadnji
            if(op == nenavedeno): 
                return prvi
            elif self >> {NL.IME, NL.BROJ}: 
                drugi = self.zadnji
            elif self >> NL.OOTV:
                pom_op = self.pročitaj(NL.MINUS)
                if self >> {NL.IME, NL.BROJ}:
                    drugi = self.zadnji
                drugi = Negativni_broj(pom_op, drugi)
                self.pročitaj(NL.OZATV)
        elif self >> NL.STRING:
            prvi = self.zadnji
            op = nenavedeno
            if self >> NL.PLUS:
                op = self.zadnji
            if(op == nenavedeno): 
                return prvi
            elif self >> NL.IME:
                drugi = self.zadnji
            else:
                drugi = self.pročitaj(NL.STRING)
 
        nula = Token(NL.BROJ, '0')
        jedan = Token(NL.BROJ, '1')


        if op ^ NL.PLUS:
            if prvi == nula:
                return drugi
            elif drugi == nula:
                return prvi
            else:
                return Operacije(op,prvi,drugi)
        elif op ^ NL.MINUS:
            if drugi == nula:
                return prvi
            else:
                return Operacije(op,prvi,drugi)
        elif op ^ NL.PUTA:
            if prvi == jedan:
                return drugi
            elif prvi == jedan:
                return drugi
            elif prvi == nula or drugi == nula:
                return nula
            else:
                return Operacije(op,prvi,drugi)
        elif op ^ NL.KROZ:
            if drugi == jedan:
                return prvi
            elif drugi == nula:
                raise self.greška()
            elif prvi == nula:
                return nula
            else:
                return Operacije(op,prvi,drugi)

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
            elif novavar.startswith('"') and novavar.endswith('"'):
                mem[unos.sadržaj] = novavar
            else:
                raise SemantičkaGreška("Krivi unos!")

class Pridruživanje(AST('ime pridruženo operator')):
    def izvrši(self, mem):
        if self.operator ^ NL.PRIDRUŽI:
            mem[self.ime.sadržaj] = self.pridruženo.vrijednost(mem)
        elif self.operator ^ NL.PJEDNAKO:
            mem[self.ime.sadržaj] += self.pridruženo.vrijednost(mem)
        elif self.operator ^ NL.MIJEDNAKO:
            mem[self.ime.sadržaj] -= self.pridruženo.vrijednost(mem)
        elif self.operator ^ NL.PPLUS:
            mem[self.ime.sadržaj] = mem[self.ime.sadržaj] + 1
        elif self.operator ^ NL.MMINUS:
            mem[self.ime.sadržaj] = mem[self.ime.sadržaj] - 1
        elif self.operator ^ NL.TOINT:
            trenutni = self.pridruženo.vrijednost(mem)
            len_tren = len(trenutni) - 1
            novi = trenutni[1:len_tren]
            if(novi.isnumeric()):
                mem[self.ime.sadržaj] = int(novi)
            else:
                raise SemantičkaGreška('Da biste castali u int, string mora sadržavati isključivo znamenke!')
        elif self.operator ^ NL.TOSTRING:
            novi = str(self.pridruženo.vrijednost(mem))
            novi = '"' + novi + '"'
            mem[self.ime.sadržaj] = novi

class Negativni_broj(AST('op ispod')):
    def vrijednost(self, env):
        o, z = self.op, self.ispod.vrijednost(env)
        if o ^ NL.MINUS: return -z

class Operacije(AST('op lijevo desno')):
    def vrijednost(self, mem):
        o,x,y = self.op, self.lijevo.vrijednost(mem), self.desno.vrijednost(mem)
        if type(x) is type(y):
            try:
                if type(x) == str:
                    lijevi_string = x
                    desni_string = y
                    len_lijevo = len(lijevi_string) - 1
                    final_lijevo = lijevi_string[:len_lijevo]
                    final_desno = desni_string[1:]
                    try:
                        if o ^ NL.PLUS: 
                            return final_lijevo + final_desno
                        else: assert False, 'nepokriveni slučaj binarnog operatora' + str(o)
                    except ArithmeticError as ex: o.problem(*ex.args)
                else:
                    try:
                        if o ^ NL.PLUS: return x + y
                        elif o ^ NL.MINUS: return x - y
                        elif o ^ NL.PUTA: return x * y
                        elif o ^ NL.KROZ: return x / y

                        else: assert False, 'nepokriveni slučaj binarnog operatora' + str(o)
                    except ArithmeticError as ex: o.problem(*ex.args)
            except ArithmeticError as ex: o.problem(*ex.args)
        else:
            raise SemantičkaGreška('Pokušavate raditi aritmetičku operaciju na dvijema varijablama različitog tipa!')

class Uvjet(AST('op lijevo desno')):
    def vrijednost(self, mem):
        o,x,y = self.op, self.lijevo.vrijednost(mem), self.desno.vrijednost(mem)
        if type(x) is type(y):
            try:
                if o ^ NL.JEDNAKO: return int(x == y)
                elif o ^ NL.NJEDNAKO: return int(x != y)
                elif o ^ NL.MJEDNAKO: return int(x <= y)
                elif o ^ NL.MANJE: return int(x < y)
                elif o ^ NL.VJEDNAKO: return int(x >= y)
                elif o ^ NL.VEĆE: return int(x > y)
                else: assert False, 'nepokriveni slučaj binarnog operatora' + str(o)
            except ArithmeticError as ex: o.problem(*ex.args)
        else:
            raise SemantičkaGreška('Pokušavate usporediti dvije varijable različitog tipa!')

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

class FOR_Petlja(AST('varijabla početak usporedba granica inkrement blok')):
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

    # inicijalizacija varijabli i osnovne operacije
    primjer1 = '''
        cout << "Primjer1." << endl;
        x = 5;
        xx = x / 10;
        y = "rijec";
        yy = "Duga " + y;
        
        cout << "Ispis vrijednosti varijable xx: " << xx << endl;
        cout << "Ispis vrijednosti varijable yy: " << yy << endl;  
    '''
    print(primjer1)
    tokeni1 = list(nl_lex(primjer1))
    nl = NLParser.parsiraj(tokeni1)
    print(nl)
    print()
    nl.izvrši()
    print()
    

    # petlja i upis
    primjer2 = '''
        cout << "Primjer2." << endl;
        cout << "Unesite broj: ";
        cin >> x;

        cout << "Ispis niza brojeva: ";
        for(i=0;i<10;i++)
        {
            y = x + i;
            cout << y << " ";
        }
        cout << endl;
    '''
    print(primjer2)
    tokeni2 = list(nl_lex(primjer2))
    nl = NLParser.parsiraj(tokeni2)
    print(nl)
    print()
    nl.izvrši()
    print()


    # grananje i petlja
    primjer3 = '''
        cout << "Primjer3." <<endl;
        x = 15;
        y = 20;

        if( x > (y-6) )
        {
            while (x > 0){
                x--;
                cout << "x = " << x << endl;
            }
        }
        else
        {
            cout << "x je veći!" << endl;
        }
         
    '''
    print(primjer3)
    tokeni3 = list(nl_lex(primjer3))
    nl = NLParser.parsiraj(tokeni3)
    print(nl)
    print()
    nl.izvrši()
    print()


    primjer4 = '''
        cout << "Primjer4." << endl;
        y = "15";
        toInt(x,y);
            
        str = 


         
    '''
    print(primjer4)
    tokeni4 = list(nl_lex(primjer4))
    nl = NLParser.parsiraj(tokeni4)
    print(nl)
    print()
    nl.izvrši()
    print()


    # osnovne operacije s tipovima
    primjer5 = '''
         x = 2;
         y = 5;
         z = x + y;
         
    '''
    print(primjer5)
    tokeni5 = list(nl_lex(primjer5))
    nl = NLParser.parsiraj(tokeni5)
    print(nl)
    print()
    nl.izvrši()
    print()





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
        i-=2;
        cout << i << endl;
        i--;
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

    //y = "5smc";
    //toInt(x,y);
    //cout << x << endl;

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
    y = "kata";
    z = "rina";
    x1 = "katarina";
    
    if((y+z)==x1) 
        cout << "y je manji od z:";
    cout << x1 <<endl;

    if(2<3) 
        cout << "2 je manje od 3";

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


    ulaz13 = ''' 
    a = 1+(-2);
    b = -2+(-3);
    c = 9 - (-3);
    d = -5 -( -1);
    e = 1 * (-5);
    f = -3 * (-2);
    g = 2 / (-3);
    h = -5 / (-5); 
    
    cout << "Plus" << a << b << endl;
    cout << "Minus: " << c << d << endl;
    cout << "Puta: " << e << f << endl;
    cout << "Kroz: " << g << h << endl;

    x = 2; y = 3;
    z = x + y; 
    cout << z;
    z = x + (-y);
    cout << " " << z;
    z = -x + (-y);
    cout << " " << z;
    z = -x + y;
    cout << " " << z << endl;
    
    

    '''

    print(ulaz13)
    tokeni = list(nl_lex(ulaz13))
    #print(*tokeni5)
    nl = NLParser.parsiraj(tokeni)
    print(nl)
    nl.izvrši() 

    ulaz14 = ''' 
   for( i = 0; i <= 10; i++ ) {
        if( i < 9 ) 
            cout << i << endl;
        else break; 
    }
    for( i = 10; i >= 0; i-- ) {
            cout << i << endl;
    }

    '''
    

    print(ulaz14)
    tokeni = list(nl_lex(ulaz14))
    #print(*tokeni5)
    nl = NLParser.parsiraj(tokeni)
    print(nl)
    nl.izvrši() 

