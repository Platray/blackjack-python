class Partie:
    def __init__(self):
        self.paquet = Paquet()
        self.joueurs = [Joueur("Joueur"), Joueur("Banque")]

    def distribuer_cartes_initiales(self):
        for _ in range(2):
            for joueur in self.joueurs:
                joueur.ajouter_carte(self.paquet.piocher())

    def afficher_etats(self):
        for joueur in self.joueurs:
            print(f"{joueur.nom} a : {joueur.afficher_main()} (valeur : {joueur.valeur_main()})")

    def tour_joueur(self, joueur):
        while joueur.valeur_main() < 21:
            action = input(f"{joueur.nom}, voulez-vous piocher une carte ? (o/n) : ").lower()
            if action == 'o':
                joueur.ajouter_carte(self.paquet.piocher())
                print(f"{joueur.nom} a maintenant : {joueur.afficher_main()} (valeur : {joueur.valeur_main()})")
            else:
                break

    def tour_banque(self, joueur):
        while joueur.valeur_main() < 17:
            joueur.ajouter_carte(self.paquet.piocher())
            print(f"La banque pioche une carte : {joueur.afficher_main()} (valeur : {joueur.valeur_main()})")

    def determiner_gagnant(self):
        joueur, banque = self.joueurs
        score_joueur = joueur.valeur_main()
        score_banque = banque.valeur_main()

        if score_joueur > 21:
            return "La banque gagne (le joueur a dépassé 21) !"
        if score_banque > 21:
            return "Le joueur gagne (la banque a dépassé 21) !"
        if score_joueur > score_banque:
            return "Le joueur gagne !"
        elif score_joueur < score_banque:
            return "La banque gagne !"
        else:
            return "Égalité !"

    def jouer(self):
        print("Bienvenue au Blackjack !")
        self.distribuer_cartes_initiales()
        self.afficher_etats()

        # Tour du joueur
        print("\n--- Tour du Joueur ---")
        self.tour_joueur(self.joueurs[0])

        # Tour de la banque
        print("\n--- Tour de la Banque ---")
        self.tour_banque(self.joueurs[1])

        # Résultat
        print("\n--- Résultat ---")
        self.afficher_etats()
        print(self.determiner_gagnant())