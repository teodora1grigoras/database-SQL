from flask import Flask, render_template, request, url_for, redirect
from flask_mysqldb import MySQL
from datetime import datetime


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'grigo_user'
app.config['MYSQL_PASSWORD'] = 'grigo_pass'
app.config['MYSQL_DB'] = 'fabrica'

mysql = MySQL(app)

@app.route('/')
def form():
    cursor = mysql.connection.cursor()
    return render_template('index.html')

@app.route('/index.html', methods=['POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            with mysql.connection.cursor() as cursor:
                # Verificare în baza de date (asigură-te că ai o tabelă 'utilizatori' cu coloanele 'name' și 'parola')
                query = "SELECT * FROM angajati WHERE nume = %s AND parola = %s"
                cursor.execute(query, (username, password))
                utilizator = cursor.fetchone()

                if utilizator:
                    return render_template('meniu.html', username=username)
                else:
                    error = "Credentiale invalide. Verifica numele si parola."
                    return render_template('index.html', error=error)
        except Exception as e:
            print(f"Error: {e}")
            error = "An error occurred while processing your request."
            return render_template('index.html', error=error)


@app.route('/meniu.html', methods=['POST', 'GET'])
def meniu():
    cursor = mysql.connection.cursor()
    query1="SELECT p.numePartener, p.dataExpirariiContractului "\
           "FROM parteneri p "\
            "WHERE p.idParteneri IN ( "\
                "SELECT idPartener "\
                "FROM comanda c "\
                "WHERE c.idComanda IN ( "\
                    "SELECT idComanda "\
                    "FROM comandaprodus cp "\
                    "WHERE cp.idProdus IN ( "\
                        "SELECT idProdus "\
                        "FROM produs pr "\
                        "WHERE pr.idMaterial IN ( "\
                            "SELECT idMateriale "\
                            "FROM materiale m "\
                            "WHERE m.pierderi = (SELECT MAX(pierderi) FROM materiale))))) AND p.tipPartener='client';"
    cursor.execute(query1)
    results = cursor.fetchone()
    return render_template('meniu.html', results=results)


@app.route('/products.html',  methods=['GET'])
def products():
   
    denumire = request.args.get('search', '')
    cursor = mysql.connection.cursor()

    descriere=denumire
    t  = (denumire, descriere, )

    if denumire:
        query ="SELECT denumire, pretUnitate, descriere FROM produs INNER JOIN categorie ON (denumire = %s OR descriere = %s)  AND   produs.idCategorie=categorie.idCategorie"
        cursor.execute(query, t)
        results = cursor.fetchall()
    else:  
        query ="SELECT denumire, pretUnitate, descriere FROM produs INNER JOIN categorie ON produs.idCategorie=categorie.idCategorie"
        cursor.execute(query)
        results = cursor.fetchall()
    
    if results:
        return render_template('products.html', results=results)
    else:
        
        error = "produsul nu exista in baza de date"
        return render_template('products.html', error=error)


@app.route('/materials.html', methods=['GET'])
def materials():
   
    denumire = request.args.get('search', '')
    cursor = mysql.connection.cursor()


    t  = (denumire, denumire, )

    if denumire:
        query ="SELECT denumire, pretUnitate, cantitate, numePartener FROM materiale INNER JOIN parteneri ON (denumire = %s OR parteneri.numePartener = %s)  AND  materiale.idPartener=parteneri.idParteneri"
        cursor.execute(query, t)
        results = cursor.fetchall()
    else:  
        query ="SELECT denumire, pretUnitate, cantitate, numePartener FROM materiale INNER JOIN parteneri ON materiale.idPartener=parteneri.idParteneri"
        cursor.execute(query)
        results = cursor.fetchall()
    
    if results:
        return render_template('materials.html', results=results)
    else:
        
        error = "produsul nu exista in baza de date"
        return render_template('materials.html', error=error)


@app.route('/parteneri.html', methods=['GET'])
def parteneri():
   
    numePartener = request.args.get('search', '')
    cursor = mysql.connection.cursor()

    if numePartener:
        query ="SELECT numePartener, tipPartener, dataExpirariiContractului, telefon, mail FROM parteneri INNER JOIN contact  ON numePartener = %s  AND   parteneri.idContact=contact.idContact"
        cursor.execute(query, [numePartener])
        results = cursor.fetchall()
    else:  
        query ="SELECT numePartener, tipPartener, dataExpirariiContractului, telefon, mail FROM parteneri INNER JOIN contact  ON   parteneri.idContact=contact.idContact "
        cursor.execute(query)
        results = cursor.fetchall()
    
    if results:
        return render_template('parteneri.html', results=results)
    else:
        
        error = "Partenerul nu exista in baza de date"
        return render_template('parteneri.html', error=error)


@app.route('/employees.html')
def angj():

    nume_prenume = request.args.get('angj', '')  # Use 'args' to get the query parameter from the URL
    cursor = mysql.connection.cursor()

    names = nume_prenume.split()

    if len(names) == 2:
            nume, prenume = names
    elif len(names) == 1:
            nume=prenume=names
    if len(names) == 0:
            query ="SELECT idAngajat, nume, prenume, CNP, telefon, mail, numeDepartament FROM angajati INNER JOIN contact ON (angajati.idContact=contact.idContact) INNER JOIN departament  ON (departament.idDepartament=angajati.idDepartament)"
            cursor.execute(query)
            results = cursor.fetchall()
    else:  
        query ="SELECT idAngajat,nume, prenume, CNP, telefon, mail, numeDepartament FROM angajati INNER JOIN contact ON angajati.idContact = contact.idContact INNER JOIN departament ON angajati.idDepartament = departament.idDepartament WHERE nume = %s OR prenume = %s"

        cursor.execute(query, (nume, prenume))
        results = cursor.fetchall()

    if results:
        return render_template('employees.html', results=results)
    else:
        
        error = "Angajatul nu exista in baza de date"
        return render_template('employees.html', error=error)

@app.route('/comenzi.html',  methods=['GET'])
def comenzi():
      
    data = request.args.get('search', '')
    cursor = mysql.connection.cursor()

    if data:
        # Convertiți data în format de dată, dacă este furnizată
        try:
            d = datetime.strptime(data, '%Y-%m-%d').date()
            query ="SELECT idComanda,  tipComanda, numePartener, dataComanda,  pretComanda, detalii FROM comanda INNER JOIN parteneri ON dataComanda = %s   AND  comanda.idPartener=parteneri.idParteneri"
            cursor.execute(query,[data])
            results = cursor.fetchall()
        except ValueError:
            query ="SELECT idComanda,  tipComanda, numePartener, dataComanda,  pretComanda, detalii FROM comanda INNER JOIN parteneri ON ( parteneri.numePartener = %s OR idComanda= %s)  AND  comanda.idPartener=parteneri.idParteneri"
            cursor.execute(query, [data, data])
            results = cursor.fetchall()
    else:  
        query ="SELECT idComanda,  tipComanda, numePartener, dataComanda,  pretComanda, detalii FROM comanda INNER JOIN parteneri ON comanda.idPartener=parteneri.idParteneri"
        cursor.execute(query)
        results = cursor.fetchall()
    
    if results:
        return render_template('comenzi.html', results=results)
    else:
        
        error = "comanda nu exista in baza de date"
        return render_template('comenzi.html', error=error)

@app.route('/produseexpediate.html',  methods=['GET'])
def prexp():
    data= request.args.get('search','')
    cursor= mysql.connection.cursor()

    query="SELECT denumire, pretUnitate, comandaprodus.cantitate from produs INNER JOIN comandaprodus where produs.idProdus=comandaprodus.idProdus AND comandaprodus.idComanda = (select idComanda from comanda where comanda.idPartener= (select idParteneri from parteneri where parteneri.tipPartener='client'AND parteneri.numePartener=%s))"
    cursor.execute(query,[data])
    results = cursor.fetchall()
    if results:
        return render_template('produseexpediate.html', results=results)
    else:
        error = "Nu exista rezultate"
        return render_template('produseexpediate.html', error=error)
    
@app.route('/produseprimite.html',  methods=['GET'])
def prpr():
    data= request.args.get('search','')
    cursor= mysql.connection.cursor()

    query="SELECT denumire, pretUnitate, comandaprodus.cantitate,  dataComanda  from materiale "\
            "INNER JOIN comandaprodus "\
            "INNER JOIN comanda "\
            "where materiale.idMateriale=comandaprodus.idProdus "\
            "AND comanda.idComanda=comandaprodus.idComanda AND comandaprodus.idComanda IN (select idComanda from comanda where comanda.idPartener= (select idParteneri from parteneri where parteneri.tipPartener='furnizor' AND parteneri.numePartener=%s))"
    cursor.execute(query,[data])
    results = cursor.fetchall()
    if results:
        return render_template('produseprimite.html', results=results)
    else:
        error = "Nu exista rezultate"
        return render_template('produseprimite.html', error=error)

@app.route('/add_employee', methods=['POST', 'GET'])
def add_employee():

    if request.method == 'POST':
        nume = request.form['nume']
        prenume = request.form['prenume']
        CNP = request.form['CNP']
        departament = request.form.get('departament')
        telefon = request.form.get('telefon')
        mail = request.form['mail']
        parola = request.form['parola']


        # Add other form fields as needed
        try:
            with mysql.connection.cursor() as cursor:
                # potrivirea id-ului departamentului cu numele din form
                cursor.execute("SELECT idDepartament FROM departament WHERE numeDepartament = %s", (departament,))
                idDepartament=cursor.fetchone()

                if idDepartament:
                    #actualizarea numaruluin de angajati din departament
                    query_actualizare = "UPDATE departament SET NrAngajati = NrAngajati + 1 WHERE idDepartament = %s"
                    cursor.execute(query_actualizare, (idDepartament,))

                    cursor.execute("SELECT idManager FROM departament WHERE numeDepartament = %s", (departament,))
                    idSupervizor=cursor.fetchone()

                    #introducerea datelor in tabela de contact
                    numeContact=f"{nume} {prenume}"
                    query1="INSERT INTO contact (NumeContact, telefon, mail) VALUES (%s, %s, %s)"
                    cursor.execute(query1, (numeContact,telefon, mail))
                    mysql.connection.commit()
                    cursor.execute("SELECT idContact FROM contact WHERE NumeContact = %s", (numeContact,))
                    idContact=cursor.fetchone()

                    query = "INSERT INTO angajati (nume, prenume, CNP, idDepartament, idContact, parola, idSupervizor) VALUES (%s, %s, %s, %s,%s,%s,%s)"
                    cursor.execute(query, (nume, prenume, CNP, idDepartament, idContact, parola, idSupervizor))
                    mysql.connection.commit()
                    success_message = "Angajat adăugat cu succes!"
                    return render_template('add_employee.html', success_message=success_message)
                else:
                    error_message = "Departamentul specificat nu există. Verifică departamentul și încearcă din nou."
                    return render_template('add_employee.html', error_message=error_message)
        except Exception as e:
            print(f"Error: {e}")
            error_message = "Eroare la adăugarea angajatului. Verifică datele și încearcă din nou."
            return render_template('add_employee.html', error_message=error_message)
    else:
        return render_template('add_employee.html')

@app.route('/schimbaParola/<username>', methods=['POST', 'GET'])
def change_password(username):
    if request.method == 'POST':
        old_password=request.form.get('old_password')
        new_password=request.form.get('new_password')

        try:
            with mysql.connection.cursor() as cursor:
                query="UPDATE angajati SET parola = %s WHERE nume = %s AND parola = %s"
                cursor.execute(query, (new_password,username,old_password ))
                mysql.connection.commit()
                success_message='Parola a fost schimbată cu succes!'
                return render_template('schimbaParola.html', success_message=success_message, username=username)
        except Exception as e:
                print(f"Error: {e}")
                # Anulare tranzacție în caz de eroare
                mysql.connection.rollback()
                error = "Eroare la schimbarea parolei."
                return render_template('schimbaParola.html', error_message=error)
    else:
        return render_template('schimbaParola.html',username=username)
    
@app.route('/succes/<id>', methods=['POST', 'GET'])
def delete_employee(id):
    try:
        cursor = mysql.connection.cursor()

        cursor.execute("SELECT idContact FROM angajati WHERE idAngajat = %s",(id,))
        idContact=cursor.fetchone()

        cursor.execute("SELECT idDepartament FROM angajati WHERE idAngajat = %s",(id,))
        idDepartament=cursor.fetchone()

        query = "DELETE FROM angajati WHERE idAngajat = %s"
        query1="DELETE FROM contact WHERE idContact = %s"
        cursor.execute(query, (id,))
        cursor.execute(query1, ( idContact,))

        query_actualizare = "UPDATE departament SET NrAngajati = NrAngajati - 1 WHERE idDepartament = %s"
        cursor.execute(query_actualizare, (idDepartament,))

        mysql.connection.commit()
        cursor.close()
        success_message = "Angajat eliminat cu succes!"
        return render_template('succes.html', success_message=success_message)
    except Exception as e:
        # Gestionează excepțiile, de exemplu, prin afișarea unui mesaj de eroare
        return render_template('succes.html', error=str(e))
    
@app.route('/departamente.html', methods=['GET'])
def departament():
   
    departament = request.args.get('search', '')
    cursor = mysql.connection.cursor()
    results2=0;
    if departament:
        query ="SELECT numeDepartament, nume,prenume, NrAngajati FROM departament INNER JOIN angajati ON numeDepartament = %s  AND   departament.idManager=angajati.idAngajat"
        cursor.execute(query, [departament])
        results = cursor.fetchall()

        query1="SELECT nume, prenume FROM angajati where idDepartament IN(SELECT idDepartament FROM departament WHERE numeDepartament = %s)"
        cursor.execute(query1, [departament])
        results1 = cursor.fetchall()

    else:  
        query ="SELECT numeDepartament, nume,prenume, NrAngajati FROM departament INNER JOIN angajati ON  departament.idManager=angajati.idAngajat"
        cursor.execute(query)
        results = cursor.fetchall()
        results1=0;
    
    if results:
        return render_template('departamente.html', results=results, results1=results1, results2=results2)
    else:
        
        error = "Departamentul nu exista in baza de date"
        return render_template('departamente.html', error=error)
@app.route('/departamente.html', methods=['POST'])
def angajati_barbati():
     cursor = mysql.connection.cursor()
     query="select NumeDepartament from departament where idDepartament IN (select idDepartament from angajati where  LEFT(CNP, 1) = '1' OR LEFT(CNP, 1) = '5')"
     cursor.execute(query)
     results2=cursor.fetchall()

     if results2:
         results=1;
         results1=1;
         return render_template('departamente.html', results=results, results1=results1, results2=results2)
     else:
        error = "Nu exista departamente cu angajati de genul masculin"
        return render_template('departamente.html', error=error)
# Creating a connection cursor
app.run(host='localhost', port=5000)
