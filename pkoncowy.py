from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from sqlalchemy.orm import sessionmaker
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, Table, String
from sqlalchemy.orm import declarative_base, relationship


root = Tk()
root.title("Szpital rejestracja")
root.iconbitmap('c:/gui/icon.ico')
root.geometry("872x900")


Base = declarative_base()

#Połączenie z bazą danych

engine = db.create_engine("mysql+pymysql://root:password123@localhost:3306/szpital")

# mapowanie tabel na klasy

class dzial(Base):
    __tablename__ = 'dzial'

    dzialID = Column(Integer, primary_key = True)
    nazwa = Column(String(20))
    diagnozaID = Column(Integer, ForeignKey("diagnoza.diagnozaID"))
    opiekunID = Column(Integer, ForeignKey("opiekun.opiekunID"))
    pacjentID = Column(Integer, ForeignKey("pacjent.pacjentID"))
    pacjent = relationship("pacjent")
    diagnoza = relationship("diagnoza")
    opiekun = relationship("opiekun")

class diagnoza(Base):
    __tablename__ = 'diagnoza'

    diagnozaID = Column(Integer, primary_key = True)
    choroba = Column(String(20))
    objaw = Column(String(20))
    poziom_zagrozenia_zycia = Column(String(20))
    leczenie = Column(String(20))

class pacjent(Base):
    __tablename__ = 'pacjent'

    pacjentID = Column(Integer, primary_key = True)
    imie = Column(String(20))
    nazwisko = Column(String(20))
    pesel = Column(db.String(20))

class opiekun(Base):
    __tablename__ = 'opiekun'

    opiekunID = db.Column(db.Integer, primary_key = True)
    imie = db.Column(db.String(20))
    nazwisko = db.Column(db.String(20))
    posada = db.Column(db.String(20))    

Session = sessionmaker(bind=engine)
sesja = Session()

roo = Frame(root)
roo.pack(side="top", expand=True, fill="both")

# mapowanie joinów do zmiennych globalnych

join_all = sesja.query(dzial, pacjent, opiekun, diagnoza). \
    select_from(dzial).join(pacjent).join(opiekun).join(diagnoza).all()

join_pacjent = sesja.query(dzial, pacjent).join(pacjent).all()

join_opiekun = sesja.query(dzial, opiekun).join(opiekun).all()

join_diagnoza = sesja.query(dzial, diagnoza).join(diagnoza).all()


