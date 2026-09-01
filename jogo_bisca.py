import pyxel
import json
import random

# Dimensões carta
LARGURA_CARTA = 18
ALTURA_CARTA = 28

#1 "partida" = quem conseguir vencer 4 rodadas primeiro;
#1 "Rodada" é composto por 20 jogadas de cada (acabar o baralho);
#Cada "jogada" é 1 carta escolhida por cada jogador para ir a mesa;
#A "mesa" é a comparação das duas cartas jogadas;
#A "mão" são as cartas que o jogador possui;
#A carta "bisca" é a carta horizontal na mesa que define o naipe


def carregar_cartas(caminho="cartas.json"):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


class MenuInicial:
    def __init__(self):
        pass

    def _verificar_clique_jogar(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if 60<=pyxel.mouse_x<=100 and 60<=pyxel.mouse_y<=70:
                return True

    def _botao_jogar(self):
        pyxel.rect(60,60, 40,10, 4)
        pyxel.text(70,62,"Jogar",7)

    def _desenhar_titulo_bisca(self, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    self._renderizar_letreiro_bisca(x + dx, y + dy, 0)

        
        self._renderizar_letreiro_bisca(x, y, 7) 

    def _renderizar_letreiro_bisca(self, x, y, cor):
        # B
        pyxel.rect(x, y, 2, 7, cor)
        pyxel.rect(x, y, 4, 1, cor)
        pyxel.rect(x, y + 3, 4, 1, cor)
        pyxel.rect(x, y + 6, 4, 1, cor)
        pyxel.pset(x + 4, y + 1, cor)
        pyxel.pset(x + 4, y + 2, cor)
        pyxel.pset(x + 4, y + 4, cor)
        pyxel.pset(x + 4, y + 5, cor)

        # I
        pyxel.rect(x + 6, y, 3, 1, cor)
        pyxel.rect(x + 7, y, 1, 7, cor)
        pyxel.rect(x + 6, y + 6, 3, 1, cor)

        # S
        pyxel.rect(x + 10, y, 5, 1, cor)
        pyxel.rect(x + 10, y + 3, 5, 1, cor)
        pyxel.rect(x + 10, y + 6, 5, 1, cor)
        pyxel.pset(x + 10, y + 1, cor)
        pyxel.pset(x + 10, y + 2, cor)
        pyxel.pset(x + 14, y + 4, cor)
        pyxel.pset(x + 14, y + 5, cor)

        # C
        pyxel.rect(x + 16, y, 5, 1, cor)
        pyxel.rect(x + 16, y + 6, 5, 1, cor)
        pyxel.rect(x + 16, y, 1, 7, cor)

        # A
        pyxel.rect(x + 22, y, 5, 1, cor)
        pyxel.rect(x + 22, y + 3, 5, 1, cor)
        pyxel.rect(x + 22, y, 1, 7, cor)
        pyxel.rect(x + 26, y, 1, 7, cor)    

    def update(self):
        if self._verificar_clique_jogar():
            return "Jogar"
        else:
            return "Menu Inicial"
            
    def draw(self):
        pyxel.cls(4)
        self._desenhar_titulo_bisca(66,25)
        self._botao_jogar()

      
        
        

class Jogar:
    def __init__(self):
        # mesa redonda 
        self.centro_x = 80
        self.centro_y = 60
        self.raio_externo = 53
        self.espessura_borda = 4

        self.desenhar_area=False

        # sorteia 4 cartas distintas: as 3 da mão + a carta rotacionada.
        self.cartas_disponiveis = carregar_cartas()
        cartas_sorteadas = random.sample(self.cartas_disponiveis, 4)

        # Cada item de self.cartas_mesa é um dicionário com:
        espaco_mao = 2
        pos_x_inicial = 51
        pos_y_mao = 90

        x_carta1 = pos_x_inicial                                    # 51
        x_carta2 = pos_x_inicial + LARGURA_CARTA + espaco_mao       # 71
        x_carta3 = pos_x_inicial + 2 * (LARGURA_CARTA + espaco_mao)  # 91

        self.cartas_mesa = [
            {
                "sprite": cartas_sorteadas[0],
                "x": x_carta1, "y": pos_y_mao,
                "origem_x": x_carta1, "origem_y": pos_y_mao,
                "rotacionada": False,
            },
            {
                "sprite": cartas_sorteadas[1],
                "x": x_carta2, "y": pos_y_mao,
                "origem_x": x_carta2, "origem_y": pos_y_mao,
                "rotacionada": False,
            },
            {
                "sprite": cartas_sorteadas[2],
                "x": x_carta3, "y": pos_y_mao,
                "origem_x": x_carta3, "origem_y": pos_y_mao,
                "rotacionada": False,
            },
        ]

        # carta do monte (baralho), fixa, virada para baixo 
        self.monte_x = 35
        self.monte_y = 46

        # carta rotacionada 90° no sentido horário
        altura_rotacionada = LARGURA_CARTA  # 18, após girar 90°
        espaco_monte = 1
        rot_x = self.monte_x + LARGURA_CARTA + espaco_monte
        rot_y = self.monte_y + (ALTURA_CARTA - altura_rotacionada) // 2

        self.cartas_mesa.append({
            "sprite": cartas_sorteadas[3],
            "x": rot_x, "y": rot_y,
            "origem_x": rot_x, "origem_y": rot_y,
            "rotacionada": True,
        })

        # Controle de arraste
        self.indice_arrastando = None
        self.offset_x = 0
        self.offset_y = 0

    def _dimensoes(self, carta):
        # Carta rotacionada 90° 
        if carta["rotacionada"]:
            return ALTURA_CARTA, LARGURA_CARTA
        return LARGURA_CARTA, ALTURA_CARTA

    def _arraste_carta(self):

        # de trás pra frente, para pegar a que está "por cima" primeiro
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            
            for i in reversed(range(len(self.cartas_mesa))):
                carta = self.cartas_mesa[i]
                largura, altura = self._dimensoes(carta)
                if (carta["x"] <= pyxel.mouse_x <= carta["x"] + largura and
                        carta["y"] <= pyxel.mouse_y <= carta["y"] + altura):
                    self.cartas_mesa.pop(i)
                    self.cartas_mesa.append(carta)
                    self.indice_arrastando = len(self.cartas_mesa) - 1
                    self.offset_x = pyxel.mouse_x - carta["x"]
                    self.offset_y = pyxel.mouse_y - carta["y"]
                    break
        
        # Enquanto o botão continua pressionado, a carta segue o mouse
        if self.indice_arrastando is not None and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.desenhar_area=True

            carta = self.cartas_mesa[self.indice_arrastando]
            carta["x"] = pyxel.mouse_x - self.offset_x
            carta["y"] = pyxel.mouse_y - self.offset_y
        
        # Soltou o botão -> a carta volta para a posição original
        if self.indice_arrastando is not None and pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            self.desenhar_area=False
            carta = self.cartas_mesa[self.indice_arrastando]
            carta["x"] = carta["origem_x"]
            carta["y"] = carta["origem_y"]
            self.indice_arrastando = None


    
    

    def _inicio_jogo(self):
        # Embaralhar as 40 cartas
        # Distribuição e cartas, sendo uma para a "bisca"(a primeira da pilha e a última a retirar e virada para cima) e três para cada jogador
        # Definir quem fará a primeira jogada

        return

    def _jogar_cartas(self):
        # O jogador vencedor será o primeiro a jogar a carta na mesa, posteriormente o segundo jogador
        # Chamar a função "_calc_mesa"
        # Será chamada a função "_proximo_pescar" quando o jogador tiver menos de 3 cartas na mão e o baralho for diferente de zero                
        return

    def _calc_mesa(self):
        # Após a jogada de cada jogador, as duas cartas na mesa serão analisadas a hierarquia delas, definindo o jogador vencedor da mesa
        # quando decidida a de maior hierarquia e vendo qual jogador que jogou. Essas duas cartas serão somadas a sua pontuação e adicionados a pontuação do jogador
        return
    
    
    def _proximo_pescar(self):
        # Jogador vencedor da "mesa" irá "pescar" primeiro, o segundo jogador posteriormente
        # A carta pescada será a primeira a entrar e a última a sair
        return

        
    
    
            


    
    def update(self):

        self._arraste_carta()
        
        
        return "Jogar"

    def _desenhar_jogadores(self):
        raio = 10
        cor_contorno = 0  
        cor_texto = 7     

        
        x_p1, y_p1 = 35, 95
        cor_p1 = 12 
        pyxel.circ(x_p1, y_p1, raio, cor_p1)
        pyxel.circb(x_p1, y_p1, raio, cor_contorno)
       
        pyxel.text(x_p1 - 4, y_p1 - 2, "P1", cor_texto)

        
        x_p2, y_p2 = 125, 25
        cor_p2 = 8  # Vermelho
        pyxel.circ(x_p2, y_p2, raio, cor_p2)
        pyxel.circb(x_p2, y_p2, raio, cor_contorno)
        
        pyxel.text(x_p2 - 3, y_p2 - 4, "BOT", cor_texto)


    def _desenhar_monte(self):
        # Representa o monte (baralho) virado para baixo. Como o Cards.png
        x, y = self.monte_x, self.monte_y

        pyxel.rect(x, y, LARGURA_CARTA, ALTURA_CARTA, 7)                      
        pyxel.rect(x + 1, y + 1, LARGURA_CARTA - 2, ALTURA_CARTA - 2, 8)       
        pyxel.rect(x + 3, y + 3, LARGURA_CARTA - 6, ALTURA_CARTA - 6, 7)       

        # Campo central com o padrão em xadrez
        campo_x, campo_y = x + 4, y + 4
        campo_largura, campo_altura = LARGURA_CARTA - 8, ALTURA_CARTA - 8
        tamanho_quadrado = 2
        for linha in range(campo_altura // tamanho_quadrado):
            for coluna in range(campo_largura // tamanho_quadrado):
                if (linha + coluna) % 2 == 0:
                    pyxel.rect(
                        campo_x + coluna * tamanho_quadrado,
                        campo_y + linha * tamanho_quadrado,
                        tamanho_quadrado, tamanho_quadrado,
                        8,
                    )

    def _desenhar_carta_rotacionada(self, dest_x, dest_y, u, v):

        for x in range(LARGURA_CARTA):
            for y in range(ALTURA_CARTA):
                cor = pyxel.images[0].pget(u + x, v + y)
                novo_x = ALTURA_CARTA - 1 - y
                novo_y = x
                pyxel.pset(dest_x + novo_x, dest_y + novo_y, cor)

    def _desenhar_mesa(self):
        # Borda externa de madeira (Círculo maior)
        pyxel.circ(self.centro_x, self.centro_y, self.raio_externo, 4)        
        pyxel.circb(self.centro_x, self.centro_y, self.raio_externo, 0)     
        
                # Feltro interno da mesa (Círculo menor)
        raio_interno = self.raio_externo - self.espessura_borda
        pyxel.circ(self.centro_x, self.centro_y, raio_interno, 11)         
        pyxel.circb(self.centro_x, self.centro_y, raio_interno, 3)  

    def _area_carta_jogada(self):       
        x, y = 85, 40
        largura, altura = 37, 40
        cores = [7, 7, 11, 11, 11, 11, 11] 

        for i in range(largura):
            cor = cores[i % 7] if (pyxel.frame_count // 20) % 2 == 0 else 11
            pyxel.pset(x + i, y, cor)
            pyxel.pset(x + i, y + altura - 1, cor)
        
        
        for i in range(altura):
            cor = cores[i % 7] if (pyxel.frame_count // 20) % 2 == 0 else 11
            pyxel.pset(x, y + i, cor)
            pyxel.pset(x + largura - 1, y + i, cor)

    def draw(self):
        pyxel.cls(3)

        self._desenhar_jogadores()

        self._desenhar_mesa()
        if self.desenhar_area==True:
            self._area_carta_jogada()

        # Monte (carta virada para baixo, fixa na mesa)
        self._desenhar_monte()

        # As 5 cartas (3 da mão + a carta rotacionada), usando o recorte
        for carta in self.cartas_mesa:
            sprite = carta["sprite"]
            if carta["rotacionada"]:
                self._desenhar_carta_rotacionada(carta["x"], carta["y"], sprite["posX"], sprite["posY"])
            else:
                pyxel.blt(
                    carta["x"], carta["y"],
                    0,
                    sprite["posX"], sprite["posY"],
                    LARGURA_CARTA, ALTURA_CARTA,
                )


class JogoBisca:
    def __init__(self):
        pyxel.init(160, 120, title="Bisca")
        pyxel.fullscreen(True) 
        pyxel.mouse(True) 

        pyxel.images[0].load(0, 0, "Cards.png")

        self.cenariosJogo={
            "Menu Inicial": MenuInicial(),
            "Jogar": Jogar()
        }
        self.cenarioAtual="Menu Inicial"


        pyxel.run(self.update, self.draw)
        
        
        

    def update(self):
        self.cenarioAtual=self.cenariosJogo[self.cenarioAtual].update()
        

    def draw(self):
        pyxel.cls(0)
        self.cenariosJogo[self.cenarioAtual].draw()
        


JogoBisca()