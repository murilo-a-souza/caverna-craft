import random
import json
import sys

# Sem esta linha, imprimir emoji derruba o jogo em terminais que nao usam UTF-8
sys.stdout.reconfigure(encoding="utf-8")

#Sortear localização das pedras
def sortearPedra(nivel):
    lista = []
    while len(lista) < 10*nivel:
        x = random.randrange(8)
        y = random.randrange(8)
        # so aceita a pedra se nao for repetida e nao cair na posicao inicial do jogador
        if [x,y] not in lista and [x,y] != [0,0]:
            lista.append([x,y])
    return lista

# Sortear um do local das pedras para ser a escada
def sortearEscada(pedras):
    escada = random.choice(pedras)
    return escada

# Monta a matriz 8x8 da mina a partir da lista de pedras
def criarMapa(pedras):
    mapa = []
    for i in range(8):
        linha = []
        for j in range(8):
            linha.append(".")
        mapa.append(linha)

    # marca cada pedra sorteada na matriz
    for pedra in pedras:
        mapa[pedra[0]][pedra[1]] = "#"

    return mapa

# Desenha a mina na tela, com o jogador por cima
# A matriz continua guardando "#" e ".": o emoji e so o desenho
def mostrarMapa(mapa, jogador):
    print("  0 1 2 3 4 5 6 7 ")
    for i in range(8):
        linha = str(i) + " "
        for j in range(8):
            if i == jogador["linha"] and j == jogador["coluna"]:
                linha = linha + "🧍"
            elif mapa[i][j] == "#":
                linha = linha + "🟫"
            else:
                linha = linha + "⬛"
        print(linha)

# Cria o jogador com os dados iniciais da partida
def criarJogador(nome):
    jogador = {
        "nome": nome,
        "hp": 3,
        "gemas": 0,
        "nivel": 1,
        "linha": 0,
        "coluna": 0
    }
    
    return jogador

# Mostra as informações atuais do jogador
def mostrarStatus(jogador):
    print("===== STATUS DO JOGADOR =====")
    print("Nome:", jogador["nome"])
    print("HP:", jogador["hp"])
    print("Gemas:", jogador["gemas"])
    print("Nível:", jogador["nivel"])

# Calcula para qual casa o jogador iria naquela direcao, sem mexer nele
def calcularDestino(jogador, direcao):
    linha = jogador["linha"]
    coluna = jogador["coluna"]

    match direcao:
        case "W"|"w":
            linha = linha - 1
        case "S"|"s":
            linha = linha + 1
        case "A"|"a":
            coluna = coluna - 1
        case "D"|"d":
            coluna = coluna + 1
        case _:
            print('❓ Direção inválida! Use W, A, S ou D.')
            return -1, -1

    return linha, coluna

# Move o jogador uma casa na direcao escolhida (W, A, S ou D)
def mover(jogador, mapa, direcao):
    linha, coluna = calcularDestino(jogador, direcao)

    # o -1, -1 e o aviso de direcao invalida que o calcularDestino devolve
    if linha == -1 and coluna == -1:
        return False

    # o mapa vai da linha 0 ate a 7 e da coluna 0 ate a 7
    if linha < 0 or linha > 7 or coluna < 0 or coluna > 7:
        print('🧱 Você bateu na parede da caverna!')
        return False

    if mapa[linha][coluna] == "#":
        print('🟫 Tem uma pedra no caminho! Você precisa minerar antes de passar.')
        return False

    # so agora, com tudo validado, o jogador anda de verdade
    jogador["linha"] = linha
    jogador["coluna"] = coluna
    return True

#Sortear um evento ao clicar em uma pedra
def sortearDrop(posicao, escada):
    if posicao == escada:
        return "escada"

    drop = random.choice(["gema", "cura", "monstro"])
    return drop

#numa luta, o usuário decide atacar
def dadoAtaque(nome:str,dado:int):
    match dado:
        case 1|2:
            print(f'{nome} acertou o monstro e tirou 1hp')
            return 0,1 #Acerta e não sofre 2/6
        case 3:
            print(f'{nome} acertou um crítico no monstro e tirou 2hp')
            return 0,2 #acerto crítico 1/6
        case 4:
            print(f'{nome} errou um ataque, nada acontece')
            return 0,0 #acerta e sofre 1/6
        case 5:
            print(f'{nome} errou um ataque, e tomou um contra-ataque, perdendo um de 1hp')
            return 1,0 # erra e não sofre 1/6
        case 6:
            print(f'{nome} acertou mas também tomou um contra-ataque, ambos perderam 1hp')
            return 1,1 # erra e sofre 1/6

