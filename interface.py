import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Pour gérer les images
from Partie import Blackjack


class BlackjackGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Blackjack")
        self.images = {}  # Dictionnaire pour stocker les images des cartes
        self.load_card_images()
        self.setup_game()
        self.joueur_courant = 0  # Ajout de l'attribut pour suivre le joueur courant


    def load_card_images(self):
        """Charge les images des cartes dans un dictionnaire."""
        couleurs = ['Coeurs', 'Carreaux', 'Piques', 'Trefles']  # Utilisation de noms sans accents pour les fichiers
        rangs = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        correspondances = {
            'Coeurs': 'Cœurs',
            'Carreaux': 'Carreaux',
            'Piques': 'Piques',
            'Trefles': 'Trèfles'
        }

        for couleur_sans_accent, couleur_avec_accent in correspondances.items():
            for rang in rangs:
                filename = f"images/{rang}_de_{couleur_sans_accent}.png"
                try:
                    image = Image.open(filename).resize((80, 120))
                    self.images[f"{rang}_de_{couleur_avec_accent}"] = ImageTk.PhotoImage(image)
                except FileNotFoundError:
                    print(f"Image introuvable : {filename}")
                except Exception as e:
                    print(f"Erreur lors du chargement de {filename} : {e}")

        # Ajouter une image pour le dos de la carte
        try:
            back_image = Image.open("images/back.png").resize((80, 120))
            self.images["back"] = ImageTk.PhotoImage(back_image)
        except FileNotFoundError:
            print("Image introuvable : images/back.png")
        except Exception as e:
            print(f"Erreur lors du chargement de l'image du dos : {e}")

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
        """Initialiser le jeu avec les paramètres donnés."""
        nombre_joueurs = self.nombre_joueurs.get()
        nombre_paquets = self.nombre_paquets.get()
        fonds_initiaux = self.fonds_initiaux.get()

        self.jeu = Blackjack(nombre_joueurs, fonds_initiaux, nombre_paquets)
        self.current_player_index = 0  # Indice du joueur courant
        self.setup_frame.pack_forget()
        self.create_game_frame()

    def create_game_frame(self):
        """Créer l'interface de jeu principale."""
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack()

        # Affichage des joueurs
        self.player_frames = []
        for joueur in self.jeu.joueurs:
            frame = tk.Frame(self.game_frame)
            frame.pack(side=tk.TOP, pady=10)
            label = tk.Label(frame, text=f"{joueur.nom} : {joueur.fonds}€")
            label.pack()
            joueur.label = label  # Stocker le label dans l'objet joueur
            joueur.cards_frame = tk.Frame(frame)
            joueur.cards_frame.pack()
            self.player_frames.append(frame)

        # Affichage du croupier
        self.croupier_frame = tk.Frame(self.game_frame)
        self.croupier_frame.pack(pady=20)
        self.croupier_label = tk.Label(self.croupier_frame, text="Croupier")
        self.croupier_label.pack()
        self.croupier_cards_frame = tk.Frame(self.croupier_frame)
        self.croupier_cards_frame.pack()

        # Boutons d'action
        self.action_frame = tk.Frame(self.root)
        self.action_frame.pack(pady=20)

        self.tirer_btn = tk.Button(self.action_frame, text="Tirer une carte", command=self.tirer_carte)
        self.tirer_btn.pack(side=tk.LEFT, padx=10)

        self.passer_btn = tk.Button(self.action_frame, text="Passer", command=self.passer_tour)
        self.passer_btn.pack(side=tk.LEFT, padx=10)

        self.stop_btn = tk.Button(self.action_frame, text="Arrêter le jeu", command=self.stop_game)
        self.stop_btn.pack(side=tk.LEFT, padx=10)

        self.play_round()

    def play_round(self):
        """Commencer une nouvelle manche."""
        self.jeu.vider_mains()
        self.jeu.distribuer_cartes()
        self.update_display()

    def tirer_carte(self):
        """Tirer une carte pour le joueur courant."""
        joueur_courant = self.jeu.joueurs[self.current_player_index]
        joueur_courant.recevoir_carte(self.jeu.paquet.tirer_carte())
        self.update_display()

        # Vérifier si le joueur a dépassé 21
        if joueur_courant.a_depasse_21():
            messagebox.showinfo("Tour terminé", f"{joueur_courant.nom} a dépassé 21.")
            self.passer_tour()


    def passer_tour(self):
        """Passer le tour du joueur courant."""
        joueur_courant = self.jeu.joueurs[self.current_player_index]

        # Si le joueur a dépassé 21, on passe immédiatement au joueur suivant ou au croupier
        if joueur_courant.valeur_main() > 21:
            messagebox.showinfo("Tour terminé", f"{joueur_courant.nom} a dépassé 21.")
            self.current_player_index += 1  # Passer au joueur suivant

        # Si c'est le dernier joueur, on passe au croupier
        elif self.current_player_index == len(self.jeu.joueurs) - 1:
            self.tour_du_croupier()
        else:
            self.current_player_index += 1  # Passer au joueur suivant

        self.update_display()


    def tour_du_croupier(self):
        """Lance le tour du croupier après que les joueurs ont terminé."""
        self.jeu.tour_croupier()  # Appelle la méthode tour_croupier du jeu
        self.update_display()  # Mets à jour l'affichage après le tour du croupier
        self.regler_paris()  # Gère les paris après le tour du croupier
        self.fin_de_partie()  # Vérifie si la partie est terminée

        
    def a_depasse_21(self):
        """Retourne True si le joueur a dépassé 21."""
        return self.calculer_score() > 21
        
    def terminer_manche(self):
        """Afficher les résultats de la manche et relancer une nouvelle."""
        resultats = self.jeu.determiner_resultats()
        message = "\n".join(resultats)
        messagebox.showinfo("Résultats de la manche", message)

        # Redémarrer une nouvelle manche
        if messagebox.askyesno("Nouvelle manche", "Voulez-vous jouer une nouvelle manche ?"):
            self.current_player_index = 0
            self.play_round()
        else:
            self.stop_game()



    def stop_game(self):
        """Arrêter le jeu."""
        self.root.destroy()

    def update_display(self):
        """Met à jour l'affichage des cartes et des fonds."""
        # Mise à jour des cartes des joueurs
        for joueur in self.jeu.joueurs:
            for widget in joueur.cards_frame.winfo_children():
                widget.destroy()
            for carte in joueur.main:
                image = self.images[str(carte)]
                label = tk.Label(joueur.cards_frame, image=image)
                label.pack(side=tk.LEFT)

        # Mise à jour des cartes du croupier
        for widget in self.croupier_cards_frame.winfo_children():
            widget.destroy()
        for carte in self.jeu.croupier.main:
            image = self.images[str(carte)]
            label = tk.Label(self.croupier_cards_frame, image=image)
            label.pack(side=tk.LEFT)


    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = BlackjackGUI()
    app.run()
