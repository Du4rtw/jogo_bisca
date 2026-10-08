"""
estatisticas.py
---------------
Gerencia, salva e calcula as estatisticas do Player 1 no jogo de bisca.

- NAO importa pyxel nem jogo_bisca.py (evita import circular e permite testar sozinho).
- O JSON guarda apenas SOMAS BRUTAS (contadores). As taxas/medias sao calculadas na
  hora de mostrar (funcoes calc_*).
- Durante o raio tudo fica em memoria (SessaoEstatisticas). O arquivo so e gravado
  UMA vez por raio, quando ele termina -> zero acesso a disco durante a partida.
"""
import json
import os

ARQUIVO_ESTATISTICAS = "estatisticas.json"
DEBUG_ESTATISTICAS = True   # True = escreve no console o que foi registrado (ponha False quando nao precisar)

# ---------------------------------------------------------------------------
# AJUSTES (mexa aqui para calibrar as estatisticas)
# ---------------------------------------------------------------------------
PESO_TRUNFO = 2    # carta do naipe da bisca vale (valor * PESO_TRUNFO) na conta da sorte
BONUS_TRUNFO = 0   # pontos extras fixos por trunfo recebido (0 = desligado). Use se quiser que
                   # trunfos de 0 pontos (2, 3, 4...) tambem contem como sorte.


def valor_estrategico_trunfo(carta):
    """Quanto 'custa' gastar esta carta de trunfo. Hoje = forca da carta.
    Troque aqui se quiser outra definicao (ex.: forca + valor)."""
    return int(carta["forca"])


def pontos_sorte(carta, naipe_bisca):
    """Quanto de 'sorte' vale receber esta carta."""
    valor = int(carta["valor"])
    if carta["naipe"] == naipe_bisca:
        return valor * PESO_TRUNFO + BONUS_TRUNFO
    return valor


# ---------------------------------------------------------------------------
# Persistencia
# ---------------------------------------------------------------------------
DADOS_PADRAO = {
    # Partidas
    "partidas_ganhas": 0,
    "partidas_totais": 0,
    # Raios
    "raios_ganhos": 0,
    "raios_totais": 0,
    "pontos_totais_raios": 0,        # SOMA da pontuacao final (0 a 120) de cada raio. Media = isso / raios_totais
    # Eficiencia de trunfos
    "trunfos_jogados_total": 0,
    "pontos_capturados_trunfos": 0,
    "valor_estrategico_trunfos": 0.0,
    # Dominio da mesa
    "maior_combo": 0,
    "vazas_com_iniciativa": 0,       # vazas em que o P1 estava "com a mao" (jogou primeiro)
    "vazas_mantidas": 0,             # dessas, quantas ele venceu (manteve o controle)
}


def carregar_estatisticas():
    """Carrega o JSON. Se nao existir (ou estiver corrompido), devolve o padrao.
    Chaves novas adicionadas no futuro sao completadas automaticamente."""
    if not os.path.exists(ARQUIVO_ESTATISTICAS):
        salvar_estatisticas(DADOS_PADRAO)
        return DADOS_PADRAO.copy()

    try:
        with open(ARQUIVO_ESTATISTICAS, "r", encoding="utf-8") as f:
            salvos = json.load(f)
        return {**DADOS_PADRAO, **salvos}
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return DADOS_PADRAO.copy()


def salvar_estatisticas(dados):
    """Salva o dicionario no JSON (escreve num temporario e troca, para nao corromper)."""
    try:
        tmp = ARQUIVO_ESTATISTICAS + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        os.replace(tmp, ARQUIVO_ESTATISTICAS)
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")


# ---------------------------------------------------------------------------
# Calculos (recebem o dict de dados e devolvem numeros prontos)
# ---------------------------------------------------------------------------
def _percentual(parte, total):
    return (parte / total * 100.0) if total > 0 else 0.0


def calc_taxa_partidas(dados):
    return _percentual(dados["partidas_ganhas"], dados["partidas_totais"])


def calc_taxa_raios(dados):
    return _percentual(dados["raios_ganhos"], dados["raios_totais"])


def calc_media_pontos_raio(dados):
    return dados["pontos_totais_raios"] / dados["raios_totais"] if dados["raios_totais"] > 0 else 0.0


def calc_eficiencia_trunfos(dados):
    """Pontos capturados nas vazas em que jogou trunfo / valor estrategico gasto."""
    custo = dados["valor_estrategico_trunfos"]
    return dados["pontos_capturados_trunfos"] / custo if custo > 0 else 0.0


def calc_disputa(sorte_p1, sorte_bot):
    """Divide 100% entre P1 e Bot a partir dos pesos de sorte. Sem dados = 50/50."""
    total = sorte_p1 + sorte_bot
    if total <= 0:
        return 50.0, 50.0
    pct_p1 = sorte_p1 / total * 100.0
    return pct_p1, 100.0 - pct_p1


def calc_controle_mesa(dados):
    """% das vazas em que o P1 jogou primeiro e venceu (manteve o controle)."""
    return _percentual(dados["vazas_mantidas"], dados["vazas_com_iniciativa"])


