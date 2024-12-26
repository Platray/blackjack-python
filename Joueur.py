class Joueur:
    def __init__(self, nom, fonds):
        self.nom = nom
        self.fonds = fonds
        self.main = []
        self.pari = 0

    def miser(self, montant):
        if montant > self.fonds:
            raise ValueError(f"{self.nom} n'a pas assez de fonds pour miser {montant}€.")
        self.fonds -= montant
        self.pari = montant

    def recevoir_carte(self, carte):
        self.main.append(carte)

    def valeur_main(self):
        total = sum(carte.valeur() for carte in self.main)
        as_count = sum(1 for carte in self.main if carte.rang == 'A')
        while total > 21 and as_count:
            total -= 10
            as_count -= 1
        return total

    def afficher_main(self):
        cartes = ', '.join(str(carte) for carte in self.main)
        return f"{self.nom} : {cartes} (Valeur: {self.valeur_main()})"

    def vider_main(self):
        self.main = []