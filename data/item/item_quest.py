from item import *


class itemQuest(Item):
    def __init__(self, nome, local):
        super(itemQuest, self).__init__(nome, local)

    def __str__(self):
        return 'item_quest'
