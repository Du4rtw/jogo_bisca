import json
import os

ARQUIVO_ESTATISTICAS = "estatisticas.json"

PESO_BISCA = 2    # valor * PESO_BISCA, sortometro
BONUS_BISCA = 2   # biscas valor 0 valem isso de pontos

def pontos_sorte(carta, naipe_bisca):
    # Faz a equivalencia de sorte por valor
    valor = int(carta["valor"])
    if carta["naipe"] == naipe_bisca:
        return valor * PESO_BISCA + BONUS_BISCA
    return valor

#Modelo base
DADOS_PADRAO = {
    # Partidas
    "partidas_ganhas": 0,
    "partidas_totais": 0,

    # Raios
    "raios_ganhos": 0,
    "raios_totais": 0,
    "pontos_totais_raios": 0,  # SOMA da pontuacao final (0 a 120) de cada raio. Media = acumulador / raios_totais
                
    # Eficiencia de biscas
    "biscas_jogados_total": 0,
    "pontos_capturados_biscas": 0,
    "valor_estrategico_biscas": 0.0,

    # Dominio da mesa
    "maior_combo": 0,
    "pontos_maior_combo": 0,
}


def carregar_estatisticas():
    if not os.path.exists(ARQUIVO_ESTATISTICAS):
        salvar_estatisticas(DADOS_PADRAO)
        return DADOS_PADRAO.copy()

    try:
        with open(ARQUIVO_ESTATISTICAS, "r", encoding="utf-8") as f:
            salvos = json.load(f)
        return {**DADOS_PADRAO, **salvos} #Fusão do padrão com o que foi salvo
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return DADOS_PADRAO.copy()


def salvar_estatisticas(dados):
    # Salva o dicionario no JSON
    # Usa o tmp(arquivo temporario) e depois susbstitui com os.replace, evitando corromper caso jogo feche
    try:
        tmp = ARQUIVO_ESTATISTICAS + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        os.replace(tmp, ARQUIVO_ESTATISTICAS)
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")


#CAlCULOS
def _percentual(parte, total):
    # Evita dividir por zero
    return (parte / total * 100.0) if total > 0 else 0.0

def calc_taxa_partidas(dados):
    return _percentual(dados["partidas_ganhas"], dados["partidas_totais"])

def calc_taxa_raios(dados):
    return _percentual(dados["raios_ganhos"], dados["raios_totais"])

def calc_media_pontos_raio(dados):
    return dados["pontos_totais_raios"] / dados["raios_totais"] if dados["raios_totais"] > 0 else 0.0

def calc_eficiencia_biscas(dados):
    # Pontos capturados nas vazas em que jogou bisca / valor estrategico gasto
    custo = dados["valor_estrategico_biscas"]
    return dados["pontos_capturados_biscas"] / custo if custo > 0 else 0.0

def calc_disputa(sorte_p1, sorte_bot):
    #  Divide 100% entre P1 e Bot
    total = sorte_p1 + sorte_bot
    if total <= 0:
        return 50.0, 50.0
    pct_p1 = sorte_p1 / total * 100.0
    return pct_p1, 100.0 - pct_p1



#Função que prepara para a tela mostrar
def resumo(dados, sorte_partida=(50.0, 50.0)):
    # Atualização chamada do tela_est
    sorte_p1, sorte_bot = sorte_partida
    return {
        "partidas_ganhas": dados["partidas_ganhas"],
        "partidas_totais": dados["partidas_totais"],
        "taxa_partidas": calc_taxa_partidas(dados),

        "raios_ganhos": dados["raios_ganhos"],
        "raios_totais": dados["raios_totais"],
        "taxa_raios": calc_taxa_raios(dados),
        "media_pontos_raio": calc_media_pontos_raio(dados),

        "eficiencia_biscas": calc_eficiencia_biscas(dados),
        "biscas_jogados": dados["biscas_jogados_total"],

        "sorte_p1": sorte_p1,
        "sorte_bot": sorte_bot,

        "maior_combo": dados["maior_combo"],
        "pontos_maior_combo": dados["pontos_maior_combo"],
    }


