import pyxel
from .musicas import VOLUME, VELOCIDADE, FRASES, MELODIA, BAIXO


class GerenciadorAudio:

    def __init__(self):
        self.mudo = False
        slots = {}
        for i, nome in enumerate(FRASES):
            p = FRASES[nome]
            pyxel.sounds[i].set(p["notes"].replace(" ", ""),
                                p["tone"], p["vol"], p["fx"], VELOCIDADE)
            slots[nome] = i
        pyxel.musics[0].set([slots[n] for n in MELODIA],
                            [slots[n] for n in BAIXO], [], [])
        pyxel.playm(0, loop=True)
        self._volume()

    def _volume(self):
        for ch in (0, 1):
            pyxel.channels[ch].gain = 0.0 if self.mudo else VOLUME

    def atualizar(self):
        if pyxel.btnp(pyxel.KEY_M):
            self.mudo = not self.mudo
            self._volume()

    def desenhar(self):
        pyxel.rect(2, 5, 3, 3, 7)                 # corpo do alto-falante
        pyxel.tri(5, 5, 9, 2, 9, 10, 7)            # cone
        pyxel.tri(5, 5, 5, 7, 9, 10, 7)
        pyxel.text(13,4,'[M] - MUT.',7)
        if self.mudo:
            pyxel.line(1, 2, 11, 9, 8)            # risco vermelho
        else:
            pyxel.line(11, 5, 11, 7, 7)           # ondas de som