class Paquet:
    valeurs = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Valet', 'Dame', 'Roi', 'As']
    couleurs = ['Cœur', 'Carreau', 'Trèfle', 'Pique']

    def __init__(self):
        self.cartes = [Carte(valeur, couleur) for valeur in self.valeurs for couleur in self.couleurs]
        random.shuffle(self.cartes)

    def piocher(self):
        return self.cartes.pop() if self.cartes else None