class SessaoEstatisticas:
    def __init__(self):
        self._sorte_partida_p1 = 0
        self._sorte_partida_bot = 0
        self._partida_encerrada = False
        self.iniciar_raio()

    def iniciar_raio(self, baralho_completo=None, naipe_bisca=None):
        #Zera os acumuladores 
        self._baralho = baralho_completo
        self._naipe_bisca = naipe_bisca
        self._biscas_jogados = 0
        self._pontos_capt_biscas = 0
        self._valor_estrategico = 0.0
        self._combo_atual = 0
        self._pontos_combo_atual = 0
        self._maior_combo = 0
        self._pontos_maior_combo = 0


    def registrar_vaza(self, jogador_inicial, carta_inicial, carta_secundaria, vencedor, naipe_bisca, pontos_mesa):
        #Identificas se p1 jogou a primeira
        carta_p1 = carta_inicial if jogador_inicial == 1 else carta_secundaria
        p1_venceu = (vencedor == 1)

        # Eficiencia de biscas
        if carta_p1["naipe"] == naipe_bisca:
            self._biscas_jogados += 1
            self._valor_estrategico += int(carta_p1["forca"]) #transforma em um int de força
            if p1_venceu:
                self._pontos_capt_biscas += int(pontos_mesa)

        # Combo: vazas e pontos somatoria
        if p1_venceu:
            self._combo_atual += 1
            self._pontos_combo_atual += int(pontos_mesa)
            # recorde = mais vazas; em empate de vazas, o que fez mais pontos como funciona??
            if (self._combo_atual, self._pontos_combo_atual) > (self._maior_combo, self._pontos_maior_combo):
                self._maior_combo = self._combo_atual
                self._pontos_maior_combo = self._pontos_combo_atual
        else:
            self._combo_atual = 0
            self._pontos_combo_atual = 0

    # Sortometro
    def _sorte_do_raio(self):
        # Olha so as cartas ja distribuidas
        p1 = 0
        bot = 0
        if self._baralho:
            for carta in self._baralho:
                if carta["jogador"] == "1":
                    p1 += pontos_sorte(carta, self._naipe_bisca)
                elif carta["jogador"] == "2":
                    bot += pontos_sorte(carta, self._naipe_bisca)
        return p1, bot

    def sorte_partida(self):
        p1, bot = self._sorte_partida_p1, self._sorte_partida_bot
        if not self._partida_encerrada:      # depois do fim da partida o jogo ja sorteia um raio
            raio_p1, raio_bot = self._sorte_do_raio()   # "fantasma": nao pode contar
            p1 += raio_p1
            bot += raio_bot
        return calc_disputa(p1, bot)

    # fim do raio: consolida tudo e grava
    def finalizar_raio(self, pontos_j1, pontos_j2, fim_partida=False, venceu_partida=False):
        # a sorte do raio que acabou entra na sorte da partida (em memoria)
        raio_p1, raio_bot = self._sorte_do_raio()
        self._sorte_partida_p1 += raio_p1
        self._sorte_partida_bot += raio_bot
        if fim_partida:
            self._partida_encerrada = True

        dados = carregar_estatisticas()

        dados["raios_totais"] += 1
        dados["pontos_totais_raios"] += int(pontos_j1)
        if pontos_j1 > pontos_j2:
            dados["raios_ganhos"] += 1

        if fim_partida:
            dados["partidas_totais"] += 1
            if venceu_partida:
                dados["partidas_ganhas"] += 1

        dados["biscas_jogados_total"] += self._biscas_jogados
        dados["pontos_capturados_biscas"] += self._pontos_capt_biscas
        dados["valor_estrategico_biscas"] += self._valor_estrategico

        if self._maior_combo > dados["maior_combo"]: # Maior a quantidade de combo
            dados["maior_combo"] = self._maior_combo
            dados["pontos_maior_combo"] = self._pontos_maior_combo
        elif self._maior_combo == dados["maior_combo"]: # Igual mas mais pontos
            if self._pontos_maior_combo > dados["pontos_maior_combo"]:
                dados["pontos_maior_combo"] = self._pontos_maior_combo

        salvar_estatisticas(dados)
