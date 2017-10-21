from item import *


class Sword(Item):
    def __init__(self, name, image_file, damage):
        super(Sword, self).__init__(name, image_file)
        self.damage = damage

    def __str__(self):
        return 'sword'


class Armor(Item):
    def __init__(self, name, image_file, defense):
        super(Armor, self).__init__(name, image_file)
        self.defense = defense

    def __str__(self):
        return 'armor'


class Gauntlet(Item):
    def __init__(self, name, image_file, mana, damage):
        super(Gauntlet, self).__init__(name, image_file)
        self.mana = mana
        self.damage = damage

    def __str__(self):
        return 'gauntlet'

    def spriteSheet(self):
        pass
