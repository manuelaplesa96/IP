# New Language (NL)

Zadatak nam je bio osmisliti programski jezik koji zadovoljava neke operacije i karakteristike koje inače inače očekujemo da jezik podržava. Tako ovaj naš NL jezik podržava 2 tipa podataka, broj (int) (NL.BROJ) i string (NL.STRING), pri tome se strigovi zadaju unutar dvostrukih navodnika (" "). Nazivi varijabli (NL.IME) su također strigovi, ali ne pisani unutar " ", nego u smislu da nazivi varijabli ne smiju počimati s brojem, već mora početi slovom. NL prepoznaje da se radi o naredbi ako ona završi sa ; (NL.TOČKAZAREZ). 
 
Primjer. x = 1, y = "1"; 
x i y su varijable s time da je varijabli x pridružena vrijednost 1 tipa broj, a y vrijednsot1 tipa string.

U jeziku je još definirana i klasa BREAK koja služi za izlazak iz petlje.

## Pridruživanja

* = (NL.PRIDRUŽIVANJE) - kako bismo svaku varijablu mogli inicijalizirati nekom vrijednošću ili joj kasnije pridružiti neku drugu vrijednost.
* += (NL.PJEDNKO) - kako bismo mogli povećavati vrijednost nekog ranije inicijaliziranog izraza za određenu vrijednost
* ++ (NL.PPLUS) - služi nam za inkrement, tj. povećava vrijednost varijable za 1


## Operacije s tipovima

Kako bismo išta mogli raditi s varijablama i vrijednostima koje unesemo, trebaju nam neke specifične operacije za svaki od podržanih tipova podataka.

### Broj

#### Osnovne operacije:
* + (NL.PLUS)
* - (NL.MINUS)
* * (NL.PUTA)
* / (NL.KROZ)

#### Usporedbe:
* < (NL.MANJE), <= (NL.MJEDNAKO)
* > (NL.VEĆE), => (NL.VJEDNAKO)
* = (NL.JEDNAKO), != (NL.NJEDNAKO)

#### Cast
* pretvaranje broja u string (NL.TOSTRING)

### String

#### Osnovne operacije:
* + (NL.PLUS) - kod stringa ova operacija predstavlja konkatenaciju

#### Usporedbe:
* = (NL.JEDNAKO)

#### Cast
* pretvaranje stringa u broj (NL.TOINT)

Osnovne operacije ne prihvaćaju _mješovite_ tipove, npr. broj+string, nego ako želimo takve izraze prvo se mora pretvoriti u isti tip, pri tome nam pomažu funkcije 
Operacije usporedbe vraćaju 1 (ako je izraz istinit) i 0 (ako je izraz lažan).


## Grananja

* if (NL.IF)

    if(uvjet)
       kod

* if else (NL.IF, NL.ELSE) 
    
    if(uvjet)
        kod
    else
        kod


## Petlje
 
* for (NL.FOR) - jezik prepoznaje i<broj2, i<=broj2 te da povećanje vrijednosti varijable i može ići na 3 načina ++i, i++, i+=broj3.

    for(i=broj1;i<broj2;i++)
        kod

* while (NL.WHILE)
    
    while(uvjet)
        kod

* do while (NL.DO,NL.WHILE)

    do
        kod
    while;


Primjetimo, _kod_ može biti jedna naredba ili više njih, a u tom slučaju sve naredbe se nalaze u vitičastim zagradama, (NL.VOTV,NL.VZATV). Također, uvjet, se odnosi isključivo na jedan uvjet, ne na više njih.


## Unos, ispis

* unos (NL.CIN) - omogućava korisniku unos brojeva i stringova s tipkovnice
* ispis (NL.COUT) - NL ima mogućnost ispisa broja, stringa, te vrijednosti varijabli


## Komentari

NL prepoznaje 2 vrste komentara:
* linijski (//)
* višelinijski (/**/)

