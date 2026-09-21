# ⛏️ Caverna Craft

Um jogo de exploração e mineração para terminal, feito em Python puro — sem nenhuma biblioteca externa.

O jogador desce por três minas cada vez maiores, quebra pedras em busca da escada escondida e enfrenta os monstros que aparecem no caminho. Cada mina é gerada aleatoriamente, então nenhuma partida é igual à anterior.

O projeto foi construído em cima dos conteúdos da disciplina: **funções, listas, tuplas, matrizes e dicionários**.

---

## 👥 Equipe

| Nome | RM |
|------|----|
| *a preencher* | *a preencher* |
| *a preencher* | *a preencher* |
| *a preencher* | *a preencher* |
| *a preencher* | *a preencher* |

**Curso:** Análise e Desenvolvimento de Sistemas — 2º semestre

---

## 🎮 Como rodar

**Requisito:** Python 3.10 ou superior.

> O jogo usa a estrutura `match / case`, que só existe a partir do Python 3.10. Em versões anteriores o programa não abre.

**Terminal:** o mapa é desenhado com emoji, então é preciso um terminal com suporte a Unicode — Windows Terminal, PowerShell, o terminal do VS Code ou qualquer terminal Linux/macOS. O próprio `main.py` já força a saída em UTF-8, então o jogo não quebra por causa de acentuação.

```bash
python main.py
```

Não há nada para instalar: o jogo usa apenas o módulo `random`, que já vem com o Python.

---

## 🕹️ Controles

| Tecla | Ação |
|-------|------|
| `W` | Cima |
| `A` | Esquerda |
| `S` | Baixo |
| `D` | Direita |

Maiúsculas e minúsculas funcionam igual.

Em cada turno o jogador escolhe entre **andar**, **minerar** ou **desistir da partida**. Depois de escolher andar ou minerar, informa a direção.

---

## 🗺️ O mapa

A mina é uma matriz de 8 linhas por 8 colunas, desenhada no terminal com os números das linhas e colunas para facilitar a navegação:

```
  0 1 2 3 4 5 6 7 
0 🧍⬛⬛🟫⬛⬛⬛🟫
1 ⬛⬛⬛🟫⬛⬛⬛⬛
2 ⬛🟫⬛⬛⬛⬛🟫⬛
3 🟫⬛⬛⬛⬛⬛🟫⬛
4 ⬛⬛⬛⬛⬛🟫⬛⬛
5 ⬛⬛⬛⬛⬛⬛⬛🟫
6 ⬛⬛⬛⬛🟫⬛⬛⬛
7 ⬛⬛⬛⬛⬛⬛⬛⬛
```

| Símbolo | Significado |
|---------|-------------|
| 🧍 | Jogador |
| 🟫 | Pedra — bloqueia a passagem, precisa ser minerada |
| ⬛ | Caminho livre |

> Os emoji são apenas o **desenho**. Internamente a matriz continua guardando `"#"` e `"."` — trocar a aparência do mapa não exigiu alterar nenhuma regra do jogo, só a função `mostrarMapa`.

O jogador começa sempre em `[0][0]` e **não pode** sair do mapa nem atravessar pedras.

---

## 📜 Regras

### Objetivo

Encontrar a escada escondida em cada um dos três níveis. A escada fica sempre **embaixo de uma pedra**, sorteada no início do nível — não dá para vencer só andando, é preciso minerar.

### Níveis

| Nível | Pedras na mina | HP do monstro |
|-------|----------------|---------------|
| 1 | 10 | 2 |
| 2 | 20 | 3 |
| 3 | 30 | 4 |

A cada nível uma mina nova é gerada. **O HP e as gemas do jogador são mantidos** na passagem de um nível para o outro — o que torna a gestão de vida a decisão central do jogo.

### Eventos

Ao quebrar uma pedra, um evento acontece:

| Evento | Efeito |
|--------|--------|
| 💎 Gema | +1 gema (pontuação da partida) |
| ❤️ Cura | +1 HP, até o máximo de 3 |
| 👹 Monstro | Inicia uma batalha |
| 🪜 Escada | Avança de nível — ou vence, se for o nível 3 |

Gema, cura e monstro têm a mesma chance de aparecer (1/3 cada).

### Combate

O jogador começa com **3 HP** e nunca passa disso. Em cada rodada ele escolhe atacar, defender ou fugir, e o resultado é decidido por um dado de seis lados.

**Atacar**

| Dado | Resultado |
|------|-----------|
| 1–2 | Acerta 1 de dano |
| 3 | Acerto crítico: 2 de dano |
| 4 | Erra, nada acontece |
| 5 | Erra e sofre 1 de dano |
| 6 | Acerta 1 e sofre 1 de dano |

**Defender**

