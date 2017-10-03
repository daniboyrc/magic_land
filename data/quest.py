class Quest():
    def __init__(self, nome, descricao, etapas, itens_dar, itens_pegar, disponivel, prox=None):
        self.nome = nome
        self.descricao = descricao
        self.etapas = etapas
        self.etapa_atual = 0
        self.disponivel = disponivel
        self.itens_dar = itens_dar
        self.itens_pegar = itens_pegar
        self.dialogo = None
        self.proxima = prox

    def __str__(self):
        return self.nome

    def setDialogo(self, dialogo):
        self.dialogo = dialogo

    def setEtapa(self, player):
        if self.etapa_atual == 0:
            player.newQuest(self)

        self.item(player)
        self.etapa_atual += 1

        if self.etapa_atual == len(self.etapas):
            self.disponivel = False
            if self.proxima:
                self.proxima.disponivel = True
            player.removeQuest(self)

    def item(self, player):
        if self.itens_dar[self.etapa_atual] is not None:
            player.newItem(self.itens_dar[self.etapa_atual])
        if self.itens_pegar[self.etapa_atual] is not None:
            player.removeItem(self.itens_pegar[self.etapa_atual])
