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

    def mediaStatus(self):
        qtd_valores, soma_valores = 0, 0.0
        for chave in self.status:
            if self.status.get(chave)[1] == self.nivel:
                soma_valores += self.status.get(chave)[0]
                qtd_valores += 1

        return soma_valores / qtd_valores

    def setStatus(self, valor, chave):
        self.status[chave][0] += valor
