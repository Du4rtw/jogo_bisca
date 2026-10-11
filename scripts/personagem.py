class Personagem:
    def __init__(self,nome,pontuacao_mesa,pontuacao_raios,bot):
        self.nome = nome
        self.pontuacao_mesa = pontuacao_mesa
        self.pontuacao_raios = pontuacao_raios
        self.bot = bool(bot)

    def Adicionar_Pontos(self,pontos):
        self.pontuacao_mesa += pontos
        return self.pontuacao_mesa

