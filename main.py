import random

#Sortear localzação das pedras
def sortearPedra(nivel:int) -> list[list[int]]:
    lista = []
    for i in range(10*nivel):
        x = random.randrange(8)
        y = random.randrange(8)
        for j in lista:
            while [x,y] == j:
                x = random.randrange(8)
        lista.append([x,y])
    return lista

# Sortear um do local das pedras para ser a escada
def sortearEscada(pedras: list[list[int]]) -> list[int]:
    escada = random.choice(pedras)
    return escada

#Sortear um evento ao clicar em uma pedra
def sortearDrop(posicao:list[int], escada:list[int]):
    if posicao == escada:
        return "escada"

    drop = random.choice(["gema", "cura", "monstro"])
    return drop

#numa luta, o usuário decide atacar
def dadoAtaque(nome:str,dado:int) -> tuple[int,int]:
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
def dadoDefesa(nome: str,dado:int) -> tuple[int,int] :
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
def dadoFuga(nome:str,dado:int)-> tuple[int,int] :
    #Consegue fugir 2/6, foge om sequelas 2/6, não consegue fugir 1/6, não consegue fugir e toma dano 1/6
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
def monstroSelvagem(nome:str,hp:int,nivel:int)-> tuple[int,int]:
    monstroHP = 1+nivel
    gema, dano, danoM = 0,0 ,0
    fuga = False
    while monstroHP > 0 and hp > 0:
        print(f'Nome: {nome}\t\tHP: {hp}\nMonstro da Caverna\tHP: {monstroHP}\n')
        opcao = int(input('1. Atacar\n2. Defender\n3. Fugir\nEscolha uma opção: '))
        dado = random.randrange(1,7)
        match opcao:
            case 1:
                dano,danoM = dadoAtaque(nome,dado)
            case 2:
                dano,danoM = dadoDefesa(nome,dado)
            case 3:
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

def eventoResultado(evento:str,nome:str,hp:int,nivel:int,gemas:int)->tuple[int]|void:
    match evento:
        case "gema":
            gemas += 1
        case "escada":
            nivel += 1
            novasPedras = sortearPedra(nivel)
            novaEscada = sortearEscada(novasPedras)
            # chamar inicio de jogo com novo nivel
        case "cura":
            hp += 1
        case "monstro":
            hp,gema = monstroSelvagem(nome,hp,nivel)
    return gema,hp,nivel

def iniciarJogo(nivel:int=1)->str:
    #chamar população #caverna = popularMatriz()
    print()

def main() -> void:
    escolha_numero = 1
    print ("iniciar jogo")
    print ("1- Jogar")
    print ("2- Tutorial ")
    print ("3- sair")
    numero = int(input("Escolha uma opção: "))
    match escolha_numero:
        case 1:
            print('jogar') #opção de jogar 
        case 2:
            print('Tutorial') #opção do tutorial
        case 3:
            print('Saindo...') #opção de sair
        case _:
            print('Não é uma opção válida.') #caso não insira opção válida