#!/usr/bin/env python
# coding: utf-8
# (c) 2017 Daniel Coura, UFCG


class Interaction():
    def npc(current_npc, scenario_coord, player_rect):
        for npc in current_npc:
            for collide in npc.interaction_area:
                collide = collide.move(scenario_coord[0], scenario_coord[1])
                if player_rect.colliderect(collide):
                    return npc

    def door(current_door, scenario_coord, player_rect):
        for door in current_door:
            collide = door.interaction_area.move(scenario_coord[0],
                                                 scenario_coord[1])
            if player_rect.colliderect(collide):
                if door.door_open:
                    return door


if __name__ == "__main__":
    print("interaction module")