#numa luta, o usuário decide defender
def dadoDefesa(nome: str,dado:int):
    match dado:
        case 1|2|3:
            print(f'{nome} se defendeu, sem danos')
            return 0,0 #Não sofre 3/6
        case 4:
            print(f'{nome} se defendeu e conseguiu um contra-ataque de 1hp no monstro')
            return 0,1 #não sofre e acerta 1/6
        case 5:
            print(f'{nome} não se defendeu e tomou um dano de 1hp')
            return 1,0 #sofre 1/6
        case 6:
            print(f'{nome} não se defendeu mas tomou dano de 1hp, e se levantou raidamente para um contra-ataque de 1hp')
            return 1,1 #sofre e acerta 1/6

#numa luta, o usuário decide fugir
def dadoFuga(nome:str,dado:int):
    #Consegue fugir 2/6, foge com sequelas 2/6, não consegue fugir 1/6, não consegue fugir e toma dano 1/6
    match dado:
        case 1|2:
            print(f'{nome} fugiu sem tomar danos')
            return 0, True
        case 3|4:
            print(f'{nome} fugiu, mas sofre um de 1hp')
            return 1, True
        case 5:
            print(f'{nome} não conseguiu fugir')
            return 0, False
        case 6:
            print(f'{nome} não conseguiu fugir e tomou dano de 1hp')
            return 1, False

#Quando o evento é um monstro
def monstroSelvagem(nome:str,hp:int, nivel:int):
    # Sem vida, o jogador nao inicia o combate nem recebe gemas
    if hp <= 0:
        return hp, 0

    monstroHP = 1+nivel
    gema = 0
    fuga = False
    while monstroHP > 0 and hp > 0:
        dano, danoM = 0, 0 # zera o resultado da rodada anterior
        print(f'Nome: {nome}\t\tHP: {hp}\nMonstro da Caverna\tHP: {monstroHP}\n')
        opcao = input('1. Atacar\n2. Defender\n3. Fugir\nEscolha uma opção: ')
        dado = random.randrange(1,7)
        match opcao:
            case "1":
                dano,danoM = dadoAtaque(nome,dado)
            case "2":
                dano,danoM = dadoDefesa(nome,dado)
            case "3":
                dano,fuga = dadoFuga(nome,dado)
            case _:
                print('Opção inválida!')
        hp -= dano
        monstroHP -= danoM
        if fuga == True:
            return hp,gema
        if hp <= 0:
            print(f'{nome} foi derrotado, fim de jogo!')
            return hp,gema
    gema = 2
    return hp,gema #caso não fuja ou seja derrotado quer dizer que ganhou do monstro

# Quebra a pedra vizinha e devolve o evento que estava escondido nela
def minerar(jogador, mapa, direcao, escada):
    linha, coluna = calcularDestino(jogador, direcao)

    if linha == -1 and coluna == -1:
        return "nada"

    if linha < 0 or linha > 7 or coluna < 0 or coluna > 7:
        print('🧱 Não dá para minerar fora da caverna!')
        return "nada"

    if mapa[linha][coluna] != "#":
        print('❓ Não tem pedra nessa direção.')
        return "nada"

    # a pedra quebrada vira caminho livre no mapa
    mapa[linha][coluna] = "."
    print('⛏️  Você quebrou a pedra!')

    return sortearDrop([linha, coluna], escada)

# Aplica no jogador aquilo que foi encontrado dentro da pedra
def aplicarEvento(jogador, evento):
    match evento:
        case "gema":
            jogador["gemas"] = jogador["gemas"] + 1
            print('💎 Você encontrou uma gema!')
        case "cura":
            if jogador["hp"] < 3:
                jogador["hp"] = jogador["hp"] + 1
                print('❤️  Você encontrou uma cura e recuperou 1 HP!')
            else:
                print('❤️  Você encontrou uma cura, mas sua vida já está cheia.')
        case "monstro":
            print('👹 Um monstro da caverna apareceu!')
            hp, gemas = monstroSelvagem(jogador["nome"], jogador["hp"], jogador["nivel"])
            jogador["hp"] = hp
            jogador["gemas"] = jogador["gemas"] + gemas
        case "escada":
            print('🪜 Você encontrou a escada escondida!')

