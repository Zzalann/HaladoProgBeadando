1. Ami már kész:
• Főmenü rendszer

„Pályaválasztás” gomb

„Kilépés” gomb

3 külön pálya választható (level1.txt, level2.txt, level3.txt)

• Pályaválasztás menü

1., 2., 3. pálya kiválasztása

Vissza gomb a főmenübe

• Játékmotor alapja (game.py)

Player mozgás (balra/jobbra)

Stabil ugrás (gravitációval, pontos ütközéssel)

Tile-alapú pálya betöltése .txt fájlokból

Platform ütközések (oldalról, alulról, felülről)

Win rendszer: cél jelölése → „WIN” kiírás → menübe vissza

Checkpoint jelölése (egyelőre csak sárga blokk)

Enemy pozíció megjelenítése (kék blokk, mozgás még nincs)

• A játékablak kitöltése

Minden pálya 1000×600 px (25×15 tile)

A TXT-s pálya pontosan kitölti a teljes ablakot

2. Egy pálya felépítése (TXT tilemap):

A pálya egy sima szövegfájl: level1.txt, level2.txt, level3.txt

Minden sor 25 karakter széles, minden pálya 15 sor magas.
Minden karakter jelent valamit:
Betű	Jelentése	Megjelenés
Fal / platform	Fekete blokk
P	Player kezdőpozíció	Piros négyzet
G	Célpont	Zöld négyzet
E	Ellenség helye	Kék négyzet
C	Checkpoint	Sárga négyzet
.	Üres tér	Semmi

A játék ezeket soronként beolvassa, és a megfelelő helyre rajzolja a blokkokat.

3. Ami már készen van:

Menük

Pályaválasztó rendszer

Pályák betöltése

Játékos mozgás

Ugrás és gravitáció

Ütközés platformokkal

Checkpoint megjelenítése

Enemy megjelenítése

Win → visszadob a menübe

Checkpoint rendszer

Ha a player hozzáér a checkpointhoz → felugrik egy kérdés

Többválasztós kvíz

Csak jó válasz után enged tovább a célhoz

„Feladom” gomb halállal

Player sprite

Enemy sprite

Háttérkép

UI szépítése

4. Ami még kell (következő fejlesztési lépések):

Ellenség AI működése

Idle (állás)

Ha a player közel kerül → üldözés

Ha messzire megy → visszatérés a kezdő pontra

Ha elkap → Game Over

Game Over képernyő

Újra próbálom




Vissza a menübe

Grafikai fejlesztések

Tile textúrák

