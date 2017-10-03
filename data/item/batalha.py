from item import *


class Espada(Item):
    def __init__(self, nome, local, dano):
        super(Espada, self).__init__(nome, local)
        self.dano = dano

    def __str__(self):
        return 'espada'


class Armadura(Item):
    def __init__(self, nome, local, defesa):
        super(Armadura, self).__init__(nome, local)
        self.defesa = defesa

    def __str__(self):
        return 'armadura'


class Manopla(Item):
    def __init__(self, nome, local, mana, dano):
        super(Manopla, self).__init__(nome, local)
        self.mana = mana
        self.dano = dano

    def __str__(self):
        return 'manopla'

    def spriteSheet(self):
        pass
