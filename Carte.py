class Carte:
    def __init__(self, rang, couleur):
        self.rang = rang
        self.couleur = couleur

    def valeur(self):
        if self.rang in ['J', 'Q', 'K']:
            return 10
        elif self.rang == 'A':
            return 11  # Géré comme 1 ou 11 selon les règles du Blackjack
        return int(self.rang)

    def __str__(self):
        return f"{self.rang} de {self.couleur}"