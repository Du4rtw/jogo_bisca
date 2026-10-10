import pyxel
import estatisticas

COR_FUNDO = 3
COR_PAPEL = 7
COR_SOMBRA = 5
COR_TITULO = 0
COR_CABECALHO = 5
COR_LINHA = 6
COR_LABEL = 1
COR_VALOR = 0
COR_ARGOLA = 13
COR_ARGOLA_BRILHO = 7
COR_P1 = 12
COR_BOT = 8

# caderneta
CAD_X, CAD_Y, CAD_W, CAD_H = 8, 14, 144, 94
ESQ_X0, ESQ_X1 = 15, 76     # bloco esquerdo (invisivel)
DIR_X0, DIR_X1 = 84, 145    # bloco direito (invisivel)
Y_INICIO = 30
PASSO = 6                   # altura de cada linha de texto
GAP = 5                     # espaco entre secoes

# Botao de voltar
VOLTAR_X, VOLTAR_Y, VOLTAR_W, VOLTAR_H = 8, 113, 44, 7


class TelaEstatisticas:
    def __init__(self, voltar_para="Jogar", sessao=None):
        self.voltar_para = voltar_para
        sorte = sessao.sorte_partida() if sessao else (50.0, 50.0) # Espressão  condicional : valor_se_verdadeiro if condicao else valor_se_falso
        self.resumo = estatisticas.resumo(estatisticas.carregar_estatisticas(), sorte)

    def _clicou_voltar(self):
        return (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
                and VOLTAR_X <= pyxel.mouse_x <= VOLTAR_X + VOLTAR_W
                and VOLTAR_Y <= pyxel.mouse_y <= VOLTAR_Y + VOLTAR_H)



    def update(self):
        if pyxel.btnp(pyxel.KEY_E) or self._clicou_voltar(): # Tecla E ou metodo clicou
            return self.voltar_para
        return "Estatisticas"

    def _cabecalho(self, x0, x1, y, texto):
        pyxel.text(x0, y, texto, COR_CABECALHO)
        pyxel.line(x0, y + 6, x1, y + 6, COR_LINHA)

    def _linha(self, x0, x1, y, rotulo, valor, cor_valor=COR_VALOR):
        # Rotulo alinhado a esquerda, valor alinhado a direita do bloco
        pyxel.text(x0, y, rotulo, COR_LABEL)
        pyxel.text(x1 - len(valor) * 4, y, valor, cor_valor) # Fonte padrão ocupa 4 pixels

    def _bloco_esquerdo(self):
        x0 = ESQ_X0
        x1 = ESQ_X1
        y = Y_INICIO

        self._cabecalho(x0, x1, y, "PARTIDAS")
        y += PASSO + 2
        self._linha(x0, x1, y, "Ganhas", f"{self.resumo["partidas_ganhas"]}/{self.resumo["partidas_totais"]}")
        y += PASSO
        self._linha(x0, x1, y, "Aproveit.", f"{self.resumo["taxa_partidas"]:.0f}%")

        y += PASSO + GAP
        self._cabecalho(x0, x1, y, "RAIOS")
        y += PASSO + 2
        self._linha(x0, x1, y, "Ganhos", f"{self.resumo["raios_ganhos"]}/{self.resumo["raios_totais"]}")
        y += PASSO
        self._linha(x0, x1, y, "Aproveit.", f"{self.resumo["taxa_raios"]:.0f}%")
        y += PASSO
        self._linha(x0, x1, y, "Media pts", f"{self.resumo["media_pontos_raio"]:.1f}")

    def _bloco_direito(self):
        x0 = DIR_X0
        x1 = DIR_X1
        y = Y_INICIO

        self._cabecalho(x0, x1, y, "EFIC. BISCAS")
        y += PASSO + 2
        self._linha(x0, x1, y, "Razao", f"{self.resumo["eficiencia_biscas"]:.2f}")
        y += PASSO
        self._linha(x0, x1, y, "Jogados", str(self.resumo["biscas_jogados"]))

        y += PASSO + GAP
        self._cabecalho(x0, x1, y, "SORTOMETRO")
        y += PASSO + 2
        self._linha(x0, x1, y, "Voce", f"{self.resumo["sorte_p1"]:.0f}%", COR_P1)
        y += PASSO
        self._linha(x0, x1, y, "Bot", f"{self.resumo["sorte_bot"]:.0f}%", COR_BOT)
        y += PASSO
        # barra de disputa
        largura = x1 - x0
        larg_p1 = round(largura * self.resumo["sorte_p1"] / 100.0) # multiplica a porcentagem pela distancia total
        pyxel.rect(x0, y + 1, largura, 3, COR_BOT) # retangulo vermelho ocupando tudo
        pyxel.rect(x0, y + 1, larg_p1, 3, COR_P1) # sobreposição com o azul

        y += PASSO + GAP
        self._cabecalho(x0, x1, y, "DOMINIO DA MESA")
        y += PASSO + 2
        self._linha(x0, x1, y, "Maior combo", str(self.resumo["maior_combo"]))
        y += PASSO
        self._linha(x0, x1, y, "Pts Combo", str(self.resumo["pontos_maior_combo"]))

    def _desenhar_fundo(self):
        pyxel.cls(COR_FUNDO)
        # mesa redonda aparecendo atras da caderneta
        pyxel.circ(80, 60, 53, 4)
        pyxel.circb(80, 60, 53, 0)
        pyxel.circ(80, 60, 49, 11)
        pyxel.circb(80, 60, 49, 3)

    def _desenhar_caderneta(self):
        pyxel.rect(CAD_X + 3, CAD_Y + 3, CAD_W, CAD_H, COR_SOMBRA)   # sombra
        pyxel.rect(CAD_X, CAD_Y, CAD_W, CAD_H, COR_PAPEL)            # folha

        # espiral
        for x in range(CAD_X + 8, CAD_X + CAD_W - 4, 8):
            pyxel.rect(x - 1, CAD_Y + 2, 3, 2, COR_LABEL)            # furo
            pyxel.circb(x, CAD_Y, 2, COR_ARGOLA)                     # argola
            pyxel.pset(x, CAD_Y - 2, COR_ARGOLA_BRILHO)              # brilho

        titulo = "ESTATISTICAS"
        tx = CAD_X + CAD_W // 2 - len(titulo) * 4 // 2
        pyxel.text(tx, CAD_Y + 8, titulo, COR_TITULO)

    def _desenhar_lapis(self):
        for o in range(4):
            pyxel.line(136 + o, 116, 152 + o, 100, 10)
        pyxel.line(136, 116, 152, 100, 9)
        pyxel.line(139, 116, 155, 100, 9)
        for o in range(4):
            pyxel.line(152 + o, 100, 154 + o, 98, 14)
        pyxel.tri(136, 116, 139, 116, 133, 119, 15)
        pyxel.pset(133, 119, 0)

    def _desenhar_voltar(self):
        pyxel.text(VOLTAR_X, VOLTAR_Y + 1, "[E] Voltar", 7)



    def draw(self):
        self._desenhar_fundo()
        self._desenhar_caderneta()
        self._bloco_esquerdo()
        self._bloco_direito()
        self._desenhar_lapis()
        self._desenhar_voltar()