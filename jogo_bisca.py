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

class Personagem:
    def __init__(self,nome,pontuacao_mesa,pontuacao_raios,bot):
        self.nome = nome
        self.pontuacao_mesa = pontuacao_mesa
        self.pontuacao_raios = pontuacao_raios
        self.pontuacao_total = 0

        self.bot = bool(bot)

    def Adicionar_Pontos(self,pontos):
        self.pontuacao_mesa += pontos
        return self.pontuacao_mesa



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


class TelaFinalJogo:
    def __init__(self, partida):
        # Recebe a partida anterior para extrair as pontuações
        self.partida = partida

    def update(self):
        # Como solicitado, sem interações por enquanto
        return "Tela Final"
    
    def _desenhar_tally(self, x, y, quantidade, cor):
        espaco = 3          
        altura_traco = 5
        verticais = min(quantidade, 3)
        for i in range(verticais):
            tx = x + i * espaco
            pyxel.line(tx, y, tx, y + altura_traco, cor)
        if quantidade >= 4:
            meio_y = y + (altura_traco // 2)
            pyxel.line(x - 1, meio_y, x + (2 * espaco) + 1, meio_y, cor)

    def _desenhar_seta(self, x, y, direcao, texto):
        cor_seta = 10  # Amarelo
        cor_contorno = 0
        largura_texto = len(texto) * 4

        if direcao == "esq":
            pyxel.trib(x, y+4, x+6, y, x+6, y+8, cor_contorno)
            pyxel.tri(x+1, y+4, x+5, y+1, x+5, y+7, cor_seta)
            pyxel.rectb(x+6, y+2, 6, 5, cor_contorno)
            pyxel.rect(x+6, y+3, 5, 3, cor_seta)
            pyxel.line(x+6, y+3, x+6, y+5, cor_seta) # Apaga linha divisória
            pyxel.text(x + 14, y + 2, texto, 0)
        else:
            pyxel.text(x - largura_texto - 4, y + 2, texto, 0)
            pyxel.rectb(x, y+2, 6, 5, cor_contorno)
            pyxel.rect(x+1, y+3, 5, 3, cor_seta)
            pyxel.trib(x+6, y, x+12, y+4, x+6, y+8, cor_contorno)
            pyxel.tri(x+7, y+1, x+11, y+4, x+7, y+7, cor_seta)
            pyxel.line(x+6, y+3, x+6, y+5, cor_seta) # Apaga linha divisória

    def draw(self):
        # 1. Desenha a mesa desfocada/ao fundo
        pyxel.cls(3)
        self.partida._desenhar_jogadores()
        self.partida._desenhar_mesa()
        
        # 2. Descobre quem ganhou
        venceu_p1 = self.partida.jogador1.pontuacao_raios >= 4
        texto_vitoria = "PLAYER 1 VENCEU!" if venceu_p1 else "BOT VENCEU!"
        cor_vitoria = 12 if venceu_p1 else 8
        larg_vitoria = len(texto_vitoria) * 4
        pyxel.text(80 - (larg_vitoria // 2), 10, texto_vitoria, cor_vitoria)

        # 3. O Grande Caderno Aberto
        cad_x, cad_y = 20, 20
        cad_largura, cad_altura = 120, 75

        # Sombra e Folhas
        pyxel.rect(cad_x + 2, cad_y + 2, cad_largura, cad_altura, 1)
        pyxel.rect(cad_x, cad_y, cad_largura, cad_altura, 7)
        pyxel.rectb(cad_x, cad_y, cad_largura, cad_altura, 13)
        pyxel.line(cad_x + 60, cad_y, cad_x + 60, cad_y + cad_altura, 13) # Divisão

        # Mola central
        espaco_espiral = 6
        quantidade_argolas = cad_altura // espaco_espiral
        for i in range(quantidade_argolas):
            ay = cad_y + 4 + i * espaco_espiral
            pyxel.circb(80, ay, 2, 5)
            pyxel.pset(80, ay, 6)

        # --- LADO ESQUERDO (PLAYER 1) ---
        centro_esq = cad_x + 30
        
        texto_p1 = "Player 1"
        pyxel.text(centro_esq - (len(texto_p1)*4//2), cad_y + 8, texto_p1, 12)
        
        lbl_pontos = "Pontuacao"
        pyxel.text(centro_esq - (len(lbl_pontos)*4//2), cad_y + 22, lbl_pontos, 12)
        pts_p1 = str(self.partida.jogador1.pontuacao_total)
        pyxel.text(centro_esq - (len(pts_p1)*4//2), cad_y + 30, pts_p1, 0)
        
        lbl_raios = "Raios"
        pyxel.text(centro_esq - (len(lbl_raios)*4//2), cad_y + 44, lbl_raios, 12)
        # O tally tem ~10px de largura, então subtraímos 5 para centralizar perfeitamente
        self._desenhar_tally(centro_esq - 4, cad_y + 52, self.partida.jogador1.pontuacao_raios, 12)

        # --- LADO DIREITO (BOT) ---
        centro_dir = cad_x + 90
        
        texto_bot = "Bot"
        pyxel.text(centro_dir - (len(texto_bot)*4//2), cad_y + 8, texto_bot, 8)
        
        pyxel.text(centro_dir - (len(lbl_pontos)*4//2), cad_y + 22, lbl_pontos, 8)
        pts_bot = str(self.partida.jogador2.pontuacao_total)
        pyxel.text(centro_dir - (len(pts_bot)*4//2), cad_y + 30, pts_bot, 0)
        
        pyxel.text(centro_dir - (len(lbl_raios)*4//2), cad_y + 44, lbl_raios, 8)
        self._desenhar_tally(centro_dir - 4, cad_y + 52, self.partida.jogador2.pontuacao_raios, 8)

        # 4. Setas de página
        self._desenhar_seta(cad_x + 4, cad_y + cad_altura - 12, "esq", "Menu Inicial")
        self._desenhar_seta(cad_x + cad_largura - 16, cad_y + cad_altura - 12, "dir", "Novo Jogo")     

        

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

        # Timer
        self.contador_frame=None
        self.pode_limpar=False
        self.aguardar_bot=False
        self.contador_jogada_bot=None

        # Definições do personagem
        self.jogador1 = Personagem("Personagem1",0,0,False)
        self.jogador2 = Personagem("Bot",0,0,True)
        self.jogo_finalizado = False

        # Preparar as propriedades'
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

        self._carta_bisca()

        # Controle de arraste
        self.indice_arrastando = None
        self.offset_x = 0
        self.offset_y = 0

        # Controle da jogada atual
        self.carta_inicial = None
        self.carta_secundaria = None
        self.jogador_inicial = None
        self.jogador_secundario = None

    def _carta_bisca(self):
        # Remove bisca antiga
        self.cartas_mesa = [c for c in self.cartas_mesa if c.get("grupo") != "bisca"]

        if len(self.monte) >= 2:
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
                "arrastavel": False,
                "grupo": "bisca",
            })
        else:
            pass
    
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

        # 1. PEGAR A CARTA: Livre! O jogador pode clicar e arrastar a qualquer momento.
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

        # 2. MOVER A CARTA: Enquanto o botão estiver pressionado, a carta segue o mouse.
        if self.carta_arrastando is not None and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            if self.carta_arrastando not in self.cartas_mesa:
                self.carta_arrastando = None
            else:
                self.desenhar_area = True
                carta = self.carta_arrastando
                carta["x"] = pyxel.mouse_x - self.offset_x
                carta["y"] = pyxel.mouse_y - self.offset_y

        # 3. SOLTAR A CARTA: Aqui acontece a mágica e o bloqueio de segurança.
        if self.carta_arrastando is not None and pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            self.desenhar_area = False
            carta = self.carta_arrastando

            # Só aceita a jogada se estiver na área, SE for a vez do P1 e SE o jogo não estiver pausado
            if (carta in self.cartas_mesa and 
                self._dentro_area(carta["x"], carta["y"]) and 
                self.vez_jogador == 1 and 
                self._pode_jogador_jogar()):
                
                self.cartas_mesa.remove(carta)
                self.mao_j1 = [c for c in self.mao_j1 if c is not carta["sprite"]]
                self._sincronizar_mao_j1()
                self._jogar_cartas(carta["sprite"], jogador=1)
                
            elif carta in self.cartas_mesa:
                # Se soltou fora da área, ou se não era a vez dele, a carta volta pra mão!
                carta["x"] = carta["origem_x"]
                carta["y"] = carta["origem_y"]

            self.carta_arrastando = None

    def _dentro_area(self, x, y):

        centro_x = x + (LARGURA_CARTA // 2)
        centro_y = y + (ALTURA_CARTA // 2)

        return (self.area_jogada_x <= centro_x <= self.area_jogada_x + self.area_jogada_largura and 
                self.area_jogada_y <= centro_y <= self.area_jogada_y + self.area_jogada_altura)

    def _bot_carta(self):
        if not self.mao_j2:
            return None
        indice = random.randint(0, len(self.mao_j2) - 1)
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
            self.jogador1.Adicionar_Pontos(pontuacao_mesa)
            print(f"jogador1 = {self.jogador1.pontuacao_mesa}")
        else:
            self.jogador2.Adicionar_Pontos(pontuacao_mesa)
            print(f"jogador 2 = {self.jogador2.pontuacao_mesa} ")

        self.vez_jogador = vencedor

        # Arma o timer de 60 frames para limpar a mesa visualmente
        self.contador_frame=pyxel.frame_count+60
        self.pode_limpar=True      

        # RETIRAMOS AS FUNÇÕES DE PESCAR E SOMAR RAIO DAQUI!
        # Elas vão acontecer só quando a mesa for limpa no update.

        return vencedor


    def update(self):
        self._arraste_carta()

        # limpeza da mesa após a rodada + arma o delay do bot para abrir a próxima
        if self.pode_limpar and pyxel.frame_count >= self.contador_frame:
            # 1. Limpa as cartas do centro da mesa
            self.cartas_mesa = [c for c in self.cartas_mesa if c["sprite"] not in (self.carta_inicial, self.carta_secundaria)]
            self.pode_limpar = False
            self.carta_inicial = None
            self.carta_secundaria = None

            # 2. AGORA SIM, visualmente, os jogadores pescam as novas cartas!
            vencedor = self.vez_jogador
            outro_jogador = 2 if vencedor == 1 else 1

            if len(self.monte) > 0:
                self._proximo_pescar(vencedor)
                self._proximo_pescar(outro_jogador)
                
                # Se as duas cartas que acabaram de ser pescadas eram as últimas (zerou):
                if len(self.monte) == 0:
                    self._carta_bisca() # Isso vai remover a bisca da mesa
            
            # 3. Verifica se o raio/jogo acabou
            self._pontuacao_raio()

            # 4. Se o jogo continuar e for a vez do bot, arma o delay dele jogar
            if self.vez_jogador == 2 and self.mao_j2:
                self.contador_jogada_bot = pyxel.frame_count + 30
                self.aguardar_bot = True

        # dispara a jogada do bot quando o delay (de qualquer origem) estourar
        if self.aguardar_bot and pyxel.frame_count >= self.contador_jogada_bot:
            self.aguardar_bot = False
            carta_bot = self._bot_carta()
            self._jogar_cartas(carta_bot, jogador=2)

        return "Jogar"
    
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

    def _pontuacao_raio(self):
       
        if self.monte or self.mao_j1 or self.mao_j2:
            return

        self.jogador1.pontuacao_total += self.jogador1.pontuacao_mesa
        self.jogador2.pontuacao_total += self.jogador2.pontuacao_mesa

        # Definindo quem ganhou o raio e vendo se terminou o jogo
        # Mudar esses prints para futuras telas
        if self.jogador1.pontuacao_mesa > self.jogador2.pontuacao_mesa:
            self.jogador1.pontuacao_raios += 1
            print(f"Jogador vencedor deste raio: {self.jogador1.nome}") 
            print("Tela final_raio")
            if self.jogador1.pontuacao_raios > 3:
                print(f"Acabou o jogo, {self.jogador1.nome} tem {self.jogador1.pontuacao_raios} pontosde raio")
                print("Tela final_Partida")

        elif self.jogador2.pontuacao_mesa > self.jogador1.pontuacao_mesa:
            self.jogador2.pontuacao_raios += 1
            print(f"Jogador vencedor deste raio: {self.jogador2.nome}") 
            print("Tela final_raio")
            if self.jogador2.pontuacao_raios > 3:
                print(f"Acabou o jogo, {self.jogador2.nome} tem {self.jogador2.pontuacao_raios} pontos de raio")
                print("Tela final_Partida")
        else: 
            print("Raio empatado, não será somado pontuação") 
            print("Novo Jogo e estatisticas")

        # Zerar variaveis de pontuação de mesa
        self.jogador1.pontuacao_mesa = 0
        self.jogador2.pontuacao_mesa = 0
        self.vez_jogador=0
        self.mao_j1=[]
        self.mao_j2=[]
        self.carta_bisca=[]
        self.cartas_mesa = []
        
        self.monte = self._inicio_jogo() 
        self._sincronizar_mao_j1()
        
        self._carta_bisca()

    def _pode_jogador_jogar(self):
        return (not self.aguardar_bot
                and not self.pode_limpar
                and self.carta_secundaria is None)    



    def update(self):

       
# --- ATALHO DE DESENVOLVEDOR (Pressione F para testar a Tela Final) ---
        if pyxel.btnp(pyxel.KEY_F):
            self.jogador1.pontuacao_raios = 4
            self.jogador1.pontuacao_total = 254 
            self.jogador2.pontuacao_raios = 2
            self.jogador2.pontuacao_total = 130
            self.jogo_finalizado = True
        # ----------------------------------------------------------------------

        # ---> TRAVA 2: SE O JOGO ACABOU, ELE TRAVA AQUI E MANDA PRA TELA FINAL
        if self.jogo_finalizado:
            return "Tela Final"        
        self._arraste_carta()

        
        if self.pode_limpar and pyxel.frame_count >= self.contador_frame:
           
            self.cartas_mesa = [c for c in self.cartas_mesa if c["sprite"] not in (self.carta_inicial, self.carta_secundaria)]
            self.pode_limpar = False
            self.carta_inicial = None
            self.carta_secundaria = None

            
            vencedor = self.vez_jogador
            outro_jogador = 2 if vencedor == 1 else 1

            if len(self.monte) > 0:
                self._proximo_pescar(vencedor)
                self._proximo_pescar(outro_jogador)
                
             
                if len(self.monte) == 0:
                    self._carta_bisca() 
            
            self._pontuacao_raio()

            
            if self.vez_jogador == 2 and self.mao_j2:
                self.contador_jogada_bot = pyxel.frame_count + 30
                self.aguardar_bot = True

      
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

        if len(self.monte) >= 2:
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
        else:
            pass

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


    def _desenhar_tally(self, x, y, quantidade, cor):
       
        espaco = 3          
        altura_traco = 5

        verticais = min(quantidade, 3)
        for i in range(verticais):
            tx = x + i * espaco
            pyxel.line(tx, y, tx, y + altura_traco, cor)

   
        if quantidade >= 4:
            meio_y = y + (altura_traco // 2)
        
            pyxel.line(x - 1, meio_y, x + (2 * espaco) + 1, meio_y, cor)

    def _desenhar_caderno(self):
        cad_x, cad_y = 120, 90
        cad_largura, cad_altura = 36, 26

        pyxel.rect(cad_x + 1, cad_y + 1, cad_largura, cad_altura, 1)

        pyxel.rect(cad_x, cad_y, cad_largura, cad_altura, 7)
        pyxel.rectb(cad_x, cad_y, cad_largura, cad_altura, 13)

      
        espaco_espiral = 4
        quantidade_argolas = cad_altura // espaco_espiral
        for i in range(quantidade_argolas):
            ax = cad_x                             
            ay = cad_y + 3 + i * espaco_espiral    
            pyxel.circb(ax, ay, 1, 5)              
            pyxel.pset(ax, ay, 6)                  

        pyxel.line(cad_x + 5, cad_y + 8, cad_x + cad_largura - 2, cad_y + 8, 6)

    
        raio_atual = self.jogador1.pontuacao_raios + self.jogador2.pontuacao_raios + 1
        pyxel.text(cad_x + 5, cad_y + 3, f"Raio {raio_atual}", 0)

       
        pyxel.text(cad_x + 5, cad_y + 11, "P1", 12)
        pyxel.text(cad_x + 5, cad_y + 19, "BOT", 8)

        self._desenhar_tally(cad_x + 23, cad_y + 11, self.jogador1.pontuacao_raios, 12)
        self._desenhar_tally(cad_x + 23, cad_y + 19, self.jogador2.pontuacao_raios, 8)
        
    
    def draw(self):
        pyxel.cls(3)

        self._desenhar_jogadores()

        self._desenhar_mesa()
        if self.desenhar_area==True:
            self._area_carta_jogada()

        # Monte (carta virada para baixo, fixa na mesa)
        self._desenhar_monte()
        self._desenhar_caderno()

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
        proximo_cenario = self.cenariosJogo[self.cenarioAtual].update()
        
        
        if proximo_cenario == "Tela Final" and "Tela Final" not in self.cenariosJogo:
            self.cenariosJogo["Tela Final"] = TelaFinalJogo(self.cenariosJogo["Jogar"])

        self.cenarioAtual = proximo_cenario
        

    def draw(self):
        pyxel.cls(0)
        self.cenariosJogo[self.cenarioAtual].draw()
        


JogoBisca()