# Joga um nivel inteiro. Devolve True se o jogador achou a escada
def jogarNivel(jogador, mapa, escada):
    achouEscada = False

    while achouEscada == False and jogador["hp"] > 0:
        mostrarMapa(mapa, jogador)
        print("❤️ ", jogador["hp"], "  💎", jogador["gemas"], "  🗺️  Nível", jogador["nivel"])

        print("1 - Andar")
        print("2 - Minerar")
        print("3 - Desistir da partida")
        acao = input("Escolha uma opção: ")

        match acao:
            case "1":
                direcao = input("Andar para onde? (W, A, S, D): ")
                mover(jogador, mapa, direcao)

            case "2":
                direcao = input("Minerar para onde? (W, A, S, D): ")
                evento = minerar(jogador, mapa, direcao, escada)
                aplicarEvento(jogador, evento)
                if evento == "escada":
                    achouEscada = True

            case "3":
                print("🚪 Você desistiu e voltou para a superfície.")
                return False

            case _:
                print("Não é uma opção válida.")

    # se saiu do while sem achar a escada, foi porque o hp acabou
    return achouEscada

# Inicia a partida e conduz o jogador pelos tres niveis
def jogar(ranking):
    nome = input("Digite o nome do jogador: ")
    jogador = criarJogador(nome)
    jogando = True

    while jogando == True and jogador["nivel"] <= 3:
        # cada nivel ganha uma mina nova, com mais pedras que a anterior
        pedras = sortearPedra(jogador["nivel"])
        escada = sortearEscada(pedras)
        mapa = criarMapa(pedras)

        # o jogador sempre recomeca no canto da mina nova
        jogador["linha"] = 0
        jogador["coluna"] = 0

        print("")
        print("⛏️  ===== NÍVEL", jogador["nivel"], "=====")
        mostrarStatus(jogador)

        if jogarNivel(jogador, mapa, escada) == True:
            jogador["nivel"] = jogador["nivel"] + 1
        else:
            jogando = False

    # a partida acabou por um destes tres motivos
    print("")
    if jogador["hp"] <= 0:
        print("💀 ===== DERROTA =====")
        print(jogador["nome"], "não resistiu à caverna.")
    elif jogador["nivel"] > 3:
        print("🏆 ===== VITÓRIA =====")
        print(jogador["nome"], "encontrou a saída e escapou da caverna!")
    else:
        print("🚪 ===== PARTIDA ENCERRADA =====")
        print(jogador["nome"], "saiu da caverna por conta própria.")

    print("💎 Gemas coletadas:", jogador["gemas"])
    opcao = input("Deseja salvar sua pontuação no ranking? (S/N): ")

    if opcao.lower() == "s":
        registrar_ranking(ranking, jogador)
        print("Pontuação salva no ranking!")
    input("Pressione ENTER para voltar ao menu principal...")

