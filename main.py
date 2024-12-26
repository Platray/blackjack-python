from Partie import Blackjack

if __name__ == "__main__":
    nombre_joueurs = int(input("Combien de joueurs (1-6) ? "))
    nombre_paquets = int(input("Combien de paquets de cartes (1-8) ? "))
    jeu = Blackjack(nombre_joueurs=nombre_joueurs, nombre_paquets=nombre_paquets)
    jeu.jouer_partie()