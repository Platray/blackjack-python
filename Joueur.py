class Joueur:
    def __init__(self, nom, fonds):
        self.nom = nom
        self.fonds = fonds
        self.main = []
        self.pari = 0

    def miser(self, montant):
        """Permet au joueur de miser une somme sur la manche."""
        if montant > self.fonds:
            raise ValueError(f"{self.nom} n'a pas assez de fonds pour miser {montant}€.")
        self.fonds -= montant
        self.pari = montant

    def recevoir_carte(self, carte):
        """Ajoute une carte à la main du joueur."""
        self.main.append(carte)

    def valeur_main(self):
        """
        Calcule la valeur totale des cartes dans la main du joueur.
        Gère les As comme valant 11 ou 1 selon la situation.
        """
        total = sum(carte.valeur() for carte in self.main)
        as_count = sum(1 for carte in self.main if carte.rang == 'A')
        while total > 21 and as_count:
            total -= 10
            as_count -= 1
        return total

    def a_depasse_21(self):
        """Retourne True si la valeur totale de la main dépasse 21."""
        return self.valeur_main() > 21

    def afficher_main(self):
        """Affiche les cartes dans la main du joueur, ainsi que leur valeur totale."""
        cartes = ', '.join(str(carte) for carte in self.main)
        return f"{self.nom} : {cartes} (Valeur: {self.valeur_main()})"

    def vider_main(self):
        """Vide la main du joueur."""
        self.main = []
