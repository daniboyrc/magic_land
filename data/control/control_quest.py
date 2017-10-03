def getQuest(player):
    quests = []
    descricao = []
    etapas = []

    for i in player.quest:
        quests.append(i.nome)
        descricao.append(i.descricao)
        etp = []
        for j in range(len(i.etapas)):
            if i.etapa_atual > j > 0:
                etp.append(i.etapas[j])
        etapas.append(etp)

    return quests, descricao, etapas
