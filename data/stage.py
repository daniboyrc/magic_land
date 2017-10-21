#!/usr/bin/env python
# coding: utf-8
# (c) 2017 Daniel Coura, UFCG


class Stage():
    def __init__(self, player, scenario, npc, current_npc,
                 door, current_door, quests):

        self.player = player
        self.scenario = scenario
        self.npc = npc
        self.current_npc = current_npc
        self.door = door
        self.current_door = current_door
        self.quests = quests

    def set_stage(self, door):
        self.scenario.refresh(door.scenario['img'], door.scenario['pos'])
        self.current_npc = door.scenario['npc_list']
        self.current_door = door.scenario['door_list']
        self.player.coordinate = door.player


if __name__ == "__main__":
    print("stage module")