| Dado | Resultado |
|------|-----------|
| 1–3 | Defende, sem danos |
| 4 | Defende e contra-ataca 1 de dano |
| 5 | Falha e sofre 1 de dano |
| 6 | Sofre 1 e contra-ataca 1 |

**Fugir**

| Dado | Resultado |
|------|-----------|
| 1–2 | Foge sem dano |
| 3–4 | Foge, mas sofre 1 de dano |
| 5 | Não consegue fugir |
| 6 | Não consegue fugir e sofre 1 de dano |

Derrotar um monstro rende **2 gemas**. Fugir ou ser derrotado não concede nada.

### Fim de partida

- **Vitória** — encontrar a escada do nível 3
- **Derrota** — HP chegar a 0
- **Desistência** — sair da mina por conta própria

---

## 🧱 Estrutura do código

Todo o jogo está em `main.py`, organizado em **19 funções** com responsabilidade única. Nenhuma função faz duas coisas ao mesmo tempo.

### Geração da mina

| Função | Responsabilidade |
|--------|------------------|
| `sortearPedra(nivel)` | Sorteia as posições das pedras, sem repetir e sem ocupar a casa inicial |
| `sortearEscada(pedras)` | Escolhe qual das pedras esconde a escada |
| `criarMapa(pedras)` | Monta a matriz 8×8 a partir da lista de posições |
| `mostrarMapa(mapa, jogador)` | Desenha a mina no terminal |

### Jogador

| Função | Responsabilidade |
|--------|------------------|
| `criarJogador(nome)` | Cria o dicionário com nome, HP, gemas, nível e posição |
| `mostrarStatus(jogador)` | Exibe os dados atuais |
| `calcularDestino(jogador, direcao)` | Calcula para qual casa uma direção levaria |
| `mover(jogador, mapa, direcao)` | Move o jogador, validando bordas e pedras |

### Mineração e eventos

| Função | Responsabilidade |
|--------|------------------|
| `minerar(jogador, mapa, direcao, escada)` | Quebra a pedra vizinha e devolve o evento encontrado |
| `sortearDrop(posicao, escada)` | Sorteia qual evento estava dentro da pedra |
| `aplicarEvento(jogador, evento)` | Aplica o efeito do evento no jogador |

### Combate

| Função | Responsabilidade |
|--------|------------------|
| `monstroSelvagem(nome, hp, nivel)` | Conduz a batalha até alguém cair ou o jogador fugir |
| `dadoAtaque(nome, dado)` | Resultado da rolagem ao atacar |
| `dadoDefesa(nome, dado)` | Resultado da rolagem ao defender |
| `dadoFuga(nome, dado)` | Resultado da rolagem ao fugir |

### Fluxo do programa

| Função | Responsabilidade |
|--------|------------------|
| `menuPrincipal()` | Menu inicial — jogar, tutorial ou sair |
| `jogar()` | Conduz a partida pelos três níveis e decide o fim |
| `jogarNivel(jogador, mapa, escada)` | Roda uma mina inteira, turno a turno |
| `tutorial()` | Explica as regras e os controles |

### Fluxo de um turno

```
jogarNivel
    └─ mostrarMapa          desenha a mina
    └─ minerar              quebra a pedra
         └─ calcularDestino  qual casa a direção aponta
         └─ sortearDrop      o que havia dentro
    └─ aplicarEvento        aplica o efeito
         └─ monstroSelvagem  se for monstro, a batalha
              └─ dadoAtaque / dadoDefesa / dadoFuga
```

---

## 🧠 Decisões técnicas

Três decisões guiaram a arquitetura do projeto.

### 1. A matriz guarda o cenário; o dicionário guarda o jogador

A posição do jogador **não** é gravada na matriz. O 🧍 é desenhado por cima apenas na hora de imprimir.

Se a posição fosse gravada na matriz, cada movimento exigiria apagar o jogador da casa anterior — e apagar trocando por quê? Por chão livre? E se ali houvesse uma pedra? Manter cada informação num lugar só elimina a classe inteira de bugs.

Essa decisão se pagou quando o mapa foi trocado para emoji: como a matriz guarda `"#"` e `"."` e o desenho é feito à parte, **apenas a função `mostrarMapa` precisou mudar**. Nenhuma regra do jogo foi tocada, e todos os testes de lógica continuaram passando sem alteração.

### 2. Calcular, validar, só então aplicar

As funções `mover` e `minerar` seguem o mesmo padrão: calculam o destino em variáveis locais, conferem todas as regras e **só gravam no jogador ou no mapa depois de passar em tudo**.

A alternativa — mover primeiro e desfazer se der errado — funciona, mas exige lembrar de desfazer em cada nova regra que surgir. Com este padrão, enquanto uma validação falhar, nada foi alterado.

### 3. A matriz é montada com laço aninhado, nunca com `* 8`

