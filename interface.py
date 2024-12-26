import tkinter as tk
from Partie import Blackjack

class BlackjackGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Blackjack")
        self.setup_game()

    def setup_game(self):
        self.nombre_joueurs = tk.IntVar(value=1)
        self.nombre_paquets = tk.IntVar(value=6)
        self.fonds_initiaux = tk.IntVar(value=1000)

        # Interface d’accueil pour configurer le jeu
        self.setup_frame = tk.Frame(self.root)
        self.setup_frame.pack()

        tk.Label(self.setup_frame, text="Nombre de joueurs (1-6)").pack()
        tk.Entry(self.setup_frame, textvariable=self.nombre_joueurs).pack()

        tk.Label(self.setup_frame, text="Nombre de paquets (1-8)").pack()
        tk.Entry(self.setup_frame, textvariable=self.nombre_paquets).pack()

        tk.Label(self.setup_frame, text="Fonds initiaux par joueur (€)").pack()
        tk.Entry(self.setup_frame, textvariable=self.fonds_initiaux).pack()

        tk.Button(self.setup_frame, text="Démarrer le jeu", command=self.start_game).pack()

    def start_game(self):
        # Initialiser le jeu avec les paramètres
        nombre_joueurs = self.nombre_joueurs.get()
        nombre_paquets = self.nombre_paquets.get()
        fonds_initiaux = self.fonds_initiaux.get()

        self.jeu = Blackjack(nombre_joueurs, fonds_initiaux, nombre_paquets)
        self.setup_frame.pack_forget()
        self.create_game_frame()

    def create_game_frame(self):
        # Interface principale pour jouer
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack()

        self.joueur_labels = []
        self.croupier_label = tk.Label(self.game_frame, text="Croupier")
        self.croupier_label.pack()

        for joueur in self.jeu.joueurs:
            joueur_label = tk.Label(self.game_frame, text=f"{joueur.nom} : {joueur.fonds}€")
            joueur_label.pack()
            self.joueur_labels.append(joueur_label)

        tk.Button(self.game_frame, text="Jouer une manche", command=self.play_round).pack()

    def play_round(self):
        # Lancer une nouvelle manche
        self.jeu.vider_mains()
        self.jeu.distribuer_cartes()

        # Commencer avec le premier joueur
        self.show_player_turn(self.jeu.joueurs[0])

    def show_player_turn(self, joueur):
        """Afficher les options pour le tour d'un joueur."""
        self.current_player = joueur
        self.action_frame = tk.Frame(self.game_frame)
        self.action_frame.pack()

        self.status_label = tk.Label(
            self.action_frame, text=f"{joueur.nom}, à votre tour ! (Valeur: {joueur.valeur_main()})"
        )
        self.status_label.pack()

        self.tirer_btn = tk.Button(self.action_frame, text="Tirer une carte", command=self.tirer_carte)
        self.tirer_btn.pack()

        self.passer_btn = tk.Button(self.action_frame, text="Passer", command=self.passer_tour)
        self.passer_btn.pack()

    def tirer_carte(self):
        """Action : tirer une carte pour le joueur courant."""
        self.current_player.recevoir_carte(self.jeu.paquet.tirer_carte())
        self.status_label.config(
            text=f"{self.current_player.nom}, valeur actuelle: {self.current_player.valeur_main()}"
        )

        if self.current_player.valeur_main() >= 21:
            self.fin_tour()

    def passer_tour(self):
        """Action : passer le tour."""
        self.fin_tour()

    def fin_tour(self):
        """Terminer le tour actuel."""
        self.action_frame.destroy()  # Supprimer les boutons d'action
        if self.jeu.joueurs.index(self.current_player) < len(self.jeu.joueurs) - 1:
            # Passer au prochain joueur
            prochain_joueur = self.jeu.joueurs[self.jeu.joueurs.index(self.current_player) + 1]
            self.show_player_turn(prochain_joueur)
        else:
            # Tous les joueurs ont joué, c'est au tour du croupier
            self.tour_croupier()

    def tour_croupier(self):
        """Gérer le tour du croupier."""
        self.jeu.tour_croupier()
        self.jeu.regler_paris()
        self.update_labels()

    def update_labels(self):
        # Met à jour les fonds et cartes affichés
        for i, joueur in enumerate(self.jeu.joueurs):
            self.joueur_labels[i].config(
                text=f"{joueur.nom} : {joueur.fonds}€ - {joueur.afficher_main()}"
            )
        self.croupier_label.config(text=f"Croupier : {self.jeu.croupier.afficher_main()}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = BlackjackGUI()
    app.run()
