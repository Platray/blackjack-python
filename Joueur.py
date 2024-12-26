class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.main = []

    def ajouter_carte(self, carte):
        self.main.append(carte)

    def afficher_main(self):
        return ", ".join(str(carte) for carte in self.main)

    def valeur_main(self):
        valeurs = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
                   'Valet': 10, 'Dame': 10, 'Roi': 10, 'As': 11}
        total = 0
        nb_as = 0
        for carte in self.main:
            total += valeurs[carte.valeur]
            if carte.valeur == 'As':
                nb_as += 1
        while total > 21 and nb_as > 0:  # Réduire la valeur des As si nécessaire
            total -= 10
            nb_as -= 1
        return total