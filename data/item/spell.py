#!/usr/bin/env python
# coding: utf-8
# (c) 2017 Daniel Coura, UFCG

from item import *


class Spell(Item):
    def __init__(self, name, image_file, id_spell, description, level,
                 step, type_spell, status, ex_solution):
        super(Feitico, self).__init__(name, image_file)
        self.id = id_spell
        self.description = description
        self.level = level
        self.step = step
        self.type = type_spell
        self.status = status
        self.ex_solution = ex_solution

        self.solution = ''

    def __str__(self):
        return 'spell'

if __name__ == "__main__":
    print("spell module")
