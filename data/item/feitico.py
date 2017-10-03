from item import *


class Feitico(Item):
    def __init__(self, nome, local, idfeitico, descricao, nivel,
                 dificuldade, tipo, status, ex_solucao):
        super(Feitico, self).__init__(nome, local)
        self.id = idfeitico
        self.descricao = descricao
        self.nivel = nivel
        self.dificuldade = dificuldade
        self.tipo = tipo
        self.status = status
        self.ex_solucao = ex_solucao

        self.solucao = ''

    def __str__(self):
        return 'feitico'

    def setSolucao(self, solucao):
        self.solucao = solucao
