import pyxel

class MenuInicial:
    def __init__(self):
        pass

    RODAPE_TEXTO = "(c) R. Prescendo & D. Wiesel"
    RODAPE_Y = 111

    def _mouse_no_rodape(self):
        return pyxel.mouse_y >= self.RODAPE_Y - 2  

    def _verificar_clique_rodape(self):
        return pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self._mouse_no_rodape()

    def _desenhar_rodape(self):
        largura = len(self.RODAPE_TEXTO) * 4          
        x = (160 - largura) // 2
        pyxel.text(x, self.RODAPE_Y, self.RODAPE_TEXTO, 7)



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
        if self._verificar_clique_rodape():
            return "Creditos"
        else:
            return "Menu Inicial"


            
    def draw(self):
        pyxel.cls(4)
        self._desenhar_titulo_bisca(66,25)
        self._botao_jogar()
        self._desenhar_rodape()


