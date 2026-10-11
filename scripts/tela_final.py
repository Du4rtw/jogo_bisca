import pyxel

class TelaFinalJogo:
    def __init__(self, partida):
        self.partida = partida
        self.hover_botao = False 



    def update(self):
        self.hover_botao = (90 <= pyxel.mouse_x <= 150) and (80 <= pyxel.mouse_y <= 95)

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.hover_botao:
            # Checa se algum jogador alcançou 4 raios para o fim da partida
            if self.partida.jogador1.pontuacao_raios >= 4 or self.partida.jogador2.pontuacao_raios >= 4:
                return "Estatisticas"
            else:
                self.partida._resetar_raio()
                self.partida.fim_raio = False
                return "Jogar"
                
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
        # SE O MOUSE ESTIVER EM CIMA, AS CORES MUDAM!
        cor_seta = 9 if self.hover_botao else 10 
        cor_texto = 8 if self.hover_botao else 0
        cor_contorno = 0
        largura_texto = len(texto) * 4

        if direcao == "esq":
            pyxel.trib(x, y+4, x+6, y, x+6, y+8, cor_contorno)
            pyxel.tri(x+1, y+4, x+5, y+1, x+5, y+7, cor_seta)
            pyxel.rectb(x+6, y+2, 6, 5, cor_contorno)
            pyxel.rect(x+6, y+3, 5, 3, cor_seta)
            pyxel.line(x+6, y+3, x+6, y+5, cor_seta) 
            pyxel.text(x + 14, y + 2, texto, 0)
        else:
            pyxel.text(x - largura_texto - 4, y + 2, texto, cor_texto)
            pyxel.rectb(x, y+2, 6, 5, cor_contorno)
            pyxel.rect(x+1, y+3, 5, 3, cor_seta)
            pyxel.trib(x+6, y, x+12, y+4, x+6, y+8, cor_contorno)
            pyxel.tri(x+7, y+1, x+11, y+4, x+7, y+7, cor_seta)
            pyxel.line(x+6, y+3, x+6, y+5, cor_seta) 



    def draw(self):
        pyxel.cls(3)
        self.partida._desenhar_jogadores()
        self.partida._desenhar_mesa()
        p1 = self.partida.jogador1
        bot = self.partida.jogador2
        partida_acabou = p1.pontuacao_raios >= 4 or bot.pontuacao_raios >= 4

        if partida_acabou:
            texto_vitoria = "PLAYER 1 VENCEU!" if p1.pontuacao_raios >= 4 else "BOT VENCEU!"
        elif p1.pontuacao_mesa > bot.pontuacao_mesa:
            texto_vitoria = "PLAYER 1 VENCEU O RAIO!"
        elif bot.pontuacao_mesa > p1.pontuacao_mesa:
            texto_vitoria = "BOT VENCEU O RAIO!"
        else:
            texto_vitoria = "RAIO EMPATADO!"

        larg_vitoria = len(texto_vitoria) * 4
        pyxel.text(80 - (larg_vitoria // 2), 10, texto_vitoria, 7)
        cad_x, cad_y = 20, 20
        cad_largura, cad_altura = 120, 75
        
        pyxel.rect(cad_x + 2, cad_y + 2, cad_largura, cad_altura, 1)
        pyxel.rect(cad_x, cad_y, cad_largura, cad_altura, 7)
        pyxel.rectb(cad_x, cad_y, cad_largura, cad_altura, 13)
        pyxel.line(cad_x + 60, cad_y, cad_x + 60, cad_y + cad_altura, 13) 
        
        espaco_espiral = 6
        quantidade_argolas = cad_altura // espaco_espiral
        for i in range(quantidade_argolas):
            ay = cad_y + 4 + i * espaco_espiral
            pyxel.circb(80, ay, 2, 5)
            pyxel.pset(80, ay, 6)
        
        centro_esq = cad_x + 30
        texto_p1 = "Player 1"
        pyxel.text(centro_esq - (len(texto_p1)*4//2), cad_y + 8, texto_p1, 12)
        lbl_pontos = "Pontuacao"
        pyxel.text(centro_esq - (len(lbl_pontos)*4//2), cad_y + 22, lbl_pontos, 12)
        pts_p1 = str(self.partida.jogador1.pontuacao_mesa)
        pyxel.text(centro_esq - (len(pts_p1)*4//2), cad_y + 30, pts_p1, 0)
        lbl_raios = "Raios"
        pyxel.text(centro_esq - (len(lbl_raios)*4//2), cad_y + 44, lbl_raios, 12)
        self._desenhar_tally(centro_esq - 4, cad_y + 52, self.partida.jogador1.pontuacao_raios, 12)
        
        centro_dir = cad_x + 90
        texto_bot = "Bot"
        pyxel.text(centro_dir - (len(texto_bot)*4//2), cad_y + 8, texto_bot, 8)
        pyxel.text(centro_dir - (len(lbl_pontos)*4//2), cad_y + 22, lbl_pontos, 8)
        pts_bot = str(self.partida.jogador2.pontuacao_mesa)
        pyxel.text(centro_dir - (len(pts_bot)*4//2), cad_y + 30, pts_bot, 0)
        pyxel.text(centro_dir - (len(lbl_raios)*4//2), cad_y + 44, lbl_raios, 8)
        self._desenhar_tally(centro_dir - 4, cad_y + 52, self.partida.jogador2.pontuacao_raios, 8)

        if partida_acabou:
            self._desenhar_seta(cad_x + cad_largura-2, cad_y + cad_altura - 12, "dir", "Estatisticas")
        else:
            self._desenhar_seta(cad_x + cad_largura-2, cad_y + cad_altura - 12, "dir", "Continuar")
