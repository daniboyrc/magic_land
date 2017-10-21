#!/usr/bin/env python
# coding: utf-8
# (c) 2017 Daniel Coura, UFCG

from item import *


class ItemQuest(Item):
    def __init__(self, name, image_file):
        super(itemQuest, self).__init__(nome, local)

    def __str__(self):
        return 'item_quest'


if __name__ == "__main__":
    print("item_quest module")
