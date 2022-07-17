import mysql.connector
class MyDatabase():
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456789",
        )
        self.cursor=self.connection.cursor(buffered=True);
        self.rows = []
        self.columns=[]
        self.prosecna_ocena=None
        self.create_database()
        self.connect_to_database()
        self.create_tables()
        self.fill_tables()

    def create_database(self):
        self.cursor.execute("DROP DATABASE IF EXISTS univerzitet_megatrend" )
        self.cursor.execute("CREATE DATABASE univerzitet_megatrend")
        print("Database created.")

    def connect_to_database(self):
        self.cursor.execute("USE univerzitet_megatrend")
        print("You're connected to database.")

    def create_tables(self):
        self.cursor.execute("CREATE TABLE gradovi (sifra int AUTO_INCREMENT, naziv VARCHAR(15) NOT NULL, PRIMARY KEY (sifra))")
        self.cursor.execute("CREATE TABLE adrese (sifra int AUTO_INCREMENT, sifra_grada int NOT NULL, naziv VARCHAR(50) NOT NULL, PRIMARY KEY (sifra), FOREIGN KEY (sifra_grada) REFERENCES gradovi(sifra) ON DELETE CASCADE)")
        self.cursor.execute("CREATE TABLE fakulteti (sifra int AUTO_INCREMENT, sifra_adrese int, naziv VARCHAR(50) NOT NULL, PRIMARY KEY (sifra), FOREIGN KEY (sifra_adrese) REFERENCES adrese(sifra) ON DELETE SET NULL)")
        self.cursor.execute("CREATE TABLE profesori (sifra int AUTO_INCREMENT, ime VARCHAR(15) NOT NULL, prezime VARCHAR(15) NOT NULL, email VARCHAR(50), PRIMARY KEY (sifra))")
        self.cursor.execute("CREATE TABLE studenti (sifra int AUTO_INCREMENT, ime VARCHAR(15) NOT NULL, prezime VARCHAR(15) NOT NULL,email VARCHAR(50), sifra_adrese int, godina int NOT NULL, PRIMARY KEY (sifra), FOREIGN KEY (sifra_adrese) REFERENCES adrese(sifra) ON DELETE SET NULL)")
        self.cursor.execute("CREATE TABLE predmeti (sifra int AUTO_INCREMENT, sifra_fakulteta int NOT NULL, sifra_profesora int, naziv VARCHAR(50) NOT NULL, broj_casova int NOT NULL, ESPB int NOT NULL, semestar int NOT NULL, godina int NOT NULL, PRIMARY KEY (sifra), FOREIGN KEY (sifra_fakulteta) REFERENCES fakulteti(sifra) ON DELETE CASCADE,FOREIGN KEY (sifra_profesora) REFERENCES profesori(sifra) ON DELETE SET NULL)")
        self.cursor.execute("CREATE TABLE predavanja (sifra int AUTO_INCREMENT, sifra_predmeta int NOT NULL, datum DATE, prostorija VARCHAR(15) NOT NULL, PRIMARY KEY (sifra), FOREIGN KEY (sifra_predmeta) REFERENCES predmeti(sifra) ON DELETE CASCADE)")
        self.cursor.execute("CREATE TABLE prisustvo (sifra int AUTO_INCREMENT, sifra_studenta int NOT NULL,prisustvovao BOOLEAN NOT NULL, PRIMARY KEY (sifra), FOREIGN KEY (sifra_studenta) REFERENCES studenti(sifra) ON DELETE CASCADE) ")
        self.cursor.execute("CREATE TABLE rokovi (sifra int AUTO_INCREMENT, naziv VARCHAR(15) NOT NULL, PRIMARY KEY (sifra))")
        self.cursor.execute("CREATE TABLE polaganje (sifra int AUTO_INCREMENT, sifra_predmeta int, sifra_studenta int NOT NULL, sifra_roka int NOT NULL, ocena int CHECK (ocena<=10 and ocena >=5), PRIMARY KEY (sifra), FOREIGN KEY (sifra_predmeta) REFERENCES predmeti(sifra) ON DELETE CASCADE,FOREIGN KEY (sifra_studenta) REFERENCES studenti(sifra) ON DELETE CASCADE,FOREIGN KEY (sifra_roka) REFERENCES rokovi(sifra) ON DELETE CASCADE)")
        print("Tables successfully created.")
        #Nisam nigde stavio on update zato sto je po defaultu no action, a to zelim da se desava da izlazi error ako neko proba da promeni glavni kljuc. Za on delete npr kod grada ako se obrise grad imaju i adrese da se obrisu zbog CASCADE to zelim da se desava, dok npr kod predmeta ako se obrise profesor ne zelim da se obrise i predmet zato ce da ide NULL.
        #Not null nije svugde stavljen jer su neki podaci manje bitni ili npr nisu dostupni a za neke u slucaju brisanja sifre iz tabele roditelja zelim da postanu null.

    def fill_tables(self):
        self.cursor.execute("INSERT INTO gradovi(naziv) VALUES ('Beograd'),('Novi Sad'),('Nis'),('Subotica')")
        self.cursor.execute("INSERT INTO adrese(sifra_grada,naziv) VALUES (3,'Ulica Zivota'),(2,'Ulica Ljubavi'),(1,'Ulica Srece')")
        self.cursor.execute("INSERT INTO fakulteti(sifra_adrese,naziv) VALUES (2,'Fakultet Poslovnih Studija'),(3,'Pravni Fakultet')")
        self.cursor.execute("INSERT INTO profesori(ime,prezime,email) VALUES ('Veljko','Veljkovic','veljkoveljkovic6436346@gmail.com'), ('Misa','Miskovic','misamiskovic5325523@gmail.com')")
        self.cursor.execute("INSERT INTO studenti(ime,prezime,email,sifra_adrese,godina) VALUES ('Petar','Petrovic','perapetrovic@gmail.com',1,2), ('Marija','Maric','marijamaric3@gmail.com',3,4)")
        self.cursor.execute("INSERT INTO predmeti(sifra_fakulteta,sifra_profesora,naziv,broj_casova,ESPB,semestar,godina) VALUES (2,1,'Racunarski Predmet',3,12,2,3),(1,2,'Logicki Predmet',2,8,1,3)")
        self.cursor.execute("INSERT INTO predavanja(sifra_predmeta,datum,prostorija) VALUES (1,'2000-1-1','K1'),(2,'2005-5-5','K3')")
        self.cursor.execute("INSERT INTO prisustvo(sifra_studenta,prisustvovao) VALUES (1,true), (2,false),(1,false),(2,true)")
        self.cursor.execute("INSERT INTO rokovi(naziv) VALUES ('Martovski'),('Januarski'),('Septembarski')")
        self.cursor.execute("INSERT INTO polaganje(sifra_predmeta,sifra_studenta,sifra_roka,ocena) VALUES (1,2,3,7),(2,1,1,10)")
        print("Tables sucessfully filled.")

    #Svi uneti podaci tipa string se moraju unositi izmedju '', ako stavim da se automatski prebacuju u string onda nece izlaziti error kada korisnik unese NULL.
    def show_results(self,tabela):
        self.columns = []
        self.rows=[]
        self.cursor.execute("SHOW COLUMNS FROM " + tabela)
        for k in self.cursor.fetchall():
            self.columns.append(k[0])
        self.cursor.execute("SELECT * FROM " + tabela)
        for k in self.cursor.fetchall():
            self.rows.append(list(k))

    def show_polaganja_without_keys(self):
        self.cursor.execute("DROP TABLE IF EXISTS desifrovano")
        self.cursor.execute("CREATE TABLE desifrovano AS (SELECT polaganje.sifra,predmeti.naziv AS predmet,studenti.ime AS ime,studenti.prezime as prezime,rokovi.naziv as rok,polaganje.ocena FROM polaganje JOIN predmeti ON predmeti.sifra = polaganje.sifra_predmeta JOIN studenti ON studenti.sifra = polaganje.sifra_studenta JOIN rokovi on rokovi.sifra = polaganje.sifra_roka ORDER BY polaganje.ocena DESC) " )
        self.show_results('desifrovano')
        #Stvara se nova tabela desifrovano, bice bazirana na tabeli polaganje, strani kljucevi iz tabele polaganje ce se povezati sa svojim tabelama da se izvuku vrednosti iz njih, ova tabela ce biti sortirana po ocenama od najvise do najnize.

    def update_data(self,data1,data2,data3,data4):
        self.cursor.execute("UPDATE " + data1 + " SET " + data3 + "= " + data4 + " WHERE sifra = " + str(data2) )

    def insert_data(self,data1,data2):
        self.cursor.execute("INSERT INTO " + data1 + " VALUES (null," + str(data2) +")")
        #Ovde iz nekog razloga zeli da se unese vrednost i primary keya a ako se ne unese onda place da se nije unelo dovoljno argumenata i kao da se ignorise AUTO_INCREMENT, problem resen tako sto se za primarni kljuc odredi NULL i tek onda on izvrsi AUTO INCREMENT na toj vrednosti.

    def delete_data(self,data1,data2):
        self.cursor.execute("DELETE FROM " + data1 + " WHERE sifra = " + str(data2))

    def change_name_of_table(self,data1,data2):
        self.cursor.execute("ALTER TABLE " + data1 + " RENAME TO " + data2)

    def show_average_grade_of_student(self,data1):
        self.cursor.execute("SELECT AVG(ocena) FROM polaganje WHERE ocena > 5 AND sifra_studenta = " + data1)
        self.prosecna_ocena=self.cursor.fetchall()
