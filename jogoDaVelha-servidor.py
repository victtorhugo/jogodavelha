from socket import *
from termcolor import colored

host = '192.168.0.104'
port = 5000
tcp = socket(AF_INET, SOCK_STREAM)
dest = (host, port)
tcp.bind(dest)
tcp.listen(1)

tabuleiro = ['',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
tabuleiro_aux = ['','1','2','3','4','5','6','7','8','9','2',' ']

jogadas_possiveis = ['1','2','3','4','5','6','7','8','9']

jogadas = 0
jogador_da_vez = 0
vitorias_um = 0
vitorias_dois = 0
empates = 0

def imprime(tabuleiro):
    print('')
    print('\t\t      |     |     ')
    print('\t\t   %s  |  %s  |  %s '%(tabuleiro[7],tabuleiro[8],tabuleiro[9]))
    print('\t\t _____|_____|_____')
    print('\t\t      |     |     ')
    print('\t\t   %s  |  %s  |  %s '%(tabuleiro[4],tabuleiro[5],tabuleiro[6]))
    print('\t\t _____|_____|_____')
    print('\t\t      |     |     ')
    print('\t\t   %s  |  %s  |  %s '%(tabuleiro[1],tabuleiro[2],tabuleiro[3]))
    print('\t\t      |     |     ')
    print('')

def jogada(posicao,jogador_vez):
    while True:
        if tabuleiro[posicao] not in [simbolo_jogador1,simbolo_jogador2]:

            if jogador_vez == 1:
                tabuleiro[posicao] = simbolo_jogador1
                return 1
            elif jogador_vez == 2:
                tabuleiro[posicao] = simbolo_jogador2
                return 2
            break
        else:
            imprime(tabuleiro_aux)
            imprime(tabuleiro)
            posicao = int(input("Posição ocupada, tente outra posição:  "))

def vencedor():
    i = 1
    v = 1
    
    while i <= 7:
        if tabuleiro[i] == tabuleiro[i+1] and tabuleiro[i+1] == tabuleiro[i+2] and tabuleiro[i+2] == simbolo_jogador1: #ganhou na horizontal
            i = 1
            return 1
            break

        elif tabuleiro[i] ==tabuleiro[i+1] and tabuleiro[i+1] ==tabuleiro[i+2] and tabuleiro[i+2] == simbolo_jogador2: #ganhou na horizontal
            i = 1
            return 2
            break

        aux = v + 3
        if tabuleiro[v] == tabuleiro[v+3] and tabuleiro[v] == tabuleiro[aux+3] and tabuleiro[aux+3] == simbolo_jogador1:
            i = 1
            return 1
            break

        elif tabuleiro[v] == tabuleiro[v+3] and tabuleiro[v] == tabuleiro[aux+3] and tabuleiro[aux+3]  == simbolo_jogador2:
            i = 1
            return 2
            break

        #diagonal 1
        if tabuleiro[7] == tabuleiro[5] and tabuleiro[5] == tabuleiro[3] and tabuleiro[3] == simbolo_jogador1:
            i = 1
            return 1
            break

        elif tabuleiro[7] == tabuleiro[5] and tabuleiro[5] == tabuleiro[3] and tabuleiro[3] == simbolo_jogador2:
            i = 1
            return 2
            break

        #diagonal 2
        if tabuleiro[9] == tabuleiro[5] and tabuleiro[5] == tabuleiro[1] and tabuleiro[1] == simbolo_jogador1:
            i = 1
            return 1
            break

        elif tabuleiro[9] == tabuleiro[5] and tabuleiro[5] == tabuleiro[1] and tabuleiro[1] == simbolo_jogador2:
            i = 1
            return 2
            break

        i += 3
        v += 1
    return 'Sem Vencedor'

def jogar_novamente(): #como estava repetindo muito criei está função

    print('')
    escolha = input("Digite S se quer jogar novamente? Caso contrário, aperte outra tecla: ")
    envia_escolha = bytes(escolha)
    conecxao.send(escolha)

    print('')
    print('Esperando a resposicaota do adversário! Aguarde...')
    resposta = conecxao.recv(1024)

    if escolha.upper() == 'S' and resposta == 'S':
        global jogadas
        jogadas = 1
        return True

    else:
        print('O outro jogador desistiu. Fim de Jogo')
        print('')
        print('Empates: ', empates)
        print('Vitórias de %s = %d' %(jogador1, vitorias_um))
        print('Vitórias de %s = %d' %(jogador2, vitorias_dois))

while True:
    
    while True:
        
        jogador1 = input('Informe o nome do jogar que vai jogar primeiro: ')
    
        if not jogador1.isalpha():
            print('Informe seu nome corretamente.')
            print('')
        else:
            print('')
            print('Esperando o nome do jogador adversário! Aguarde...')
            conecxao, cliente = tcp.accept()

            envia_nome = jogador1
            envia_nome = bytes(envia_nome)
            conecxao.send(envia_nome)
            jogador2 = conecxao.recv(1024)
            break
    
    while True:
    
        simbolo_jogador1 = input('%s Informe se você vai jogar: '%(jogador1))
        simbolo_jogador1 = simbolo_jogador1.upper()
        
        enviar_simbolo = simbolo_jogador1
        enviar_simbolo = bytes(enviar_simbolo)
        conecxao.send(enviar_simbolo)
        
        print('Esperando o símbolo que será usado pelo adversário! Aguarde...')
        simbolo_jogador2 = conecxao.recv(1024)
        simbolo_jogador2 = str(simbolo_jogador2,'utf-8')
    
        if simbolo_jogador1 == simbolo_jogador2:
            print('O outro jogador escolheu o mesmo Símbolo que você. Informe outro símbolo para continuar o jogo.')
            print('')
        else:
            simbolo_jogador1 = colored(simbolo_jogador1, 'red')
            simbolo_jogador2 = colored(simbolo_jogador2, 'blue')
            print('')
            break

    jogador_vez = 1

    while jogador_vez == 1:

        imprime(tabuleiro_aux)
        imprime(tabuleiro)

        posicao = input("Escolha, utilizando os números de 1 a 9, em qual posição vai jogar %s: " %jogador1)

        if posicao in jogadas_possiveis:
            posicao = int(posicao)

            posicao_enviada = str(posicao)
            posicao_enviada= bytes(posicao_enviada)
            conecxao.send(posicao_enviada)  #O cliente vai receber a posição, verificar em vencedor() e retornar o resultado

            jogada(posicao, jogador_vez)

            jogador_vez = 2

        else:
            imprime(tabuleiro_aux)
            imprime(tabuleiro)
            print('Posição Inválida. Informe um número de 1 a 9.')
            continue

    imprime(tabuleiro_aux)
    imprime(tabuleiro)

    venceu = conecxao.recv(1024)
    venceu = str(venceu,'utf-8')
    venceu = int(venceu)
    jogadas += 1

    if venceu == 1:
        print("Parabéns %s! Você GANHOU!!" %jogador1)
        vitorias_um += 1

        if jogar_novamente() == True:
            continue
        else:
            break

    elif jogadas == 9:
        print("Partida empatada,nenhum vencendor!")
        empates += 1

        if jogar_novamente() == True:
            continue
        else:
            break

    print('Esperando o adversário jogar! Aguarde...')

    posicao_adversario = conecxao.recv(1024) #recebe a posição que o adversário vai jogar
    posicao_adversario = str(posicao_adversario,'utf-8')
    posicao_adversário = int(posicao_adversario)

    jogada(posicao_adversario, jogador_vez)
    imprime(tabuleiro_aux)
    imprime(tabuleiro)

    venceu = vencedor()
    jogadas += 1

    if venceu == 2:
        print("O jogador %s Ganhou! Você Perdeu!!" %jogador1)
        vitorias_um += 1

        if jogar_novamente() == True:
            continue
        else:
            break

    elif jogadas == 9:
        print("Partida empatada,nenhum vencendor!")
        empates += 1

        if jogar_novamente() == True:
            continue
        else:
            break