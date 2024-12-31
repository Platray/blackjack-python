from Paquet import Paquet
from Joueur import Joueur

class Blackjack:
    def __init__(self, nombre_joueurs, fonds_initiaux=1000, nombre_paquets=6):
        if not (1 <= nombre_joueurs <= 6):
            raise ValueError("Le nombre de joueurs doit être entre 1 et 6.")
        self.paquet = Paquet(nombre_paquets)
        self.joueurs = [Joueur(f"Joueur {i+1}", fonds_initiaux) for i in range(nombre_joueurs)]
        self.croupier = Joueur("Croupier", float('inf'))  # Le croupier n'a pas de fonds limités

    def distribuer_cartes(self):
        for _ in range(2):  # Deux cartes à chaque joueur et au croupier
            for joueur in self.joueurs:
                joueur.recevoir_carte(self.paquet.tirer_carte())
            self.croupier.recevoir_carte(self.paquet.tirer_carte())

    def tour_joueur(self, joueur):
        while joueur.valeur_main() < 21:
            print(joueur.afficher_main())
            action = input(f"{joueur.nom}, voulez-vous tirer une carte (T) ou passer (P) ? ").strip().upper()
            if action == 'T':
                joueur.recevoir_carte(self.paquet.tirer_carte())
            elif action == 'P':
                break
            else:
                print("Action non reconnue !")
        print(joueur.afficher_main())

    def tour_croupier(self):
        """Logique du tour du croupier."""
        print(self.croupier.afficher_main())
        while self.croupier.valeur_main() < 17:
            print("Le croupier tire une carte...")
            self.croupier.recevoir_carte(self.paquet.tirer_carte())
        print(self.croupier.afficher_main())



    def regler_paris(self):
        """Régler les paris des joueurs après le tour du croupier."""
        croupier_valeur = self.jeu.croupier.valeur_main()
        for joueur in self.jeu.joueurs:
            if joueur.valeur_main() > 21:
                print(f"{joueur.nom} a dépassé 21. Pari perdu !")
            elif croupier_valeur > 21 or joueur.valeur_main() > croupier_valeur:
                gains = joueur.pari * 2
                joueur.fonds += gains
                print(f"{joueur.nom} gagne {gains}€ !")
            elif joueur.valeur_main() == croupier_valeur:
                joueur.fonds += joueur.pari
                print(f"{joueur.nom} récupère sa mise.")
            else:
                print(f"{joueur.nom} perd sa mise.")
            joueur.pari = 0  # Réinitialiser le pari

    def fin_de_partie(self):
        """Vérifie si la partie est terminée."""
        if not any(joueur.fonds > 0 for joueur in self.jeu.joueurs):
            print("Tous les joueurs sont à court de fonds. Fin du jeu !")
            self.stop_game()


    def vider_mains(self):
        for joueur in self.joueurs:
            joueur.vider_main()
        self.croupier.vider_main()

    def jouer_partie(self):
        while True:
            print("\n--- Nouvelle partie ---\n")
            for joueur in self.joueurs:
                print(f"{joueur.nom} : {joueur.fonds}€ disponibles.")
                montant = int(input(f"{joueur.nom}, combien voulez-vous miser ? "))
                joueur.miser(montant)

            self.distribuer_cartes()
            for joueur in self.joueurs:
                self.tour_joueur(joueur)

            self.tour_croupier()
            self.regler_paris()
            self.vider_mains()

            if not any(joueur.fonds > 0 for joueur in self.joueurs):
                print("Tous les joueurs sont à court de fonds. Fin du jeu !")
                break

            continuer = input("Voulez-vous continuer la partie (O/N) ? ").strip().upper()
            if continuer != 'O':
                print("Merci d'avoir joué !")
                break