class Level():
    def __init__(self):
        self.level = 0
        self.progresso = 0
        self.nivel = 0
        self.dificuldade = 0

    def setProgresso(self, media_status):
        self.progresso = media_status

    def setLevel(self):
        self.level = (self.progresso + self.nivel * 100) / 16.25

    def setDificuldade(self):
        if self.progresso // 16.25 > self.dificuldade:
            self.dificuldade += 1

    def setNivel(self):
        if self.progresso >= 100:
            self.nivel += 1
            self.dificuldade = 0
