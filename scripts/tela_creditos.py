import pyxel




class TelaCreditos:
    def __init__(self):
        # Botão voltar
        self.btn_x, self.btn_y, self.btn_w, self.btn_h = 118, 106, 38, 10
        pyxel.images[1].load(0, 0, "Creditos.png")

    def _clique_voltar(self):
        return (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
                and self.btn_x <= pyxel.mouse_x <= self.btn_x + self.btn_w
                and self.btn_y <= pyxel.mouse_y <= self.btn_y + self.btn_h)

    def _desenhar_botao_voltar(self):
        hover = (self.btn_x <= pyxel.mouse_x <= self.btn_x + self.btn_w
                 and self.btn_y <= pyxel.mouse_y <= self.btn_y + self.btn_h)
        pyxel.rect(self.btn_x, self.btn_y, self.btn_w, self.btn_h, 5 if hover else 1)
        pyxel.text(self.btn_x + 7, self.btn_y + 3, "Voltar", 7)

    def _texto_centralizado(self, y, texto, cor):
        pyxel.text((160 - len(texto) * 4) // 2, y, texto, cor)

    def update(self):
        if self._clique_voltar() or pyxel.btnp(pyxel.KEY_ESCAPE):
            return "Menu Inicial"
        return "Creditos"

    def draw(self):
        pyxel.cls(1)

        self._texto_centralizado(4, "CREDITOS", 10)

        # Rostos 40x40 (banco 1): Rafael em u=0, Daniel em u=40
        pyxel.blt(18, 18, 1, 0, 0, 44, 44)
        pyxel.blt(98, 18, 1, 44, 0, 44, 44)

        pyxel.text(40 - len("Rafael Prescendo") * 4 // 2, 66, "Rafael Prescendo", 7)
        pyxel.text(40 - len("Dev") * 4 // 2, 72, "Dev", 13)

        pyxel.text(120 - len("Daniel D. Wiesel") * 4 // 2, 66, "Daniel D. Wiesel", 7)
        pyxel.text(120 - len("Dev") * 4 // 2, 72, "Dev", 13)

        self._texto_centralizado(85, "FURG - 2026", 7)
        self._texto_centralizado(94, "Obrigado por jogar!", 10)

        self._desenhar_botao_voltar()

