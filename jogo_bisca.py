import pyxel

class MenuInicial:
    def __init__(self):
        

        pass

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if 60<=pyxel.mouse_x<=100 and 60<=pyxel.mouse_y<=70:
                return "Jogar"
            


        return "Menu Inicial"

    def draw(self):
        pyxel.cls(4)
        pyxel.rect(60,60, 40,10, 4)
        pyxel.text(70,62,"Jogar",7)
        

class Jogar:
    def __init__(self):
        # Configurações da mesa redonda (Círculo Perfeito)
        self.centro_x = 80
        self.centro_y = 60
        self.raio_externo = 53  # Diâmetro de 106px
        self.espessura_borda = 4

    def update(self):
        return "Jogar"

    def draw(self):
        pyxel.cls(3)  # Fundo verde escuro (feltro externo/cenário)

        # 1. Borda externa de madeira (Círculo maior)
        pyxel.circ(self.centro_x, self.centro_y, self.raio_externo, 4)        # Madeira (Castanho)
        pyxel.circb(self.centro_x, self.centro_y, self.raio_externo, 0)       # Contorno externo preto

        # 2. Feltro interno da mesa (Círculo menor)
        raio_interno = self.raio_externo - self.espessura_borda
        pyxel.circ(self.centro_x, self.centro_y, raio_interno, 11)           # Feltro Verde Claro
        pyxel.circb(self.centro_x, self.centro_y, raio_interno, 3)            # Contorno interno verde escuro

       
        
        
        

class JogoBisca:
    def __init__(self):
        pyxel.init(160, 120, title="Bisca")
        pyxel.fullscreen(True) 
        pyxel.mouse(True) # Mostra o mouse na tela do jogo
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

        

       