def pacjenci():

    def czyscpacjent():
        box1.delete(0, END)
        box2.delete(0, END)
        box3.delete(0, END)


    def dodajpacjent(imie_n, nazwisko_n, pesel_n):
        n_pacjent = pacjent(imie=imie_n, nazwisko=nazwisko_n, pesel=pesel_n)
        wynik = sesja.add(n_pacjent)
        sesja.commit()


        pacjenci()

    def szukajpacjent():

        def wypisz():
            # pasek wyszukiwania
            wczytaj = Entry(szu)
            wczytaj.grid(row=0, column=1, padx=10, pady=10)

            szukaj = Label(szu, text="Wyszukaj pacjentow")
            szukaj.grid(row=0, column=0, padx=10, pady=10)

            wybierz = ttk.Combobox(szu, values=['Wyszukaj po.. ', 'Imieniu', 'Nazwisku', 'Peselu'])
            wybierz.current(0)
            wybierz.grid(row=0, column=2,columnspan=2)

            przycisk = Button(szu, text="Szukaj", command=lambda: szuk(wczytaj.get(), wybierz.get()))
            przycisk.grid(row=1, column=0)

        def edytuj(id):

            def czyscpacjent():
                box1.delete(0, END)
                box2.delete(0, END)
                box3.delete(0, END)

            def update(id, n_imie, n_nazwisko, n_pesel):
                wynik_edycji = sesja.query(pacjent).filter(pacjent.pacjentID == id).first()
                wynik_edycji.imie = n_imie
                wynik_edycji.nazwisko = n_nazwisko
                wynik_edycji.pesel = n_pesel
                sesja.commit()

                edt.destroy()
                pacjenci()

            edt = Tk()
            edt.title("Edycja danych")
            edt.iconbitmap('c:/gui/icon.ico')
            edt.geometry("400x400")

            tytul = Label(edt, text="Edycja danych dla tabeli: Pacjent", font=("Arial", 12, 'bold'))
            tytul.grid(row=0, column=1, columnspan=3, sticky=W)

            label1 = Label(edt, text="Imie", font=("Arial", 12)).grid(column=1, row=2, sticky=W, padx=5, pady=10)
            label2 = Label(edt, text="Nazwisko", font=("Arial", 12)).grid(column=1, row=3, sticky=W, padx=5, pady=10)
            label3 = Label(edt, text="Pesel", font=("Arial", 12)).grid(column=1, row=4, sticky=W, padx=5, pady=10)

            box1 = Entry(edt)
            box1.grid(column=2, row=2)
            box2 = Entry(edt)
            box2.grid(column=2, row=3)
            box3 = Entry(edt)
            box3.grid(column=2, row=4)


            dod = Button(edt, text="Zatwierdz zmiany", padx=20, pady=10,command=lambda: update(id, box1.get(), box2.get(), box3.get()))
            dod.grid(column=1, row=6, sticky=W, padx=20, pady=20)
            czysc = Button(edt, text="Wyczysc", padx=20, pady=10, command=czyscpacjent)
            czysc.grid(column=2, row=6, sticky=W, padx=20, pady=20)

        def usunpacjent(id):
            usun = sesja.query(pacjent).filter(pacjent.pacjentID == id).first()
            sesja.delete(usun)
            sesja.commit()

            for widgets in szu.winfo_children():
                widgets.destroy()
            wypisz()
            pacjenci()

        def szuk(dan, wybor):

            for widgets in szu.winfo_children():
                widgets.destroy()

            wypisz()

            if wybor == 'Imieniu':
                wynik_szukania = sesja.query(pacjent).filter(pacjent.imie == dan)
            if wybor == 'Nazwisku':
                wynik_szukania = sesja.query(pacjent).filter(pacjent.nazwisko == dan)
            if wybor == 'Peselu':
                wynik_szukania = sesja.query(pacjent).filter(pacjent.pesel == dan)


            label01 = Label(szu, text="ID", font=('arial', 10, "bold")).grid(column=2, row=2,sticky=W)
            label12 = Label(szu, text="Imie", font=('arial', 10, "bold")).grid(column=3, row=2,sticky=W)
            label21 = Label(szu, text="Nazwisko", font=('arial', 10, "bold")).grid(column=4, row=2,sticky=W)
            label31 = Label(szu, text="Pesel", font=('arial', 10, "bold")).grid(column=5, row=2,sticky=W)

            wr = 3
            ko = 0
            for r in wynik_szukania:
                e_przycisk = Button(szu, text="Edytuj", command=lambda: edytuj(r.pacjentID))
                u_przycisk = Button(szu, text='Usun', command=lambda: usunpacjent(r.pacjentID))
                e_przycisk.grid(row=wr, column=ko)
                u_przycisk.grid(row=wr, column=ko+1)
                label00 = Label(szu, text=r.pacjentID, font=('arial', 10)).grid(column=ko+2, row=wr, sticky=W)
                label11 = Label(szu, text=r.imie, font=('arial', 10)).grid(column=ko + 3, row=wr, sticky=W)
                label22 = Label(szu, text=r.nazwisko, font=('arial', 10)).grid(column=ko + 4, row=wr, sticky=W)
                label33 = Label(szu, text=r.pesel, font=('arial', 10)).grid(column=ko + 5, row=wr, sticky=W)
                wr = wr + 1



        szu = Tk()
        szu.title("Szukaj pacjentow")
        szu.iconbitmap('c:/gui/icon.ico')
        szu.geometry("1000x800")
        wypisz()

    clear_frame()
    root.title("Pacjeci w szpitalu")
    cof = Button(roo, text="cofnij", padx=10, pady=5, command=ekran_poczatek)
    cof.grid(row=0, column=0,sticky=W)
    tytul = Label(roo, text="Dodaj do bazy pacjeta:", font=("Arial", 12,'bold'))
    tytul.grid(row=0, column=1,columnspan=3,sticky=W)

    label1 = Label(roo, text="Imie",font=("Arial", 12)).grid(column=1,row=2,sticky=W,padx=5,pady=10)
    label2 = Label(roo, text="Nazwisko", font=("Arial", 12)).grid(column=1, row=3,sticky=W,padx=5,pady=10)
    label3 = Label(roo, text="Pesel", font=("Arial", 12)).grid(column=1, row=4,sticky=W,padx=5,pady=10)

    box1 = Entry(roo)
    box1.grid(column=2, row=2)
    box2 = Entry(roo)
    box2.grid(column=2, row=3)
    box3 = Entry(roo)
    box3.grid(column=2, row=4)


    dodpacjentow = Button(roo, text="Dodaj", padx=20, pady=10, command=lambda:dodajpacjent(box1.get(), box2.get(), box3.get()))
    dodpacjentow.grid(column=1, row=6, sticky=W, padx=20, pady=20)
    czys = Button(roo, text="Czysc", padx=20, pady=10, command=czyscpacjent)
    czys.grid(column=2, row=6, sticky=W, padx=20, pady=20)
    szukaj = Button(roo, text="Szukaj w bazie pacjentow", padx=20, pady=10, command=szukajpacjent)
    szukaj.grid(column=3, row=6, sticky=W, padx=20, pady=20,columnspan=3)


    podglad = Label(roo, text="Zarejestrowani Pacjenci", font=("Arial", 12, 'bold')).grid(column=0, row=7, sticky=W,padx=5, pady=10,columnspan=4)

    label00 = Label(roo, text="ID", font=('arial', 10, "bold")).grid(column=0, row=8,sticky=W)
    label11 = Label(roo, text="Imie", font=('arial', 10, "bold")).grid(column=1, row=8,sticky=W)
    label22 = Label(roo, text="Nazwisko", font=('arial', 10, "bold")).grid(column=2, row=8,sticky=W)
    label33 = Label(roo, text="Pesel", font=('arial', 10, "bold")).grid(column=3, row=8,sticky=W)

    dowys = sesja.query(pacjent)
    wr = 9
    ko = 0
    for r in dowys:
        label00 = Label(roo, text=r.pacjentID, font=('arial', 10)).grid(column=ko, row=wr,sticky=W)
        label11 = Label(roo, text=r.imie, font=('arial', 10)).grid(column=ko + 1, row=wr,sticky=W)
        label22 = Label(roo, text=r.nazwisko, font=('arial', 10)).grid(column=ko + 2, row=wr,sticky=W)
        label33 = Label(roo, text=r.pesel, font=('arial', 10)).grid(column=ko + 3, row=wr,sticky=W)
        wr = wr + 1


