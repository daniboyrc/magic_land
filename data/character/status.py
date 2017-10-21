#!/usr/bin/env python
# coding: utf-8
# (c) 2017 Daniel Coura, UFCG

STEP = 33


class Status():
    def __init__(self):
        self.status = {'tipos': [0, 0],
                       'operadores': [0, 0],
                       'entrada': [0, 0],
                       'booleano': [0, 1],
                       'logica': [0, 1],
                       'if_else': [0, 1],
                       'elif': [0, 1],
                       'math': [0, 1],
                       'lacos_definidos': [0, 2],
                       'lacos_indefinidos': [0, 2],
                       'listas': [0, 3],
                       'append': [0, 3],
                       'pop': [0, 3],
                       'insertion': [0, 3],
                       'bubble': [0, 3],
                       'busca': [0, 3],
                       'matriz': [0, 4],
                       'dicionario': [0, 4],
                       }
        self.level = 0
        self.step = 0

    def _avarage_status(self):
        amount_values, sum_values = 0, 0.0
        for chave in self.status:
            if self.status.get(chave)[1] == self.level:
                sum_values += self.status.get(chave)[0]
                amount_values += 1

        return sum_values / amount_values

    def increment_status(self, value, key):
        self.status[key][0] += value

    def refresh_step(self):
        if self._avarage_status() // STEP > self.step:
            self.step += 1

    def refresh_level(self):
        if self._avarage_status() >= 100:
            self.level += 1
            self.step = 0


if __name__ == "__main__":
    print("status module")
