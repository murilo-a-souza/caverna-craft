import random

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

# Inicia a partida criando o jogador e mostrando seus dados
def jogar():
    nome = input("Digite o nome do jogador: ")

    jogador = criarJogador(nome)

    mostrarStatus(jogador)


# Explica as regras e os controles do jogo
def tutorial():
    print("\n===== TUTORIAL - CAVERNA CRAFT =====")

    print("\nOBJETIVO:")
    print("Explore a caverna, quebre pedras e encontre a escada")
    print("escondida para avançar pelos níveis.")
    print("Complete os 3 níveis sem perder toda a vida para vencer.")

    print("\n===== MAPA =====")
    print("A mina tem 8 linhas e 8 colunas.")
    print("P = Jogador")
    print("# = Pedra")
    print(". = Caminho livre")

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
    print("Gema    = Você recebe 1 gema.")
    print("Cura    = Você recupera 1 HP, até o máximo de 3.")
    print("Monstro = Uma batalha começa.")
    print("Escada  = Permite avançar de nível ou vencer no terceiro nível.")
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


# Mostra as opções iniciais do programa
def menuPrincipal():
    menuAtivo = True

    while menuAtivo:
        print("\n===== CAVERNA CRAFT =====")
        print("1 - Jogar")
        print("2 - Tutorial")
        print("3 - Sair")

        opcao = input("Escolha uma opção: ")

        match opcao:
            case "1":
                jogar()

            case "2":
                tutorial()

            case "3":
                print("Jogo encerrado.")
                menuAtivo = False

            case _:
                print("Não é uma opção válida.")


menuPrincipal()
