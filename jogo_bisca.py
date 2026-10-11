import pyxel
from scripts.menu_inicial import MenuInicial
from scripts.jogar import Jogar
from scripts.tela_final import TelaFinalJogo
from scripts.tela_estatisticas import TelaEstatisticas
from audio.gerenciador import GerenciadorAudio
from scripts.tela_creditos import TelaCreditos




#1 "partida" = quem conseguir vencer 4 rodadas primeiro;
#1 "Rodada" é composto por 20 jogadas de cada (acabar o baralho);
#Cada "jogada" é 1 carta escolhida por cada jogador para ir a mesa;
#A "mesa" é a comparação das duas cartas jogadas;
#A "mão" são as cartas que o jogador possui;
#A carta "bisca" é a carta horizontal na mesa que define o naipe

class JogoBisca:
    def __init__(self):
        pyxel.init(160, 120, title="Bisca", fps=60)
        pyxel.fullscreen(True) 
        pyxel.mouse(True) 
        pyxel.images[0].load(0, 0, "resources/Cards.png")

        self.cenariosJogo = {
            "Menu Inicial": MenuInicial(),
            "Jogar": Jogar(),
            "Estatisticas": TelaEstatisticas(),
            "Creditos" : TelaCreditos()
        }
        self.cenarioAtual = "Menu Inicial"
        pyxel.run(self.update, self.draw)



    def update(self):
        cenario_antigo = self.cenarioAtual
        proximo_cenario = self.cenariosJogo[self.cenarioAtual].update()

        if proximo_cenario != cenario_antigo:

            if proximo_cenario == "Menu Inicial":
                self.cenariosJogo["Jogar"] = Jogar()

            elif proximo_cenario == "Tela Final":
                self.cenariosJogo["Tela Final"] = TelaFinalJogo(self.cenariosJogo["Jogar"])

            elif proximo_cenario == "Estatisticas":
                destino = "Menu Inicial" if cenario_antigo == "Tela Final" else cenario_antigo
                self.cenariosJogo["Estatisticas"] = TelaEstatisticas(destino,self.cenariosJogo["Jogar"].sessao)

        self.cenarioAtual = proximo_cenario



    def draw(self):
        
        pyxel.cls(0)
        self.cenariosJogo[self.cenarioAtual].draw()

JogoBisca()