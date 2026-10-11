# 🃏 Jogo de Bisca

## Sobre o jogo
A bisca é um jogo de cartas tradicional, muito jogado em mesas de bar, botecos e rodas de amigos, no qual dois jogadores disputam vazas com um baralho de 40 cartas. Em cada vaza, cada jogador joga uma carta e quem vence leva os pontos das duas. Este projeto leva essa partida de mesa para o computador: você enfrenta um Bot em uma mesa redonda de feltro verde, arrastando as cartas com o mouse.

## Origem
A bisca pertence à família dos jogos de vazas com naipe de trunfo e tem raízes europeias. Ela é parente próxima da brisca, espanhola, e da briscola, italiana, e também é conhecida em Portugal. O jogo chegou ao Brasil com os imigrantes europeus, principalmente portugueses e italianos, e se espalhou por mesas familiares e de bar.

Ainda hoje a bisca é jogada em algumas regiões típicas do sul do Brasil, onde faz parte da tradição de passar o tempo com os amigos em volta de uma mesa, entre uma rodada e outra de conversa.

---

## Como jogar

### Guia rápido
1. Cada jogador começa com 3 cartas. Uma carta virada na mesa define o naipe da bisca, o mais forte do raio.
2. Quem começa joga uma carta e o outro responde com uma carta da própria mão.
3. Ganha a vaza quem jogou a carta mais forte (veja as regras abaixo) e leva os pontos das duas cartas.
4. Quem venceu compra primeiro, depois o outro compra, e o vencedor abre a próxima jogada.
5. Quando o baralho e as mãos acabam, o raio termina. Quem tiver mais de 60 pontos ganha o raio.
6. Vence a partida quem fizer 4 raios primeiro.

### Objetivo
Uma partida é uma disputa para ver quem faz quatro raios primeiro. Um raio é uma rodada completa, que termina quando o baralho e as mãos acabam. Ganha o raio quem somar mais pontos nas cartas que capturou.

### Preparação
- O baralho espanhol tem 40 cartas, em quatro naipes (cada naipe tem Ás, 2, 3, 4, 5, 6, 7, Fante, Cavalo e Rei), e é embaralhado a cada raio.
- Cada jogador recebe 3 cartas na mão.
- A última carta do monte é virada e fica na mesa, na horizontal, ao lado do monte. Ela é a bisca, e o naipe dela é o naipe de maior poder naquele raio.
- Quem começa o raio é sorteado.

### Como funciona uma jogada
1. Quem começa joga uma carta na mesa.
2. O outro jogador responde com uma carta da própria mão.
3. As duas cartas são comparadas e o vencedor leva os pontos das duas.
4. O vencedor compra primeiro do monte, o outro compra em seguida, e o vencedor começa a próxima jogada.
5. Isso se repete por 20 jogadas, até acabarem o monte e as mãos.

### Quem vence a jogada
- **Mesmo naipe:** vence a carta de maior ordem.
- **Naipes diferentes, e a segunda carta é bisca:** a bisca vence.
- **Naipes diferentes, sem bisca na resposta:** vence quem jogou primeiro.

> **Nota:** Não é obrigatório responder com o mesmo naipe, então jogar uma carta fraca para não gastar uma boa é parte da estratégia.

### Ordem das cartas (da mais forte para a mais fraca)
**Ás > 3 > Rei (12) > Cavalo (11) > Fante (10) > 7 > 6 > 5 > 4 > 2**

### Pontuação

| Carta | Pontos |
| :--- | :--- |
| Ás | 11 |
| 3 | 10 |
| Rei | 4 |
| Cavalo | 3 |
| Fante | 2 |
| Demais cartas (7, 6, 5, 4 e 2) | 0 |

Cada naipe soma 30 pontos, então há 120 pontos em jogo por raio. Quem fizer mais de 60 ganha o raio. Se houver empate em 60 a 60, o raio não conta para ninguém.

---

## Controles

| Controle | O que faz |
| :--- | :--- |
| **Mouse** | Clique em "Jogar" no menu. Na mesa, arraste uma carta da sua mão até o lugar central da mesa, onde há uma área piscante, para jogá-la. |
| **Tecla E** | Abre e fecha a tela de estatísticas. Só funciona quando você está na tela da mesa e não há nenhuma carta na mesa. |
| **Tecla M** | Muta e desmuta o som. Só funciona na tela da mesa. |

---

## STEAM
 
A disciplina de Algoritmos e Estruturas de Dados I da FURG propôs o desenvolvimento de um jogo como trabalho, utilizando a biblioteca Pyxel. O jogo deve, obrigatoriamente, integrar conceitos relacionados a STEAM (*Science, Technology, Engineering, Arts and Mathematics*). A seguir, como isso foi feito neste projeto.
 
### Ciência e Matemática: estatísticas e probabilidade
O jogo guarda o seu histórico em um arquivo e transforma esses números em uma tela de estatísticas, inspirada em uma caderneta de anotações:
 
- partidas e raios ganhos, com a taxa de aproveitamento;
- média de pontos por raio;
- eficiência das biscas, calculada pela fórmula: **eficiência = pontos capturados nas vazas em que você jogou bisca ÷ soma da força das biscas jogadas**. Quanto maior o valor, mais pontos cada bisca gasta rendeu;
- sortômetro, que compara quão fortes foram as cartas que cada lado recebeu e mostra o quanto da partida foi sorte e o quanto foi decisão;
- maior combo de vazas seguidas vencidas e sua respectiva pontuação.
Isso trabalha porcentagens, razões, médias e probabilidade. A bisca é um jogo de memória, estratégia e sorte: a sorte decide as cartas distribuídas, mas lembrar quais cartas já saíram, calcular a chance de o adversário ter uma carta forte e decidir quando vale gastar uma bisca dependem de pensamento crítico e de uma leitura probabilística do jogo. As estatísticas ajudam o jogador a enxergar o efeito de suas próprias escolhas.
 
### Tecnologia e Engenharia: a lógica de decisão do Bot
O Bot não joga ao acaso. Ele segue regras de decisão que imitam o raciocínio de um jogador de bisca:
 
- **Jogando primeiro:** ele abre com uma carta "segura" (fraca e sem ser bisca) e só gasta bisca se não tiver outra opção.
- **Jogando em segundo:**
  - se você jogou bisca, ele descarta algo barato em vez de gastar uma carta forte;
  - se dá para vencer com o mesmo naipe, ele vence com a menor carta capaz disso;
  - se você jogou uma carta valiosa que ele não consegue vencer de outra forma, ele usa a menor bisca que tiver;
  - caso contrário, ele descarta a carta de menor valor.
Ou seja, o Bot avalia o risco, o custo de cada carta e o que vale a pena gastar em cada vaza.
 
### Arte: baralho espanhol e estética de boteco
- As cartas se inspiram no baralho espanhol, com quatro naipes e figuras, e os sprites foram desenhados em pixel art.
- O cenário lembra uma mesa de bar: mesa redonda com borda de madeira e feltro verde, uma caderneta de espiral onde os raios são marcados em riscos (como a contagem de pontos num boteco), e um lápis ao lado.