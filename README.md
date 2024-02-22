# database-SQL
Documentație
Fabrică încălțăminte-îmbrăcăminte

Introducere

Tema:
Aplicație pentru gestionarea unei fabrici de încălțăminte-îmbrăcăminte.

Descriere: 
Aplicația creată oferă o interfață prietenoasă pentru a gestiona datele unei fabrici de încălțăminte-îmbrăcăminte. Aceasta este creată folosind limbajele Python 3 cu Flask, HTML și CSS.

Aplicabilități: 
Aplicația oferă posibilitatea de a vizualiza toate datele bazei de date, cu posibilitatea de a caută detalii după denumirea anumitor câmpuri. Angajatul este si utilizatorul și pe pagina de logare se poate autentifica folosind ca utilizator: nume și parola sa.

Structura Bazei de date

Baza de date este creată din 9 tabele din care 1 de legatură.
 1.Angajati
 2.Departamente
 3.Contacte
 4.Parteneri
 5.Materiale
 6.Produse
 7.Categorie
 8.Comenzi
 9.Comenzi_Produse (tabel de legatura)
 
Cele 6 interogări simple se găsesc pe paginile:
- Employees.html
- Departamente.html
- Materials.html
- Parteneri.html
- Products.html
- Comenzi.html
  
Cele 5 interogări complexe sunt:
- datele produselor care au fost expediate la [select] pe pagina produseexpediate.html
- datele materialelor care au fost primite de la [select] pe pagina 
produseprimite.html
- Numele departamentului care are angajati ale caror cnp incepe cu 1 sau 5 
(departamente care au angajati barbati) [search] pe pagina departamente.html
- data de expirare a contractului cu clientul care are pierderile cele mai mari 
pentru materialele din care fabric produsele afișat pe pagina de meniu.html.
- angajații unui departament

Cele trei acțiuni sunt:
- Delete: ștergerea unui angajat din tabela de angajați împreună cu datele de 
contact din tabela de angajați și cu UPDATE la numărul de angajați din 
departamentul la care aparțineau (tabela departamente).
- Insert: adăugarea unui angajat in tabela de angajați si adăugarea datelor de 
contact ale acestuia în tabela de contacte plus UPDATE la numărul de 
angajați la departamentul la care a fost adăugat (tabela departament).
- Update: resetarea parolei din tabela de angajați, cele doua update-uri făcute 
pentru tabela departament in urma acțiunii de delete și insert

Concluzie:
Aplicația realizată reprezintă o interfață minimalistă pentru utilizarea și gestionarea bazei de date care conține posibilități de interogare pentru majoritatea tabelelor, ștergerea unui angajat, adăugarea unui angajat și schimbarea parolei utilizatorului (angajatul).