def opiekuni():

    def czyscopiekun():
        box1.delete(0, END)
        box2.delete(0, END)
        box3.delete(0, END)


    def dodajopiekun(imie_n, nazwisko_n, posada_n):
        n_opiekun = opiekun(imie=imie_n, nazwisko=nazwisko_n, posada=posada_n)
        wynik = sesja.add(n_opiekun)
        sesja.commit()


        opiekuni()

    def szukajopiekun():

        def wypisz():
            # pasek wyszukiwania
            wczytaj = Entry(szu)
            wczytaj.grid(row=0, column=1, padx=10, pady=10)

            szukaj = Label(szu, text="Wyszukaj opiekunow")
            szukaj.grid(row=0, column=0, padx=10, pady=10)

            wybierz = ttk.Combobox(szu, values=['Wyszukaj po.. ', 'Imieniu', 'Nazwisku', 'Posadzie'])
            wybierz.current(0)
            wybierz.grid(row=0, column=2,columnspan=2)

            przycisk = Button(szu, text="Szukaj", command=lambda: szuk(wczytaj.get(), wybierz.get()))
            przycisk.grid(row=1, column=0)

        def edytuj(id):

            def czyscopiekun():
                box1.delete(0, END)
                box2.delete(0, END)
                box3.delete(0, END)

            def update(id, n_imie, n_nazwisko, n_posada):
                wynik_edycji = sesja.query(opiekun).filter(opiekun.opiekunID == id).first()
                wynik_edycji.imie = n_imie
                wynik_edycji.nazwisko = n_nazwisko
                wynik_edycji.posada = n_posada
                sesja.commit()

                edt.destroy()
                opiekuni()

            edt = Tk()
            edt.title("Edycja danych")
            edt.iconbitmap('c:/gui/icon.ico')
            edt.geometry("400x400")

            tytul = Label(edt, text="Edycja danych dla tabeli: Opiekun", font=("Arial", 12, 'bold'))
            tytul.grid(row=0, column=1, columnspan=3, sticky=W)

            label1 = Label(edt, text="Imie", font=("Arial", 12)).grid(column=1, row=2, sticky=W, padx=5, pady=10)
            label2 = Label(edt, text="Nazwisko", font=("Arial", 12)).grid(column=1, row=3, sticky=W, padx=5, pady=10)
            label3 = Label(edt, text="Posada", font=("Arial", 12)).grid(column=1, row=4, sticky=W, padx=5, pady=10)

            box1 = Entry(edt)
            box1.grid(column=2, row=2)
            box2 = Entry(edt)
            box2.grid(column=2, row=3)
            box3 = Entry(edt)
            box3.grid(column=2, row=4)


            dod = Button(edt, text="Zatwierdz zmiany", padx=20, pady=10,command=lambda: update(id, box1.get(), box2.get(), box3.get()))
            dod.grid(column=1, row=6, sticky=W, padx=20, pady=20)
            czysc = Button(edt, text="Wyczysc", padx=20, pady=10, command=czyscopiekun)
            czysc.grid(column=2, row=6, sticky=W, padx=20, pady=20)

        def usunopiekun(id):
            usun = sesja.query(opiekun).filter(opiekun.opiekunID == id).first()
            sesja.delete(usun)
            sesja.commit()

            for widgets in szu.winfo_children():
                widgets.destroy()
            wypisz()
            opiekuni()

        def szuk(dan, wybor):

            for widgets in szu.winfo_children():
                widgets.destroy()

            wypisz()

            if wybor == 'Imieniu':
                wynik_szukania = sesja.query(opiekun).filter(opiekun.imie == dan)
            if wybor == 'Nazwisku':
                wynik_szukania = sesja.query(opiekun).filter(opiekun.nazwisko == dan)
            if wybor == 'Posadzie':
                wynik_szukania = sesja.query(opiekun).filter(opiekun.posada == dan)


            label01 = Label(szu, text="ID", font=('arial', 10, "bold")).grid(column=2, row=2,sticky=W)
            label12 = Label(szu, text="Imie", font=('arial', 10, "bold")).grid(column=3, row=2,sticky=W)
            label21 = Label(szu, text="Nazwisko", font=('arial', 10, "bold")).grid(column=4, row=2,sticky=W)
            label31 = Label(szu, text="Posada", font=('arial', 10, "bold")).grid(column=5, row=2,sticky=W)

            wr = 3
            ko = 0
            for r in wynik_szukania:
                e_przycisk = Button(szu, text="Edytuj", command=lambda: edytuj(r.opiekunID))
                u_przycisk = Button(szu, text='Usun', command=lambda: usunopiekun(r.opiekunID))
                e_przycisk.grid(row=wr, column=ko)
                u_przycisk.grid(row=wr, column=ko+1)
                label00 = Label(szu, text=r.opiekunID, font=('arial', 10)).grid(column=ko+2, row=wr, sticky=W)
                label11 = Label(szu, text=r.imie, font=('arial', 10)).grid(column=ko + 3, row=wr, sticky=W)
                label22 = Label(szu, text=r.nazwisko, font=('arial', 10)).grid(column=ko + 4, row=wr, sticky=W)
                label33 = Label(szu, text=r.posada, font=('arial', 10)).grid(column=ko + 5, row=wr, sticky=W)
                wr = wr + 1



        szu = Tk()
        szu.title("Szukaj opiekunow")
        szu.iconbitmap('c:/gui/icon.ico')
        szu.geometry("1000x800")
        wypisz()

    clear_frame()
    root.title("Opiekuni w szpitalu")
    cof = Button(roo, text="cofnij", padx=10, pady=5, command=ekran_poczatek)
    cof.grid(row=0, column=0,sticky=W)
    tytul = Label(roo, text="Dodaj do bazy opiekuna:", font=("Arial", 12,'bold'))
    tytul.grid(row=0, column=1,columnspan=3,sticky=W)

    label1 = Label(roo, text="Imie",font=("Arial", 12)).grid(column=1,row=2,sticky=W,padx=5,pady=10)
    label2 = Label(roo, text="Nazwisko", font=("Arial", 12)).grid(column=1, row=3,sticky=W,padx=5,pady=10)
    label3 = Label(roo, text="Posada", font=("Arial", 12)).grid(column=1, row=4,sticky=W,padx=5,pady=10)

    box1 = Entry(roo)
    box1.grid(column=2, row=2)
    box2 = Entry(roo)
    box2.grid(column=2, row=3)
    box3 = Entry(roo)
    box3.grid(column=2, row=4)


    dodajopiekunow = Button(roo, text="Dodaj", padx=20, pady=10, command=lambda:dodajopiekun(box1.get(), box2.get(), box3.get()))
    dodajopiekunow.grid(column=1, row=6, sticky=W, padx=20, pady=20)
    czys = Button(roo, text="Czysc", padx=20, pady=10, command=czyscopiekun)
    czys.grid(column=2, row=6, sticky=W, padx=20, pady=20)
    szukaj = Button(roo, text="Szukaj w bazie opiekunow", padx=20, pady=10, command=szukajopiekun)
    szukaj.grid(column=3, row=6, sticky=W, padx=20, pady=20,columnspan=3)


    podglad = Label(roo, text="Zatrudnieni Opiekunowie", font=("Arial", 12, 'bold')).grid(column=0, row=7, sticky=W,padx=5, pady=10,columnspan=4)

    label00 = Label(roo, text="ID", font=('arial', 10, "bold")).grid(column=0, row=8,sticky=W)
    label11 = Label(roo, text="Imie", font=('arial', 10, "bold")).grid(column=1, row=8,sticky=W)
    label22 = Label(roo, text="Nazwisko", font=('arial', 10, "bold")).grid(column=2, row=8,sticky=W)
    label33 = Label(roo, text="Posada", font=('arial', 10, "bold")).grid(column=3, row=8,sticky=W)

    dowys = sesja.query(opiekun)
    wr = 9
    ko = 0
    for r in dowys:
        label00 = Label(roo, text=r.opiekunID, font=('arial', 10)).grid(column=ko, row=wr,sticky=W)
        label11 = Label(roo, text=r.imie, font=('arial', 10)).grid(column=ko + 1, row=wr,sticky=W)
        label22 = Label(roo, text=r.nazwisko, font=('arial', 10)).grid(column=ko + 2, row=wr,sticky=W)
        label33 = Label(roo, text=r.posada, font=('arial', 10)).grid(column=ko + 3, row=wr,sticky=W)
        wr = wr + 1


