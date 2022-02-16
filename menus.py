import os
import locale
import keyboard
from unicodedata import decimal
import profiles
from abc import ABC
from datetime import datetime

# Währung Setzen
locale.setlocale(locale.LC_ALL, 'de_DE')

#Constanten
UEBERSCHIRFT = 'Willkommen zur Buchhaltungssoftware!'
TRENNER = '-'

# Konsole leeren
def clear():
    os.system('cls')

# abstrakte Klasse für die einzelnen Menues
class Menu(ABC):
    def menuAnzeigen(self):
        clear()

# nachfolgend die einzelnen Menues
class StartMenu(Menu):
    def menuAnzeigen(self):
        super().menuAnzeigen()

        UeberschriftAufrufen('Was möchtest Du tun?', None, True)
        print('[1] Profil erstellen')
        print('[2] Profil laden')
        print('[3] Beenden')
        print()

        eingabe = input('Eingabe: ')

        if eingabe == '1':
            menu = NeuesProfilMenu()
            menu.menuAnzeigen()

        elif eingabe == '2':
            menu = LadeProfilMenu()
            menu.menuAnzeigen()

        elif eingabe == '3':
            exit()

        else:
            print()
            print('Ungültige Eingabe!')
            print()
            input('mit ENTER bestätigen und nochmal versuchen')

            menu = StartMenu()
            menu.menuAnzeigen()

class NeuesProfilMenu(Menu):
    def menuAnzeigen(self):
        super().menuAnzeigen()

        UeberschriftAufrufen('Profil erstellen', None, True)
        #print('Profil erstellen')
        #print('---------------------')
        #print()
        profil_name = input('Profilname: ')
        start_guthaben = input('Startguthaben: ')
        print()

        profiles.ProfilManager.erstelle_profil(profil_name, start_guthaben)

        print(f'Profil {profil_name}.json wurde angelegt!')
        print('mit ENTER bestätigen und weiter zu "Profil laden"')
        keyboard.wait("enter")

        menu = LadeProfilMenu()
        menu.menuAnzeigen()

class LadeProfilMenu(Menu):
    def menuAnzeigen(self):
        super().menuAnzeigen()

        UeberschriftAufrufen('Vorhandene Profile:', None, True)
        #print('Vorhandene Profile:')
        #print('---------------------')

        dir_path = f".\Profile\\"
        result = next(os.walk(dir_path))[2]
        for item in result:
            benutzer=item.split('.')[0]
            print(benutzer)

        print(TRENNER*22)
        print()
        print('Wähle dein Profil (mit Enter zurück zum Startmenu):')
        name = input()
        if name == '':
                menu = StartMenu()
                menu.menuAnzeigen()

        else:
            profil = profiles.ProfilManager.lade_profil(name)

            menu = AktuellesProfilMenu(profil)
            menu.menuAnzeigen()

class AktuellesProfilMenu(Menu):
    def __init__(self, profil):
        super().__init__()
        self.profil = profil

    def menuAnzeigen(self):
        super().menuAnzeigen()

        UeberschriftAufrufen('Was möchtest Du tun?', self, False)
        #print(f'Aktuelles Profil: {self.profil.name}')
        #print(f'Aktueller Kontostand: {self.profil.guthaben} EURO')
        #print()
        #print('Was möchtest Du tun?')
        #print('---------------------')
        print('[1] Neue Transaktion')
        print('[2] Zeige Transaktionen')
        print('[3] zurück zum Startmenu')
        print()

        eingabe = input('Eingabe: ')

        Switch_Auswahl(eingabe, self)
#        if eingabe == '1':
#            menu = NeueTransaktionMenu(self.profil)
#            menu.menuAnzeigen()
#
#        elif eingabe == '2':
#            menu = TransaktionAnzeigenMenu(self.profil)
#            menu.menuAnzeigen()
#            pass
#
#        elif eingabe == '3':
#            menu = StartMenu()
#            menu.menuAnzeigen()
#
#        else:
#            print()
#            print('Ungültige Eingabe!')
#            print()
#            print('mit ESC bestätigen und nochmal versuchen')
#            keyboard.wait("esc")
#            clear()
#            menu = AktuellesProfilMenu(self.profil)
#            menu.menuAnzeigen()

class NeueTransaktionMenu(Menu):
    def __init__(self, profil):
        super().__init__()
        self.profil = profil

    def menuAnzeigen(self):
        super().menuAnzeigen()
        while (True):
            UeberschriftAufrufen('Neue Transaktion', None, True)
            transaktion_name = input('Name der Transaktion: ')
            transaktion_betrag = input('Betrag [**.**]: ')
            transaktion_betrag = float(transaktion_betrag)

            transaktion_datum = input('Datum der Transaktion [yyyy-mm-dd]: ')
            transaktion_datum = datetime.strptime(transaktion_datum, '%Y-%m-%d')
            print()

            transaktion = profiles.Transaktion(transaktion_name, transaktion_betrag, transaktion_datum)
            self.profil.transaktionen.append(transaktion)
            self.profil.guthaben = float(self.profil.guthaben) + transaktion_betrag

            profiles.ProfilManager.update_profil(self.profil)

            print(transaktion)
            neues_guthaben=locale.currency(float(self.profil.guthaben), grouping=True)
            print(f'Aktuelles Guthaben: {neues_guthaben}')
            print('\nmit \'J\' neue Buchung\toder\nmit \'N\' zurück zum Menü')
            auswahl = input('Auswahl: ')
            if (auswahl == 'N' or auswahl == 'n'):
                break
            elif (auswahl == 'J' or auswahl == 'j'):
                continue
            else:
                print('Falsche eingabe, zurück ins Menü\nWeiter mit ESC-Taste')
                keyboard.wait("esc")
                break
        clear()
        menu = AktuellesProfilMenu(self.profil)
        menu.menuAnzeigen()

class TransaktionAnzeigenMenu(Menu):
    def __init__(self, profil):
        super().__init__()
        self.profil = profil

    def menuAnzeigen(self):
        super().menuAnzeigen()

        UeberschriftAufrufen('Transaktions Übersicht', self, False)
        for transaktion in self.profil.transaktionen:
            print(transaktion)
        print(TRENNER*22)
        print('Weiter mit ESC-Taste')
        keyboard.wait("esc")
        clear()
        menu = AktuellesProfilMenu(self.profil)
        menu.menuAnzeigen()

def Switch_Auswahl(no, self):
    if (no=='1'):
            menu = NeueTransaktionMenu(self.profil)
            menu.menuAnzeigen()
    elif (no=='2'):
        menu = TransaktionAnzeigenMenu(self.profil)
        menu.menuAnzeigen()
        #pass
    elif (no=='3'):
        menu = StartMenu()
        menu.menuAnzeigen()

    else:
        print()
        print('Ungültige Eingabe!')
        print()
        print('mit ESC bestätigen und nochmal versuchen')
        keyboard.wait("esc")
        clear()
        menu = AktuellesProfilMenu(self.profil)
        menu.menuAnzeigen()


def UeberschriftAufrufen(zwischentext, classe, erweiterung=True,):

        if (erweiterung == True):
            print(UEBERSCHIRFT)
            print()
            print(zwischentext)
            print(TRENNER*22)
        else:
            guthabentoConvert = classe.profil.guthaben
            guthabenLocal = locale.currency(float(guthabentoConvert), grouping=True)
            print(UEBERSCHIRFT)
            print()
            print(f'Aktuelles Profil: {classe.profil.name}')
            print(f'Aktueller Kontostand: {guthabenLocal}')
            print()
            print(zwischentext)
            print(TRENNER*22)

