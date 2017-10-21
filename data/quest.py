#!/usr/bin/env python
# coding: utf-8
# (c) 2017 Daniel Coura, UFCG


class Quest():
    def __init__(self, name, description, steps, give_item, receive_item, avaible, next_quest=None):
        self.name = name
        self.description = description
        self.steps = steps
        self.current_step = 0
        self.avaible = avaible
        self.give_item = give_item
        self.receive_item = receive_item
        self.dialogue = []
        self.next_quest = next_quest

    def set_step(self, player):
        if self.current_step == 0:
            player.newQuest(self)

        self.item(player)
        self.current_step += 1

        if self.current_step == len(self.steps):
            self.avaible = False
            if self.next_quest:
                for i in self.next_quest:
                    self.i.avaible = True
            player.removeQuest(self)

    def item(self, player):
        if self.give_item[self.current_step] is not None:
            for i in self.give_item[self.current_step]:
                player.newItem(i)

        if self.receive_item[self.current_step] is not None:
            for i in self.receive_item[self.current_step]:
                player.removeItem(i)


if __name__ == "__main__":
    print("quest module")
