class Quest():
    def __init__(self, nome, descricao, etapas, area_interacao):
        self.nome = nome
        self.descricao = descricao
        self.etapas = etapas
        self.etapa_atual = 0
        self.concluida = False
        self.area_interacao = area_interacao