def resumo(dados, sorte_partida=(50.0, 50.0)):
    """Tudo que a tela precisa, ja calculado. A tela so formata e desenha.
    `sorte_partida` = (% P1, % Bot) vindo da sessao (e AO VIVO, nao vem do JSON)."""
    sorte_p1, sorte_bot = sorte_partida
    return {
        "partidas_ganhas": dados["partidas_ganhas"],
        "partidas_totais": dados["partidas_totais"],
        "taxa_partidas": calc_taxa_partidas(dados),

        "raios_ganhos": dados["raios_ganhos"],
        "raios_totais": dados["raios_totais"],
        "taxa_raios": calc_taxa_raios(dados),
        "media_pontos_raio": calc_media_pontos_raio(dados),

        "eficiencia_trunfos": calc_eficiencia_trunfos(dados),
        "trunfos_jogados": dados["trunfos_jogados_total"],

        "sorte_p1": sorte_p1,
        "sorte_bot": sorte_bot,

        "maior_combo": dados["maior_combo"],
        "controle_mesa": calc_controle_mesa(dados),
    }


# ---------------------------------------------------------------------------
# Sessao: acumula em memoria durante o raio e grava no fim
# ---------------------------------------------------------------------------
class SessaoEstatisticas:
    def __init__(self):
        # sorte acumulada dos raios JA TERMINADOS da partida atual (nao vai pro JSON)
        self._sorte_partida_p1 = 0
        self._sorte_partida_bot = 0
        self._partida_encerrada = False
        self.iniciar_raio()

    def iniciar_raio(self, baralho_completo=None, naipe_bisca=None):
        """Zera os acumuladores do raio e guarda o baralho do raio (a lista com as 40 cartas).
        Como os dicionarios das cartas sao os mesmos do jogo, a marca "jogador" que o jogo
        coloca em cada carta ao distribuir ja aparece aqui, ao vivo."""
        self._baralho = baralho_completo
        self._naipe_bisca = naipe_bisca
        self._trunfos_jogados = 0
        self._pontos_capt_trunfos = 0
        self._valor_estrategico = 0.0
        self._combo_atual = 0
        self._maior_combo = 0
        self._vazas_iniciativa = 0
        self._vazas_mantidas = 0

    def iniciar_partida(self):
        """Chamar quando uma PARTIDA NOVA comecar: zera a sorte da partida."""
        self._sorte_partida_p1 = 0
        self._sorte_partida_bot = 0
        self._partida_encerrada = False

    # ---- eventos durante o raio (so memoria, sem disco) ----
    def registrar_vaza(self, jogador_inicial, carta_inicial, carta_secundaria,
                       vencedor, naipe_bisca, pontos_mesa):
        """Chamar uma vez por vaza, logo apos descobrir o vencedor."""
        p1_iniciou = (jogador_inicial == 1)
        carta_p1 = carta_inicial if p1_iniciou else carta_secundaria
        p1_venceu = (vencedor == 1)

        # Eficiencia de trunfos
        if carta_p1["naipe"] == naipe_bisca:
            self._trunfos_jogados += 1
            self._valor_estrategico += valor_estrategico_trunfo(carta_p1)
            if p1_venceu:
                self._pontos_capt_trunfos += int(pontos_mesa)

        # Dominio da mesa
        if p1_iniciou:
            self._vazas_iniciativa += 1
            if p1_venceu:
                self._vazas_mantidas += 1

        if p1_venceu:
            self._combo_atual += 1
            self._maior_combo = max(self._maior_combo, self._combo_atual)
        else:
            self._combo_atual = 0

    # ---- sorte (ao vivo) ----
    def _sorte_do_raio(self):
        """Pesos de sorte do raio atual, olhando as cartas JA distribuidas ate agora."""
        p1 = bot = 0
        if self._baralho:
            for carta in self._baralho:
                if carta["jogador"] == "1":
                    p1 += pontos_sorte(carta, self._naipe_bisca)
                elif carta["jogador"] == "2":
                    bot += pontos_sorte(carta, self._naipe_bisca)
        return p1, bot

    def sorte_partida(self):
        """(% P1, % Bot) da partida atual: raios terminados + cartas ja distribuidas do raio atual."""
        p1, bot = self._sorte_partida_p1, self._sorte_partida_bot
        if not self._partida_encerrada:      # depois do fim da partida o jogo ja sorteia um raio
            raio_p1, raio_bot = self._sorte_do_raio()   # "fantasma": nao pode contar
            p1 += raio_p1
            bot += raio_bot
        return calc_disputa(p1, bot)

    # ---- fim do raio: consolida tudo e grava UMA vez ----
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

        dados["trunfos_jogados_total"] += self._trunfos_jogados
        dados["pontos_capturados_trunfos"] += self._pontos_capt_trunfos
        dados["valor_estrategico_trunfos"] += self._valor_estrategico

        dados["maior_combo"] = max(dados["maior_combo"], self._maior_combo)
        dados["vazas_com_iniciativa"] += self._vazas_iniciativa
        dados["vazas_mantidas"] += self._vazas_mantidas

        salvar_estatisticas(dados)
        if DEBUG_ESTATISTICAS:
            n = len(self._baralho) if self._baralho else 0
            print(f"[estat] raio fechado: cartas na lista={n} sorte do raio P1={raio_p1} Bot={raio_bot} "
                  f"| partida P1={self._sorte_partida_p1} Bot={self._sorte_partida_bot}")
            print(f"[estat] gravado em: {os.path.abspath(ARQUIVO_ESTATISTICAS)}")
        return dados