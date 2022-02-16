import os
import profiles
from abc import ABC
from datetime import datetime

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

        print('Willkommen zur Buchhaltungssoftware!')
        print()
        print('Was möchtest Du tun?')
        print('--------------------')
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

        print('Profil erstellen')
        print('---------------------')
        print()
        profil_name = input('Profilname: ')
        start_guthaben = input('Startguthaben: ')
        print()

        profiles.ProfilManager.erstelle_profil(profil_name, start_guthaben)

        print(f'Profil {profil_name}.json wurde angelegt!')
        input('mit ENTER bestätigen und weiter zu "Profil laden"')

        menu = LadeProfilMenu()
        menu.menuAnzeigen()

class LadeProfilMenu(Menu):
    def menuAnzeigen(self):
        super().menuAnzeigen()

        print('Vorhandene Profile:')
        print('---------------------')

        dir_path = f".\Profile\\"
        result = next(os.walk(dir_path))[2]
        for item in result:
            print(item)

        print('---------------------')
        print()
        print('Wähle dein Profil (mit ENTER zurück zum Startmenu):')
        name = input()

        if name is '':
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

        print(f'Aktuelles Profil: {self.profil.name}')
        print(f'Aktueller Kontostand: {self.profil.guthaben} EURO')
        print()
        print('Was möchtest Du tun?')
        print('---------------------')
        print('[1] Neue Transaktion')
        print('[2] Zeige Transaktionen')
        print('[3] zurück zum Startmenu')
        print()

        eingabe = input('Eingabe: ')

        if eingabe == '1':
            menu = NeueTransaktionMenu(self.profil)
            menu.menuAnzeigen()

        elif eingabe == '2':
            # menu = TransaktionAnzeigenMenu()
            # menu.menuAnzeigen()
            pass

        elif eingabe == '3':
            menu = StartMenu()
            menu.menuAnzeigen()

        else:
            print()
            print('Ungültige Eingabe!')
            print()
            input('mit ENTER bestätigen und nochmal versuchen')

            menu = AktuellesProfilMenu(self.profil)
            menu.menuAnzeigen()

class NeueTransaktionMenu(Menu):
    def __init__(self, profil):
        super().__init__()
        self.profil = profil

    def menuAnzeigen(self):
        super().menuAnzeigen()

        print('Neue Transaktion')
        print('---------------------')
        print()
        transaktion_name = input('Name der Transaktion: ')

        transaktion_betrag = input('Betrag: ')
        transaktion_betrag = int(transaktion_betrag)

        transaktion_datum = input('Datum der Transaktion [yyyy-mm-dd]: ')
        transaktion_datum = datetime.strptime(transaktion_datum, '%Y-%m-%d')
        print()

        transaktion = profiles.Transaktion(transaktion_name, transaktion_betrag, transaktion_datum)
        self.profil.transaktionen.append(transaktion)
        self.profil.guthaben = int(self.profil.guthaben) + transaktion_betrag

        profiles.ProfilManager.update_profil(self.profil)

        print(transaktion)
        print(f'Aktuelles Guthaben: {self.profil.guthaben}')