def dzialy():

    def dodajdzial(nazwa_n, diagnozaID_n, opiekunID_n, pacjentID_n):
        n_dzial = dzial(nazwa=nazwa_n, diagnozaID=diagnozaID_n, opiekunID=opiekunID_n, pacjentID=pacjentID_n)
        wynik = sesja.add(n_dzial)
        sesja.commit()

        dzialy()

    def szukajdzial():

        def wypisz():
            # pasek wyszukiwania
            wczytaj = Entry(szu)
            wczytaj.grid(row=0, column=1, padx=10, pady=10)

            szukaj = Label(szu, text="Wyszukaj dzialy")
            szukaj.grid(row=0, column=0, padx=10, pady=10)

            wybierz = ttk.Combobox(szu, values=['Wyszukaj po.. ', 'Nazwa', 'ID opiekun', 'ID pacjent', 'ID diagnoza'])
            wybierz.current(0)
            wybierz.grid(row=0, column=2,columnspan=2)

            przycisk = Button(szu, text="Szukaj", command=lambda: szuk(wczytaj.get(), wybierz.get()))
            przycisk.grid(row=1, column=0)

        def edytuj(id):
                
            def czyscdzial():
                box1.delete(0, END)
                box2.delete(0, END)
                box3.delete(0, END)
                box4.delete(0, END)

            def update(id, n_nazwa, n_diagnozaID, n_opiekunID, n_pacjentID):
                wynik_edycji = sesja.query(dzial).filter(dzial.dzialID == id).first()
                wynik_edycji.nazwa = n_nazwa
                wynik_edycji.diagnozaID = n_diagnozaID
                wynik_edycji.opiekunID = n_opiekunID
                wynik_edycji.pacjentID = n_pacjentID
                sesja.commit()

                edt.destroy()
                dzialy()

            edt = Tk()
            edt.title("Edycja danych")
            edt.iconbitmap('c:/gui/icon.ico')
            edt.geometry("400x400")

            tytul = Label(edt, text="Edycja danych dla tabeli: Dzial", font=("Arial", 12, 'bold'))
            tytul.grid(row=0, column=1, columnspan=3, sticky=W)

            label1 = Label(edt, text="Nazwa", font=("Arial", 12)).grid(column=1, row=2, sticky=W, padx=5, pady=10)
            label2 = Label(edt, text="ID diagnozy", font=("Arial", 12)).grid(column=1, row=3, sticky=W, padx=5, pady=10)
            label3 = Label(edt, text="ID opiekuna", font=("Arial", 12)).grid(column=1, row=4, sticky=W, padx=5, pady=10)
            label4 = Label(edt, text="ID pacjenta", font=("Arial", 12)).grid(column=1, row=5, sticky=W, padx=5, pady=10)

            box1 = Entry(edt)
            box1.grid(column=2, row=2)
            box2 = Entry(edt)
            box2.grid(column=2, row=3)
            box3 = Entry(edt)
            box3.grid(column=2, row=4)
            box4 = Entry(edt)
            box4.grid(column=2, row=5)


            dod = Button(edt, text="Zatwierdz zmiany", padx=20, pady=10,command=lambda: update(id, box1.get(), box2.get(), box3.get(), box4.get()))
            dod.grid(column=1, row=6, sticky=W, padx=20, pady=20)
            czysc = Button(edt, text="Wyczysc", padx=20, pady=10, command=czyscdzial)
            czysc.grid(column=2, row=6, sticky=W, padx=20, pady=20)

        def usundzial(id):
            usun = sesja.query(dzial).filter(dzial.dzialID == id).first()
            sesja.delete(usun)
            sesja.commit()

            for widgets in szu.winfo_children():
                widgets.destroy()
            wypisz()
            dzialy()

        def szuk(dan, wybor):

            for widgets in szu.winfo_children():
                widgets.destroy()

            wypisz()

            if wybor == 'Nazwa':
                wynik_szukania = sesja.query(dzial).filter(dzial.nazwa == dan)
            if wybor == 'ID opiekun':
                wynik_szukania = sesja.query(dzial).filter(dzial.opiekunID == dan)
            if wybor == 'ID pacjent':
                wynik_szukania = sesja.query(dzial).filter(dzial.pacjentID == dan)
            if wybor == 'ID diagnoza':
                wynik_szukania = sesja.query(dzial).filter(dzial.diagnozaID == dan)


            label01 = Label(szu, text="ID", font=('arial', 10, "bold")).grid(column=2, row=2,sticky=W)
            label12 = Label(szu, text="Nazwa", font=('arial', 10, "bold")).grid(column=3, row=2,sticky=W)
            label21 = Label(szu, text="ID diagnoza", font=('arial', 10, "bold")).grid(column=4, row=2,sticky=W)
            label31 = Label(szu, text="ID opiekun", font=('arial', 10, "bold")).grid(column=5, row=2,sticky=W)
            label41 = Label(szu, text="ID pacjent", font=('arial', 10, "bold")).grid(column=6, row=2, sticky=W)    
            wr = 3
            ko = 0
            for r in wynik_szukania:
                e_przycisk = Button(szu, text="Edytuj", command=lambda: edytuj(r.dzialID))
                u_przycisk = Button(szu, text='Usun', command=lambda: usundzial(r.dzialID))
                e_przycisk.grid(row=wr, column=ko)
                u_przycisk.grid(row=wr, column=ko+1)
                label00 = Label(szu, text=r.dzialID, font=('arial', 10)).grid(column=ko+2, row=wr, sticky=W)
                label11 = Label(szu, text=r.nazwa, font=('arial', 10)).grid(column=ko + 3, row=wr, sticky=W)
                label22 = Label(szu, text=r.diagnozaID, font=('arial', 10)).grid(column=ko + 4, row=wr, sticky=W)
                label33 = Label(szu, text=r.opiekunID, font=('arial', 10)).grid(column=ko + 5, row=wr, sticky=W)
                label33 = Label(szu, text=r.pacjentID, font=('arial', 10)).grid(column=ko + 6, row=wr, sticky=W)

                wr = wr + 1



        szu = Tk()
        szu.title("Szukaj Dzialy")
        szu.iconbitmap('c:/gui/icon.ico')
        szu.geometry("800x800")
        wypisz()

    clear_frame()

    def diaginfo():
        clear_frame()
        add()
        label00 = Label(roo, text="ID", font=('arial', 10, "bold")).grid(column=0, row=8, sticky=W)
        label11 = Label(roo, text="Nazwa", font=('arial', 10, "bold")).grid(column=1, row=8, sticky=W)
        label22 = Label(roo, text="ID Diagnozy", font=('arial', 10, "bold")).grid(column=2, row=8, sticky=W)
        label33 = Label(roo, text="Choroba", font=('arial', 10, "bold")).grid(column=3, row=8, sticky=W)
        label44 = Label(roo, text="Objaw", font=('arial', 10, "bold")).grid(column=4, row=8, sticky=W)
        label55 = Label(roo, text="Zagrozenie", font=('arial', 10, "bold")).grid(column=5, row=8, sticky=W)
        label66 = Label(roo, text="Leczenie", font=('arial', 10, "bold")).grid(column=6, row=8, sticky=W)

        wr = 9
        ko = 0

        for dzial, diagnoza in join_diagnoza:
            label00 = Label(roo, text=dzial.dzialID, font=('arial', 10)).grid(column=ko, row=wr, sticky=W)
            label11 = Label(roo, text=dzial.nazwa, font=('arial', 10)).grid(column=ko + 1, row=wr, sticky=W)
            label22 = Label(roo, text=diagnoza.diagnozaID, font=('arial', 10)).grid(column=ko + 2, row=wr, sticky=W)
            label33 = Label(roo, text=diagnoza.choroba, font=('arial', 10)).grid(column=ko + 3, row=wr, sticky=W)
            label44 = Label(roo, text=diagnoza.objaw, font=('arial', 10)).grid(column=ko + 4, row=wr, sticky=W)
            label55 = Label(roo, text=diagnoza.poziom_zagrozenia_zycia, font=('arial', 10)).grid(column=ko + 5, row=wr, sticky=W)
            label66 = Label(roo, text=diagnoza.leczenie, font=('arial', 10)).grid(column=ko + 6, row=wr, sticky=W)
            wr = wr + 1



    def opieinfo():
        clear_frame()
        add()
        label00 = Label(roo, text="ID", font=('arial', 10, "bold")).grid(column=0, row=8, sticky=W)
        label11 = Label(roo, text="Nazwa", font=('arial', 10, "bold")).grid(column=1, row=8, sticky=W)
        label22 = Label(roo, text="ID Opiekuna", font=('arial', 10, "bold")).grid(column=2, row=8, sticky=W)
        label33 = Label(roo, text="Imie", font=('arial', 10, "bold")).grid(column=3, row=8, sticky=W)
        label44 = Label(roo, text="Nazwisko", font=('arial', 10, "bold")).grid(column=4, row=8, sticky=W)
        label55 = Label(roo, text="Posada", font=('arial', 10, "bold")).grid(column=5, row=8, sticky=W)


        wr = 9
        ko = 0

        for dzial, opiekun in join_opiekun:
            label00 = Label(roo, text=dzial.dzialID, font=('arial', 10)).grid(column=ko, row=wr, sticky=W)
            label11 = Label(roo, text=dzial.nazwa, font=('arial', 10)).grid(column=ko + 1, row=wr, sticky=W)
            label22 = Label(roo, text=opiekun.opiekunID, font=('arial', 10)).grid(column=ko + 2, row=wr, sticky=W)
            label33 = Label(roo, text=opiekun.imie, font=('arial', 10)).grid(column=ko + 3, row=wr, sticky=W)
            label44 = Label(roo, text=opiekun.nazwisko, font=('arial', 10)).grid(column=ko + 4, row=wr, sticky=W)
            label55 = Label(roo, text=opiekun.posada, font=('arial', 10)).grid(column=ko + 5, row=wr, sticky=W)
            wr = wr + 1


    def pacinfo():
        clear_frame()
        add()
        label00 = Label(roo, text="ID", font=('arial', 10, "bold")).grid(column=0, row=8, sticky=W)
        label11 = Label(roo, text="Nazwa", font=('arial', 10, "bold")).grid(column=1, row=8, sticky=W)
        label22 = Label(roo, text="ID Pacjenta", font=('arial', 10, "bold")).grid(column=2, row=8, sticky=W)
        label33 = Label(roo, text="Imie", font=('arial', 10, "bold")).grid(column=3, row=8, sticky=W)
        label44 = Label(roo, text="Nazwisko", font=('arial', 10, "bold")).grid(column=4, row=8, sticky=W)
        label55 = Label(roo, text="Pesel", font=('arial', 10, "bold")).grid(column=5, row=8, sticky=W)


        wr = 9
        ko = 0

        for dzial, pacjent in join_pacjent:
            label00 = Label(roo, text=dzial.dzialID, font=('arial', 10)).grid(column=ko, row=wr, sticky=W)
            label11 = Label(roo, text=dzial.nazwa, font=('arial', 10)).grid(column= ko + 1, row=wr, sticky=W)
            label22 = Label(roo, text=pacjent.pacjentID, font=('arial', 10)).grid(column= ko + 2, row=wr, sticky=W)
            label33 = Label(roo, text=pacjent.imie, font=('arial', 10)).grid(column= ko + 3, row=wr, sticky=W)
            label44 = Label(roo, text=pacjent.nazwisko, font=('arial', 10)).grid(column = ko + 4, row=wr, sticky=W)
            label55 = Label(roo, text=pacjent.pesel, font=('arial', 10)).grid(column= ko + 5, row=wr, sticky=W)
            wr = wr + 1


    def add():

        def czyscdzial():
            box11.delete(0, END)
            box22.delete(0, END)
            box33.delete(0, END)
            box44.delete(0, END)

        root.title("Dzialy w szpitalu")
        cof = Button(roo, text="cofnij", padx=20, pady=5, command=ekran_poczatek)
        cof.grid(row=0, column=0,sticky=W)
        tytul = Label(roo, text="Dodaj do bazy Dzialy:", font=("Arial", 12,'bold'),)
        tytul.grid(row=0, column=1,columnspan=3)

        label1 = Label(roo, text="Nazwa",font=("Arial", 12)).grid(column=1,row=2,sticky=W,padx=5,pady=10)
        label2 = Label(roo, text="ID Diagnozy", font=("Arial", 12)).grid(column=1, row=3,sticky=W,padx=5,pady=10)
        label3 = Label(roo, text="ID Opiekuna", font=("Arial", 12)).grid(column=1, row=4,sticky=W,padx=5,pady=10)
        label4 = Label(roo, text="ID Pacjenta", font=("Arial", 12)).grid(column=1, row=5, sticky=W, padx=5, pady=10)

        box11 = Entry(roo)
        box11.grid(column=2, row=2,sticky=W)
        box22 = Entry(roo)
        box22.grid(column=2, row=3,sticky=W)
        box33 = Entry(roo)
        box33.grid(column=2, row=4,sticky=W)
        box44 = Entry(roo)
        box44.grid(column=2, row=5,sticky=W)

        dodajdzialy = Button(roo, text="Dodaj", padx=5, pady=10, command=lambda:dodajdzial(box11.get(), box22.get(), box33.get(), box44.get()))
        dodajdzialy.grid(column=1, row=6, sticky=W, padx=5, pady=20)
        czysc = Button(roo, text="Czysc", padx=5, pady=10, command=czyscdzial)
        czysc.grid(column=2, row=6, sticky=W, padx=5, pady=20)
        szukaj = Button(roo, text="Szukaj w bazie dzialow", padx=20, pady=10, command=szukajdzial)
        szukaj.grid(column=3, row=6, sticky=W, padx=20, pady=20,columnspan=3)

        label5 = Label(roo, text="Zobacz w dziale: ", font=("Arial", 12,'bold')).grid(column=6, row=0, sticky=W, padx=5, pady=10,columnspan=3)
        diagnozy = Button(roo, text="Diagnozy", command=diaginfo)
        diagnozy.grid(column=6, row=2, sticky=W,columnspan=2)
        opiekunowie = Button(roo, text="Opiekunow", command=opieinfo)
        opiekunowie.grid(column=7, row=3, sticky=W,columnspan=2)
        pacjenci = Button(roo, text="Pacjentow", command=pacinfo)
        pacjenci.grid(column=8, row=4, sticky=W, columnspan=2)
        podgladan = Label(roo, text="Podgląd bazy szpitala", font=("Arial", 12, 'bold')).grid(column=0, row=7, sticky=W,padx=5, pady=10,columnspan=3)



    add()


    label00 = Label(roo, text="ID", font=('arial', 10, "bold")).grid(column=0, row=8,sticky=W)
    label11 = Label(roo, text="Nazwa", font=('arial', 10, "bold")).grid(column=1, row=8,sticky=W)
    label22 = Label(roo, text="Choroba", font=('arial', 10, "bold")).grid(column=2, row=8,sticky=W)
    label44 = Label(roo, text="Pacjent", font=('arial', 10, "bold")).grid(column=4, row=8,sticky=W)
    label44 = Label(roo, text="Opiekun", font=('arial', 10, "bold")).grid(column=6, row=8, sticky=W)

    wr = 9
    ko = 0

    for dzial1, pacjent, opiekun, diagnoza in join_all:
        label00 = Label(roo, text=dzial1.dzialID, font=('arial', 10)).grid(column=ko, row=wr, sticky=W)
        label11 = Label(roo, text=dzial1.nazwa, font=('arial', 10)).grid(column=ko + 1, row=wr, sticky=W)
        label22 = Label(roo, text=diagnoza.choroba, font=('arial', 10)).grid(column=ko + 2, row=wr, sticky=W)
        label44 = Label(roo, text=pacjent.imie, font=('arial', 10)).grid(column=ko + 4, row=wr, sticky=W)
        label55 = Label(roo, text=pacjent.nazwisko, font=('arial', 10)).grid(column=ko + 5, row=wr, sticky=W)
        label66 = Label(roo, text=opiekun.imie, font=('arial', 10)).grid(column=ko + 6, row=wr, sticky=W)
        label77 = Label(roo, text=opiekun.nazwisko, font=('arial', 10)).grid(column=ko + 7, row=wr, sticky=W)
        wr = wr + 1

   
