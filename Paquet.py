import random
from Carte import Carte

class Paquet:
    def __init__(self, nombre_paquets=1):
        self.cartes = []
        couleurs = ['Cœurs', 'Carreaux', 'Piques', 'Trèfles']
        rangs = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        for _ in range(nombre_paquets):
            for couleur in couleurs:
                for rang in rangs:
                    self.cartes.append(Carte(rang, couleur))
        random.shuffle(self.cartes)

    def tirer_carte(self):
        return self.cartes.pop()