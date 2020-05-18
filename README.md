# IP


## Upute lekser

Tipovi: BROJ, STRING, BREAK

Sve varijable koje su broj su BROJ. Sve varijable koje su tipa string (od " do ") su STRING.
Token BREAK služi za izlazak iz petlje. 

Nazivi varijabli su također STRING (lijevo od operatora pridruživanja, počinje sa slovom, a ne brojkom).

Varijabli pridružujemo vrijednost sa '=' (PRIDRUŽI).

Svaka naredba kao i u C-u završava s ; (TOČKAZAREZ).
Možemo napraviti više pridruživanja pa ih nabrojati koristeći ZAREZ(','). Npr.:

x = 1, y = "1";


Za ispis vrijednosti neke varijable koristi se ispiši(x), gdje je x naziv varijable.


### Komentari:
// je linijski, a /* */ višelinijski komentar. 


Što ako imamo /* ? Zasad javi grešku da očekuje */ (kraj komentara)
*/ lekser prevede u PUTA KROZ jer ga jos nije briga šta nije logično, pa ne znan dal drugačije handleat dio s komentarima u lekseru?


### Podržana grananja i petlje:

if(uvjet) kod;
if(uvjet) kod; else kod;

for(i=0; i <= broj; i++){ kod; }
while(uvjet){ kod; }
do{ kod; }while(uvjet)


Napomena:
Podržane su OOTV, OZATV, VOTV te VZATV zagrade ((,),{,}).

### Osnovne operacije:

+,-,*,/ = PLUS, MINUS, PUTA, KROZ
Ovisno o tipu varijabli slijeva i zdesna regulirat ćemo značenje tokena.
Konkatenacija dva stringa: string + string
string + broj
broj + string ili neće biti dozvoljeno ili će cast-ati u lijevi tip, tj.
string + broj = konkatenacija string + string(broj)
broj + string = broj akko string = 'broj' ? 

### Inkrement i +=:

Podržan je postinkrement i predinkrement (?), tj. j++ te ++j će davati novu vrijednost varijable j uvećanu za 1.
+= će kao i u C-u pridruživati novu vrijednost postojećoj varijabli, npr. j += 5 (j = j + 5). 



