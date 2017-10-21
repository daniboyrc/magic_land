#!/usr/bin/env python
# coding: utf-8
# (c) 2017 Daniel Coura, UFCG

import os

PATH = os.join(os.getcwd(), 'resources', 'item')


class Item(object):
    def __init__(self, name, image_file):
        self.name = name
        self.image_path = os.join(PATH, image_file)


if __name__ == "__main__":
    print("item module superclass")