```python
mapa = [["."] * 8] * 8    # ERRADO
```

Essa forma curta não cria oito listas: cria **uma só, repetida oito vezes**. As linhas passam a ser o mesmo objeto na memória, e alterar uma casa alteraria a coluna inteira — quebrando a mineração de um jeito muito difícil de rastrear.

Por isso `criarMapa` monta cada linha com um `for`, e existe um teste automatizado só para garantir que as linhas continuem independentes.

---

## 📚 Conceitos da disciplina aplicados

| Conceito | Onde aparece |
|----------|--------------|
| **Funções** | 19 funções, cada uma com uma responsabilidade única |
| **Listas** | Posições das pedras, linhas da matriz, opções de evento |
| **Tuplas** | Retorno múltiplo em `dadoAtaque`, `dadoDefesa`, `dadoFuga` e `calcularDestino` |
| **Matrizes** | A mina 8×8, acessada por `mapa[linha][coluna]` |
| **Dicionários** | O jogador, com nome, HP, gemas, nível e posição |
| **Estruturas de repetição** | Laços da partida, do nível e do combate |
| **Estruturas de decisão** | `match / case` no menu, no combate e nos eventos |
| **Mutabilidade** | `mover` altera o dicionário sem `return`; `monstroSelvagem` precisa devolver o HP, por ser número |

---

## ✅ Validação

O jogo foi testado de forma automatizada, e não apenas jogando na mão.

**Geração da mina** — 6.000 partidas simuladas nos três níveis:

- quantidade de pedras sempre correta, sem repetições
- nenhuma pedra na casa inicial do jogador
- exatamente uma escada por mina

**Movimentação e mineração** — 21 testes cobrindo:

- as quatro direções, em maiúscula e minúscula
- bloqueio nas quatro bordas do mapa
- bloqueio por pedra no caminho
- recusa de direções inválidas, incluindo texto e entrada vazia
- independência das linhas da matriz

**Partida completa** — 500 partidas jogadas do início ao fim por um programa que substitui a entrada do teclado:

- nenhuma travou, nenhuma encerrou com erro
- 46 vitórias

**Desenho do mapa** — após a troca para emoji:

- as oito linhas e o cabeçalho têm a mesma largura em colunas de terminal
- a matriz continua guardando apenas `"#"` e `"."`, sem emoji
- as 500 partidas automáticas terminam com as mesmas 46 vitórias de antes, confirmando que só a aparência mudou

**Robustez** — o jogo não quebra quando o jogador digita texto no lugar de número, aperta Enter sem escrever nada ou informa uma direção inexistente.

---

## 📊 Análise de equilíbrio

Além de funcionar, o jogo foi **medido**. Rodando milhares de partidas automáticas, chegamos aos seguintes números.

**Sobrevivência a uma única batalha, com 3 HP cheios:**

| Nível | HP do monstro | Sobrevive |
|-------|---------------|-----------|
| 1 | 2 | 93,4% |
| 2 | 3 | 85,6% |
| 3 | 4 | 76,2% |

**Quantas pedras é preciso quebrar até achar a escada:**

| Nível | Pedras | Média até a escada |
|-------|--------|--------------------|
| 1 | 10 | 5,5 |
| 2 | 20 | 10,5 |
| 3 | 30 | 15,5 |

Como 1 em cada 3 pedras esconde um monstro, uma partida completa gera **cerca de 10 batalhas** — e o HP não é restaurado na troca de nível. Daí a taxa de vitória observada de aproximadamente **9%**.

**Valor esperado de cada ação no combate:**

| Ação | Dano causado por rodada | Dano sofrido por rodada |
|------|-------------------------|-------------------------|
| Atacar | 0,83 HP | 0,33 HP |
| Defender | 0,33 HP | 0,33 HP |

O dado revela um desequilíbrio: **defender tem exatamente o mesmo risco de atacar, mas causa 2,5 vezes menos dano**. Na prática, nunca compensa defender. Medindo a sobrevivência por estratégia ao longo de 20.000 batalhas:

| Estratégia | Nível 1 | Nível 3 |
|------------|---------|---------|
| Só atacar | 93,4% | 76,2% |
| Só defender | 71,0% | 23,0% |

O ajuste natural é reduzir o dano sofrido ao defender, para que a ação passe a ter um papel real.

---

## 🚧 Próximos passos

- [ ] **CRUD de ranking** — salvar e gerenciar as partidas concluídas, com as quatro operações sobre a lista de registros
- [ ] **Rebalanceamento do combate** — dar propósito à ação de defender e revisar a curva de dificuldade
- [x] ~~**Mapa com emoji**~~ — concluído

---

## 📁 Estrutura do repositório

```
caverna-craft/
├── main.py      todo o jogo
└── README.md    este arquivo
```