def diagnozy():

    def czyscdiagnoza():
        box1.delete(0, END)
        box2.delete(0, END)
        box3.delete(0, END)
        box4.delete(0, END)

    def dodajdiagnoza(choroba_n, objaw_n, poziom_zagrozenia_zycia_n, leczenie_n):
        n_diagnoza = diagnoza(choroba=choroba_n, objaw=objaw_n, poziom_zagrozenia_zycia=poziom_zagrozenia_zycia_n, leczenie=leczenie_n)
        wynik = sesja.add(n_diagnoza)
        sesja.commit()

        diagnozy()

    def szukajdiagnoza():

        def wypisz():
            # pasek wyszukiwania
            wczytaj = Entry(szu)
            wczytaj.grid(row=0, column=1, padx=10, pady=10)

            szukaj = Label(szu, text="Wyszukaj diagnozy")
            szukaj.grid(row=0, column=0, padx=10, pady=10)

            wybierz = ttk.Combobox(szu, values=['Wyszukaj po.. ', 'Chorobaie', 'Objawie', 'Poziom zagrozenia zycia', 'Leczeniu'])
            wybierz.current(0)
            wybierz.grid(row=0, column=2,columnspan=2)

            przycisk = Button(szu, text="Szukaj", command=lambda: szuk(wczytaj.get(), wybierz.get()))
            przycisk.grid(row=1, column=0)

        def edytuj(id):

            def czyscdiagnoza():
                box1.delete(0, END)
                box2.delete(0, END)
                box3.delete(0, END)
                box4.delete(0, END)

            def update(id, n_choroba, n_objaw, n_poziom_zagrozenia_zycia, n_leczenie):
                wynik_edycji = sesja.query(diagnoza).filter(diagnoza.diagnozaID == id).first()
                wynik_edycji.choroba = n_choroba
                wynik_edycji.objaw = n_objaw
                wynik_edycji.poziom_zagrozenia_zycia = n_poziom_zagrozenia_zycia
                wynik_edycji.leczenie = n_leczenie
                sesja.commit()

                edt.destroy()
                diagnozy()

            edt = Tk()
            edt.title("Edycja danych")
            edt.iconbitmap('c:/gui/icon.ico')
            edt.geometry("400x400")

            tytul = Label(edt, text="Edycja danych dla tabeli: Diagnoza", font=("Arial", 12, 'bold'))
            tytul.grid(row=0, column=1, columnspan=3, sticky=W)

            label1 = Label(edt, text="Choroba", font=("Arial", 12)).grid(column=1, row=2, sticky=W, padx=5, pady=10)
            label2 = Label(edt, text="Objaw", font=("Arial", 12)).grid(column=1, row=3, sticky=W, padx=5, pady=10)
            label3 = Label(edt, text="Poziom zagrozenia zycia", font=("Arial", 12)).grid(column=1, row=4, sticky=W, padx=5, pady=10)
            label4 = Label(edt, text="Leczenie", font=("Arial", 12)).grid(column=1, row=5, sticky=W, padx=5, pady=10)


            box1 = Entry(edt)
            box1.grid(column=2, row=2)
            box2 = Entry(edt)
            box2.grid(column=2, row=3)
            box3 = Entry(edt)
            box3.grid(column=2, row=4)
            box4 = Entry(edt)
            box4.grid(column=2, row=5)


            dod = Button(edt, text="Zatwierdz zmiany", padx=20, pady=10,command=lambda: update(id, box1.get(), box2.get(), box3.get(), box4.get()))
            dod.grid(column=1, row=6, sticky=W, padx=20, pady=20)
            czysc = Button(edt, text="Wyczysc", padx=20, pady=10, command=czyscdiagnoza)
            czysc.grid(column=2, row=6, sticky=W, padx=20, pady=20)

        def usundiagnoza(id):
            usun = sesja.query(diagnoza).filter(diagnoza.diagnozaID == id).first()
            sesja.delete(usun)
            sesja.commit()

            for widgets in szu.winfo_children():
                widgets.destroy()
            wypisz()
            diagnozy()

        def szuk(dan, wybor):

            for widgets in szu.winfo_children():
                widgets.destroy()

            wypisz()

            if wybor == 'Chorobaie':
                wynik_szukania = sesja.query(diagnoza).filter(diagnoza.choroba == dan)
            if wybor == 'Objawie':
                wynik_szukania = sesja.query(diagnoza).filter(diagnoza.objaw == dan)
            if wybor == 'Poziom zagrozenia zycia':
                wynik_szukania = sesja.query(diagnoza).filter(diagnoza.poziom_zagrozenia_zycia == dan)
            if wybor == 'Leczeniu':
                wynik_szukania = sesja.query(diagnoza).filter(diagnoza.leczenie == dan)


            label01 = Label(szu, text="ID", font=('arial', 10, "bold")).grid(column=2, row=2,sticky=W)
            label12 = Label(szu, text="Choroba", font=('arial', 10, "bold")).grid(column=3, row=2,sticky=W)
            label21 = Label(szu, text="Objaw", font=('arial', 10, "bold")).grid(column=4, row=2,sticky=W)
            label31 = Label(szu, text="Poziom zagrozenia zycia", font=('arial', 10, "bold")).grid(column=5, row=2,sticky=W)
            label41 = Label(szu, text="Leczenie", font=('arial', 10, "bold")).grid(column=6, row=2,sticky=W)

            wr = 3
            ko = 0
            for r in wynik_szukania:
                e_przycisk = Button(szu, text="Edytuj", command=lambda: edytuj(r.diagnozaID))
                u_przycisk = Button(szu, text='Usun', command=lambda: usundiagnoza(r.diagnozaID))
                e_przycisk.grid(row=wr, column=ko)
                u_przycisk.grid(row=wr, column=ko+1)
                label00 = Label(szu, text=r.diagnozaID, font=('arial', 10)).grid(column=ko+2, row=wr, sticky=W)
                label11 = Label(szu, text=r.choroba, font=('arial', 10)).grid(column=ko + 3, row=wr, sticky=W)
                label22 = Label(szu, text=r.objaw, font=('arial', 10)).grid(column=ko + 4, row=wr, sticky=W)
                label33 = Label(szu, text=r.poziom_zagrozenia_zycia, font=('arial', 10)).grid(column=ko + 5, row=wr, sticky=W)
                label33 = Label(szu, text=r.leczenie, font=('arial', 10)).grid(column=ko + 6, row=wr, sticky=W)
                wr = wr + 1



        szu = Tk()
        szu.title("Szukaj diagnoz")
        szu.iconbitmap('c:/gui/icon.ico')
        szu.geometry("900x800")
        wypisz()

    clear_frame()
    root.title("Diagnozy w szpitalu")
    cof = Button(roo, text="cofnij", padx=10, pady=5, command=ekran_poczatek)
    cof.grid(row=0, column=0,sticky=W)
    tytul = Label(roo, text="Dodaj do bazy diagnoze:", font=("Arial", 12,'bold'))
    tytul.grid(row=0, column=1,columnspan=3,sticky=W)

    label1 = Label(roo, text="Choroba",font=("Arial", 12)).grid(column=1,row=2,sticky=W,padx=5,pady=10)
    label2 = Label(roo, text="Objaw", font=("Arial", 12)).grid(column=1, row=3,sticky=W,padx=5,pady=10)
    label3 = Label(roo, text="Poziom zagrozenia zycia", font=("Arial", 12)).grid(column=1, row=4,sticky=W,padx=5,pady=10)
    label4 = Label(roo, text="Leczenie", font=("Arial", 12)).grid(column=1, row=5,sticky=W,padx=5,pady=10)

    box1 = Entry(roo)
    box1.grid(column=2, row=2)
    box2 = Entry(roo)
    box2.grid(column=2, row=3)
    box3 = Entry(roo)
    box3.grid(column=2, row=4)
    box4 = Entry(roo)
    box4.grid(column=2, row=5)

    dodajdiagnozy = Button(roo, text="Dodaj", padx=20, pady=10, command=lambda:dodajdiagnoza(box1.get(), box2.get(), box3.get(), box4.get()))
    dodajdiagnozy.grid(column=1, row=6, sticky=W, padx=20, pady=20)
    czys = Button(roo, text="Czysc", padx=20, pady=10, command=czyscdiagnoza)
    czys.grid(column=2, row=6, sticky=W, padx=20, pady=20)
    szukaj = Button(roo, text="Szukaj w bazie diagnozy", padx=20, pady=10, command=szukajdiagnoza)
    szukaj.grid(column=3, row=6, sticky=W, padx=20, pady=20,columnspan=3)


    podglad = Label(roo, text="Diagnozy w szpitalu", font=("Arial", 12, 'bold')).grid(column=0, row=7, sticky=W,padx=5, pady=10,columnspan=4)

    label00 = Label(roo, text="ID", font=('arial', 10, "bold")).grid(column=0, row=8,sticky=W)
    label11 = Label(roo, text="Choroba", font=('arial', 10, "bold")).grid(column=1, row=8,sticky=W)
    label22 = Label(roo, text="Objaw", font=('arial', 10, "bold")).grid(column=2, row=8,sticky=W)
    label33 = Label(roo, text="Poziom zagrozenia zycia", font=('arial', 10, "bold")).grid(column=3, row=8,sticky=W)
    label44 = Label(roo, text="Leczenie", font=('arial', 10, "bold")).grid(column=4, row=8,sticky=W)


    dowys = sesja.query(diagnoza)
    wr = 9
    ko = 0
    for r in dowys:
        label00 = Label(roo, text=r.diagnozaID, font=('arial', 10)).grid(column=ko, row=wr,sticky=W)
        label11 = Label(roo, text=r.choroba, font=('arial', 10)).grid(column=ko + 1, row=wr,sticky=W)
        label22 = Label(roo, text=r.objaw, font=('arial', 10)).grid(column=ko + 2, row=wr,sticky=W)
        label33 = Label(roo, text=r.poziom_zagrozenia_zycia, font=('arial', 10)).grid(column=ko + 3, row=wr,sticky=W)
        label44 = Label(roo, text=r.leczenie, font=('arial', 10)).grid(column=ko + 4, row=wr,sticky=W)
        wr = wr + 1


