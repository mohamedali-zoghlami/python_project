from menu import Menu

response = 15
while (response):
    print("1. Ajouter une nouvelle aide.")
    print("2. Afficher les aides")
    print("3. Ajouter une famille.")
    print("4. Afficher les famille.")
    print("5. Afficher l'aide qui a la plus grande quantite et celle qui a la quantite la plus petite.")
    print("6. Affecter une aide à une famille.")
    print("7. Controler le stock.")
    print("0. Quitter.")
    response = int(input())
    if response == 1:
        Menu.ajouteAide()
    elif response == 2:
        Menu.afficheAide()
    elif response == 3:
        Menu.ajouteFamille()
    elif response == 4:
        Menu.afficheFamille()
    elif response == 5:
        Menu.afficheMinMax()
    elif response == 6:
        Menu.affecteAide()
    elif response == 7:
        Menu.controleStock()
