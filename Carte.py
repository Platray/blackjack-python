class Carte:
    def __init__(self, rang, couleur):
        """
        Initialise une carte avec un rang et une couleur.
        
        :param rang: Le rang de la carte ('2', '3', ..., 'A', 'J', 'Q', 'K')
        :param couleur: La couleur de la carte ('Coeurs', 'Carreaux', 'Piques', 'Trèfles')
        """
        self.rang = rang
        self.couleur = couleur

    def valeur(self):
        """
        Retourne la valeur de la carte selon les règles du Blackjack.
        
        Les cartes 'J', 'Q', 'K' valent 10, l'As vaut 11 (ou 1 selon le total de la main),
        les autres cartes valent leur valeur numérique.
        """
        if self.rang in ['J', 'Q', 'K']:
            return 10
        elif self.rang == 'A':
            return 11  # L'As sera traité plus tard dans la classe 'Joueur' pour s'ajuster
        return int(self.rang)

    def __str__(self):
        """Retourne une chaîne représentant la carte sous la forme 'Rang_de_Couleur'."""
        return f"{self.rang}_de_{self.couleur}"
