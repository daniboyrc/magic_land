# coding: utf-8

import sqlite3
from random import randint
import os
from ..item import feitico as ft
from ..tst import main as tst_run


PATH_DB = os.path.join(os.getcwd(), 'resources', 'feitico.db')
PATH_FEITICO = os.path.join(os.getcwd(), 'resources', 'feiticos')
PATH_FEITICO_RELATIVO = 'resources/feiticos/'
VALOR = '70'
LOCAL = 'resources/itens/feitico.png'


class controllFeitico():
    def __init__(self, player):
        self.player = player
        self.status = player.status
        self.level = player.level

        self.conn = sqlite3.connect(PATH_DB)
        self.cursor = self.conn.cursor()

    def selectFeitico(self):
        menor_status = "'" + self.menorStatus() + "'"
        nivel = str(self.level.nivel)
        dificuldade = str(self.level.dificuldade)

        id_feitico = self.cursor.execute("""
        SELECT id_feitico FROM feitico
        WHERE nivel = %s
        and dificuldade = %s
        and disponivel = 1
        """ % (nivel, dificuldade))

        lista = []
        for id_f in id_feitico.fetchall():
            lista.append(self.cursor.execute("""
                SELECT id_feitico FROM status WHERE
                id_feitico = %s
                and assunto like %s
                and valor > %s
            """ % (id_f[0], menor_status, VALOR)).fetchall()[0])

        feitico = self.cursor.execute("""
            SELECT id_feitico, nome, descricao, nivel, dificuldade,
            tipo, ex_solucao FROM feitico WHERE
            id_feitico = %s
        """ % (lista[randint(0, len(lista) - 1)][0]))

        feitico = feitico.fetchall()[0]

        status = self.cursor.execute("""
            SELECT assunto, valor FROM status WHERE
            id_feitico = %s
            """ % (feitico[0]))

        return feitico, status.fetchall()

    def pesquisaFeitico(self, nome):
        nome = "'" + nome + "'"

        feitico = self.cursor.execute("""
        SELECT id_feitico, nome, descricao, nivel, dificuldade,
        tipo, ex_solucao FROM feitico
        WHERE nome = %s
        """ % (nome))

        feitico = feitico.fetchall()[0]

        status = self.cursor.execute("""
        SELECT assunto, valor FROM status WHERE
        id_feitico = %s
        """ % (feitico[0]))

        return feitico, status.fetchall()

    def addFeitico(self, nome=None):
        if nome:
            feitico, status = self.pesquisaFeitico(nome)
        else:
            feitico, status = self.selectFeitico()
        item = ft.Feitico(
            feitico[1],
            LOCAL,
            feitico[0],
            feitico[2],
            feitico[3],
            feitico[4],
            feitico[5],
            feitico[6],
            status)
        return item

    def concluiFeitico(self, id_feitico):
        self.cursor.execute("""
            UPDATE feitico
            SET disponivel = 0
            WHERE id_feitico = %s
            """ % (id_feitico))

    def menorStatus(self):
        status = self.status.status
        nivel = self.level.nivel
        status_menor = ''
        menor = 100
        for chave in status:
            if status[chave][1] == nivel:
                if status[chave][0] < menor:
                    menor = status[chave][0]
                    status_menor = chave

        return status_menor


def verifica_feitico(id_feitico):
    conn = sqlite3.connect(PATH_DB)
    cursor = conn.cursor()

    # select json
    json = cursor.execute("""
    SELECT json FROM feitico
    WHERE id_feitico = %s
    """ % (id_feitico))

    json = json.fetchall()[0][0]
    conn.close()

    # salvando .json
    filename = PATH_FEITICO_RELATIVO + str(id_feitico) + '.py'
    test = PATH_FEITICO_RELATIVO + 'tst.json'

    arq = open(test, 'w')
    arq.write(json)
    arq.close()

    print tst_run(filename.decode('utf-8'), test.decode('utf-8'))

    arq = open(test, 'w')
    arq.write('')
    arq.close()

def getFeitico(player):
    id_feitico = []
    feiticos = []
    descricao = []
    for i in player.inventario:
        if str(i) == 'feitico':
            id_feitico.append(i.id)
            feiticos.append(i.nome)
            descricao.append(i.descricao)

    return id_feitico, feiticos, descricao
