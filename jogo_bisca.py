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

        # Área de soltar carta
        self.desenhar_area=False
        self.area_jogada_x = 85
        self.area_jogada_y = 40
        self.area_jogada_largura = 37
        self.area_jogada_altura = 40
        # Controle de arraste
        self.carta_arrastando = None
        self.offset_x = 0
        self.offset_y = 0

        self.contador_frame=None
        self.pode_limpar=None
        self.aguardar_bot=False
        self.contador_jogada_bot=None
    
        self.vez_jogador=0
        self.mao_j1=[]
        self.mao_j2=[]
        self.carta_bisca=[]
        self.monte = self._inicio_jogo()
        

        # se o sorteio definiu o bot como o primeiro a jogar, arma o delay dele
        if self.vez_jogador == 2 and self.mao_j2:
            self.contador_jogada_bot = pyxel.frame_count + 30
            self.aguardar_bot = True
        
        
        # Posição dos slots das cartas da mão
        espaco_mao = 2
        pos_x_inicial = 51
        pos_y_mao = 90
        self._posicoes_mao_j1 = [
            (pos_x_inicial, pos_y_mao),
            (pos_x_inicial + LARGURA_CARTA + espaco_mao, pos_y_mao),
            (pos_x_inicial + 2 * (LARGURA_CARTA + espaco_mao), pos_y_mao),
        ]

        self.cartas_mesa = []
        self._sincronizar_mao_j1()

        # carta do monte (baralho), fixa, virada para baixo 
        self.monte_x = 35
        self.monte_y = 46

        # carta rotacionada 90° no sentido horário
        altura_rotacionada = LARGURA_CARTA  # 18, após girar 90°
        espaco_monte = 1
        rot_x = self.monte_x + LARGURA_CARTA + espaco_monte
        rot_y = self.monte_y + (ALTURA_CARTA - altura_rotacionada) // 2

        self.cartas_mesa.append({
            "sprite": self.carta_bisca,
            "x": rot_x, "y": rot_y,
            "origem_x": rot_x, "origem_y": rot_y,
            "rotacionada": True,
            "arrastavel":False,
        })

        # Controle de arraste
        self.indice_arrastando = None
        self.offset_x = 0
        self.offset_y = 0

        # Controle da jogada atual
        self.carta_inicial = None
        self.carta_secundaria = None
        self.jogador_inicial = None
        self.jogador_secundario = None

        # Pontuações
        self.pontuacao_j1 = 0
        self.pontuacao_j2 = 0

    def _sincronizar_mao_j1(self):
            # Limpa a tela
            self.cartas_mesa = [c for c in self.cartas_mesa if c.get("grupo") != "mao_j1"]

            # Percorre seu número de índice
            for indice, carta in enumerate(self.mao_j1):
                # Busca a coordenada X e Y no slot específico
                x, y = self._posicoes_mao_j1[indice]
                self.cartas_mesa.append({
                    "sprite": carta,
                    "x": x, "y": y,
                    "origem_x": x, "origem_y": y,
                    "rotacionada": False,
                    "arrastavel": True,
                    "grupo": "mao_j1",
                })

    def _posicionar_carta_na_mesa(self, sprite, ordem):
            # Ordem: "inicial" ou "secundaria".
            x_base, y_base = 89, 41
            deslocamento_x = 11  
            deslocamento_y = 10  

            if ordem == "inicial":
                x, y = x_base, y_base
            else:
                x, y = x_base + deslocamento_x, y_base + deslocamento_y

            self.cartas_mesa.append({
                "sprite": sprite,
                "x": x, "y": y,
                "origem_x": x, "origem_y": y,
                "rotacionada": False,
                "arrastavel": False, 
            })

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
                if not carta.get("arrastavel", True):
                    continue
                largura, altura = self._dimensoes(carta)
                if (carta["x"] <= pyxel.mouse_x <= carta["x"] + largura and
                        carta["y"] <= pyxel.mouse_y <= carta["y"] + altura):
                    self.cartas_mesa.pop(i)
                    self.cartas_mesa.append(carta)
                    self.carta_arrastando = carta          # <-- referência, não índice
                    self.offset_x = pyxel.mouse_x - carta["x"]
                    self.offset_y = pyxel.mouse_y - carta["y"]
                    break

        # Enquanto o botão continua pressionado, a carta segue o mouse
        if self.carta_arrastando is not None and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            # a carta pode ter sido removida de cartas_mesa por uma limpeza no meio do arraste
            if self.carta_arrastando not in self.cartas_mesa:
                self.carta_arrastando = None
            else:
                self.desenhar_area = True
                carta = self.carta_arrastando
                carta["x"] = pyxel.mouse_x - self.offset_x
                carta["y"] = pyxel.mouse_y - self.offset_y

        # Soltou o botão -> a carta volta para a posição original
        if self.carta_arrastando is not None and pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            self.desenhar_area = False
            carta = self.carta_arrastando

            if carta in self.cartas_mesa and self._dentro_area(carta["x"], carta["y"]) and self.vez_jogador == 1:
                self.cartas_mesa.remove(carta)
                self.mao_j1 = [c for c in self.mao_j1 if c is not carta["sprite"]]
                self._sincronizar_mao_j1()
                self._jogar_cartas(carta["sprite"], jogador=1)
            elif carta in self.cartas_mesa:
                carta["x"] = carta["origem_x"]
                carta["y"] = carta["origem_y"]

            self.carta_arrastando = None

    def _dentro_area(self,x,y):
        return(self.area_jogada_x <= x <= self.area_jogada_x + self.area_jogada_largura and self.area_jogada_y <= y <= self.area_jogada_y + self.area_jogada_altura)

    def _bot_carta(self):
        if not self.mao_j2:
            return None
        indice = random.randint(0, len(self.mao_j2) - 1)
        # Adiconar um "timer" aqui 
        return self.mao_j2.pop(indice)
    
    def _inicio_jogo(self):

        cartas_originais = carregar_cartas()
        
        cartas_baralho = [{**carta, "jogador": "0", "bisca": "0"} for carta in cartas_originais]

        # Embaralhando usando o método do random
        random.shuffle(cartas_baralho)
        cartas_baralho[-1]["bisca"]="1"
        self.carta_bisca=cartas_baralho[-1]

        # Distribuindo cartas utilizando o .pop que seleciona a primeira carta do monte e remove ela
        for _ in range(3):
            self.mao_j1.append(cartas_baralho.pop(0))
            self.mao_j1[_]["jogador"]="1"
            self.mao_j2.append(cartas_baralho.pop(0))
            self.mao_j2[_]["jogador"]="2"

        

        # Definindo quem fará a primeira jogada
        self.vez_jogador=random.randint(1,2)

        return cartas_baralho
       
    def _jogar_cartas(self, carta_escolhida, jogador):
        if self.carta_inicial is None and self.carta_secundaria is None:
            self.jogador_inicial = self.vez_jogador
            self.jogador_secundario = 2 if self.jogador_inicial == 1 else 1

        if self.carta_inicial is None:
            self.carta_inicial = carta_escolhida
            self.vez_jogador = self.jogador_secundario
            self._posicionar_carta_na_mesa(carta_escolhida, ordem="inicial")

            # se quem vai responder agora é o bot, arma o delay antes dele jogar
            if self.jogador_secundario == 2 and self.mao_j2:
                self.contador_jogada_bot = pyxel.frame_count + 30  # ~0.5s de "pensamento"
                self.aguardar_bot = True

        elif self.carta_secundaria is None:
            self.carta_secundaria = carta_escolhida
            self._posicionar_carta_na_mesa(carta_escolhida, ordem="secundaria")
            self._calc_mesa()

    def _calc_mesa(self):
        naipe_bisca = self.carta_bisca["naipe"]

        if self.carta_inicial["naipe"] == self.carta_secundaria["naipe"]:
            if int(self.carta_secundaria["forca"]) > int(self.carta_inicial["forca"]):
                vencedor = self.jogador_secundario
            else:
                vencedor = self.jogador_inicial
        elif self.carta_secundaria["naipe"] == naipe_bisca:
            vencedor = self.jogador_secundario
        else:
            vencedor = self.jogador_inicial

        pontuacao_mesa = int(self.carta_inicial["valor"]) + int(self.carta_secundaria["valor"])
        if vencedor == 1:
            self.pontuacao_j1 += pontuacao_mesa
        else:
            self.pontuacao_j2 += pontuacao_mesa

        self.vez_jogador = vencedor
        outro_jogador = 2 if vencedor == 1 else 1 # Se o vencedor foi o Jogador 1, o outro é o 2

        # limpa a mesa (cartas jogadas somem) para a próxima jogada
        # Adiconar um "timer" aqui 
        self.contador_frame=pyxel.frame_count+60
        self.pode_limpar=True
        
       


        if len(self.monte) >= 2:
            self._proximo_pescar(vencedor)
            self._proximo_pescar(outro_jogador)
        else:
            pass
            # acabou o monte, estatistica e quem são os vencedores

        

        return vencedor

    def _proximo_pescar(self,jogador):
   
        carta_pescada = self.monte.pop(0)

        if jogador == 1:
            self.mao_j1.append(carta_pescada)
            self.mao_j1[-1]["jogador"] = "1"
            self._sincronizar_mao_j1()
        else:
            self.mao_j2.append(carta_pescada)
            self.mao_j2[-1]["jogador"] = "2"
        return
            

    
    def update(self):

        self._arraste_carta()

        # limpeza da mesa após a rodada + arma o delay do bot para abrir a próxima
        if self.pode_limpar and pyxel.frame_count >= self.contador_frame:
            self.cartas_mesa = [c for c in self.cartas_mesa if c["sprite"] not in (self.carta_inicial, self.carta_secundaria)]
            self.pode_limpar = False
            self.carta_inicial = None
            self.carta_secundaria = None

            if self.vez_jogador == 2 and self.mao_j2:
                self.contador_jogada_bot = pyxel.frame_count + 30
                self.aguardar_bot = True

        # dispara a jogada do bot quando o delay (de qualquer origem) estourar
        if self.aguardar_bot and pyxel.frame_count >= self.contador_jogada_bot:
            self.aguardar_bot = False
            carta_bot = self._bot_carta()
            self._jogar_cartas(carta_bot, jogador=2)

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
        pyxel.init(160, 120, title="Bisca", fps=60)
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
