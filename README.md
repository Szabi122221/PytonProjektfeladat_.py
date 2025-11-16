Kelemen Szabolcs


A program egy Tkinter alapú grafikus felülettel rendelkező alkalmazás, amely a dolgozók (név és kor) adatainak kezelésére szolgál. Lehetővé teszi új dolgozók hozzáadását, a meglévő lista név vagy kor szerinti rendezését, valamint az adatok CSV fájlból történő betöltését és CSV fájlba történő mentését.



Applikacio

A fő osztály, amely kezeli a felhasználói interakciókat, a widgetek elhelyezését és az adatok kezelését.

Metódusok:

__init__(self, root_ablak): Inicializálja az alkalmazást, beállítja a GUI elemeket és betölti az alap adatokat.

betolt_alap_adatok(self): Inicializál néhány alapértelmezett Dolgozo_KSZ_Osztaly objektumot.

frissit_lista(self): Frissíti a Listbox tartalmát a jelenlegi dolgozók listája alapján.

rendez_nev(self): Elindítja a név szerinti rendezést és frissíti a listát.

rendez_kor(self): Elindítja a kor szerinti rendezést és frissíti a listát.

hozzaad_dolgozo(self): Hozzáad egy új dolgozót a beviteli mezők adatai alapján, validálja a kort.

betolt_csv(self): Megnyit egy CSV fájlt, betölti az adatokat a listába, kezelve több kódolási hibát.

ment_csv(self): Elmenti a dolgozók listáját egy választott CSV fájlba.

(mentsd_adatbazisba(self, eredeti_fajlnev): (Nem használt, de definiált) Egy belső mentési metódus.)





Dolgozo_KSZ_Osztaly

A dolgozói adatokat reprezentáló osztály.

Metódusok:

__init__(self, nev, kor): Inicializálja a dolgozót a névvel (string) és a korral (integer).

__str__(self): Megadja a dolgozó objektum string reprezentációját (pl.: "Nagy Janos (45 ev)").

rendezes_ksz_fv(dolgozok, kulcs): Egy listányi Dolgozo_KSZ_Osztaly objektumot rendez a megadott kulcs ('nev' vagy 'kor') alapján.

Visszatérési érték: A rendezett dolgozói lista.
