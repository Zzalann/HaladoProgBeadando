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