# Explica as regras e os controles do jogo
def tutorial():
    print("\n===== TUTORIAL - CAVERNA CRAFT =====")

    print("\nOBJETIVO:")
    print("Explore a caverna, quebre pedras e encontre a escada")
    print("escondida para avançar pelos níveis.")
    print("Complete os 3 níveis sem perder toda a vida para vencer.")

    print("\n===== MAPA =====")
    print("A mina tem 8 linhas e 8 colunas.")
    print("🧍 = Jogador")
    print("🟫 = Pedra")
    print("⬛ = Caminho livre")

    print("\n===== MOVIMENTAÇÃO =====")
    print("W = Cima")
    print("S = Baixo")
    print("A = Esquerda")
    print("D = Direita")
    print("O jogador não pode sair do mapa nem atravessar pedras.")
    print("Para liberar o caminho, é necessário minerá-las.")

    print("\n===== MINERAÇÃO =====")
    print("Ao escolher minerar, selecione uma direção: W, A, S ou D.")
    print("Se existir uma pedra ao seu lado nessa direção, ela será quebrada.")
    print("A posição ficará livre e um evento acontecerá.")
    print("Se não houver pedra ou a posição estiver fora do mapa, nada será minerado.")

    print("\n===== EVENTOS =====")
    print("💎 Gema    = Você recebe 1 gema.")
    print("❤️  Cura    = Você recupera 1 HP, até o máximo de 3.")
    print("👹 Monstro = Uma batalha começa.")
    print("🪜 Escada  = Permite avançar de nível ou vencer no terceiro nível.")
    print("As gemas contam como pontuação da partida.")

    print("\n===== COMBATE =====")
    print("Quando um monstro aparecer, você pode:")
    print("1 - Atacar")
    print("2 - Defender")
    print("3 - Fugir")
    print("O resultado da ação depende de um dado de seis lados, de 1 a 6.")
    print("Você pode sofrer dano ao atacar, defender ou tentar fugir.")
    print("A tentativa de fuga pode falhar.")
    print("Derrotar um monstro rende 2 gemas.")
    print("Fugir ou morrer no combate não concede gemas.")

    print("\n===== VIDA =====")
    print("HP representa os pontos de vida do jogador.")
    print("O jogador começa com 3 HP.")
    print("O HP perdido não é recuperado automaticamente após uma batalha.")
    print("Para recuperar vida, é necessário encontrar uma cura.")
    print("Se o HP já estiver em 3, a cura não aumenta esse valor.")

    print("\n===== NÍVEIS =====")
    print("Nível 1 = 10 pedras")
    print("Nível 2 = 20 pedras")
    print("Nível 3 = 30 pedras")
    print("A cada nível, os monstros ficam mais resistentes.")
    print("Os monstros têm 2, 3 e 4 HP nos níveis 1, 2 e 3, respectivamente.")
    print("Ao avançar, uma nova mina é criada.")
    print("Seu HP e suas gemas são mantidos ao mudar de nível.")

    print("\n===== VITÓRIA =====")
    print("Você vence ao encontrar a escada do terceiro nível.")

    print("\n===== DERROTA =====")
    print("Se seu HP chegar a 0 ou menos, a partida termina em derrota.")

    input("\nPressione ENTER para voltar ao menu principal...")


# Carrega o ranking salvo no arquivo
def carregar_ranking():
    try:
        with open("rankings.json", "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    except FileNotFoundError:
        return None

# Salva a lista de registros no arquivo
def salvar_ranking(ranking):
    with open("rankings.json", "w", encoding="utf-8") as arquivo:
        json.dump(ranking, arquivo, indent=4, ensure_ascii=False)

# Adiciona o resultado da partida ao ranking
def registrar_ranking(ranking, jogador):
    registro = {
        "nome": jogador["nome"],
        "gemas": jogador["gemas"],
        "nivel": jogador["nivel"]
    }

    ranking.append(registro)
    salvar_ranking(ranking)

# Informa a quantidade de gemas usada na ordenacao
def pegar_gemas(jogador):
    return jogador["gemas"]

# Mostra as partidas da maior para a menor pontuacao
def mostrar_ranking(ranking):
    if len(ranking) == 0:
        print("Ainda não existem partidas no ranking.")
        return

    rankingOrdenado = sorted(
        ranking,
        key=pegar_gemas,
        reverse=True
    )

    print("\n===== RANKING =====")

    for posicao, jogador in enumerate(rankingOrdenado, start=1):
        print(
            f"{posicao}º - {jogador['nome']} "
            f"| Gemas: {jogador['gemas']} "
            f"| Nível: {jogador['nivel']}"
        )

# Apaga os registros salvos no arquivo
def apagarRanking():
    with open("rankings.json", "w", encoding="utf-8") as arquivo:
        json.dump([], arquivo)

    print("Histórico de rankings apagado!")

# Mostra as opções iniciais do programa
def menuPrincipal():
    menuAtivo = True

    ranking = carregar_ranking()
    if ranking is None:
        print("Nenhum ranking encontrado. Um novo ranking será criado.")
        ranking = []

    while menuAtivo:
        print("\n⛏️  ===== CAVERNA CRAFT =====")
        print("1 - Jogar")
        print("2 - Tutorial")
        print("3 - Ver Ranking")
        print("4 - Apagar historico")
        print("5 - Sair")

        opcao = input("Escolha uma opção: ")

        match opcao:
            case "1":
                jogar(ranking)

            case "2":
                tutorial()

            case "3":
                mostrar_ranking(ranking)

            case "4":
                confirmacao = input("Tem certeza que deseja apagar o histórico? (S/N): ")
                if confirmacao.lower() == "s":
                    apagarRanking()
                    ranking = []

            case "5":
                print("Jogo encerrado.")
                menuAtivo = False

            case _:
                print("Não é uma opção válida.")


menuPrincipal()