def clear_frame():
    for widgets in roo.winfo_children():
        widgets.destroy()


def ekran_poczatek():
 
    clear_frame()
    root.title("Szpital")
    start = Label(roo, text="Szpital - Baza", font=("Arial", 30))
    start.grid(column=2, row=0, ipadx=73,sticky=W)

    png = ImageTk.PhotoImage(Image.open('c:/gui/hospital.png'))
    png_label = Label(roo,image=png)
    png_label.image = png
    png_label.grid(column=2, row=1, ipadx=73, sticky=W)
    st = Label(roo, text="Wybierz tabelę", font=("Arial", 20))
    st.grid(column=2, row=3, ipadx=107,sticky=W)


    przycisk1 = Button(roo, text="Dzialy", padx=38, pady=20, command=dzialy)
    przycisk1.grid(column=0, pady=40, row=3,sticky=W)
    przycisk2 = Button(roo, text="Pacjenci", padx=32, pady=20, command=pacjenci)
    przycisk2.grid(column=1, row=3,sticky=W)
    przycisk3 = Button(roo, text="Opiekuni", padx=30, pady=20, command=opiekuni)
    przycisk3.grid(column=3, row=3,sticky=W)
    przycisk4 = Button(roo, text="Diagnozy", padx=29, pady=20, command=diagnozy)
    przycisk4.grid(column=4, row=3,sticky=W)
    #ipadx=113

ekran_poczatek()
root.mainloop()

