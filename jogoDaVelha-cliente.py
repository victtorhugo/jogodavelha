from socket import *
from termcolor import colored

host = '192.168.0.104'
port = 5000
tcp = socket(AF_INET, SOCK_STREAM)
dest = (host, port)
tcp.connect(dest)

tabuleiro = ['',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
tabuleiro_aux = ['','1','2','3','4','5','6','7','8','9','2',' ']

jogadas_possiveis = ['1','2','3','4','5','6','7','8','9']

jogadas = 0  #Contador de jogadas
vitorias_servidor = 0 #Contador de vitorias do jogador servidor
vitorias_cliente = 0 #Contador de vitorias do jogador cliente
empates = 0 #Contador de empates

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

def jogada(posicao, jogador_vez):
    '''Verifica se a posição já foi jogada e realiza a jogada'''
    
    while True:
        if tabuleiro[posicao] not in [simbolo_jogador_cliente, simbolo_jogador_servidor]:

            if jogador_vez == 'servidor':
                tabuleiro[posicao] = simbolo_jogador_cliente
                return True

            elif jogador_vez == 'cliente':
                tabuleiro[posicao] = simbolo_jogador_servidor
                return True

            break

        else:
            return False

def vencedor():
    '''Verifica se tem algum vencedor'''
    horizontal = 1
    vertical = 1
    
    while horizontal <= 7:
    
        if tabuleiro[horizontal] == tabuleiro[horizontal + 1] and tabuleiro[horizontal + 1] == tabuleiro[horizontal + 2] and tabuleiro[horizontal + 2] == simbolo_jogador_cliente: #ganhou na horizontal
            horizontal = 1
            return 'cliente'
            break

        elif tabuleiro[horizontal] ==tabuleiro[horizontal + 1] and tabuleiro[horizontal + 1] ==tabuleiro[horizontal + 2] and tabuleiro[horizontal + 2] == simbolo_jogador_servidor: #ganhou na horizontal
            horizontal = 1
            return 'servidor'
            break

        aux = vertical + 3
        if tabuleiro[vertical] == tabuleiro[vertical + 3] and tabuleiro[vertical] == tabuleiro[aux + 3] and tabuleiro[aux + 3] == simbolo_jogador_cliente: #ganhou na vertical
            horizontal = 1
            return 'cliente'
            break

        elif tabuleiro[vertical] == tabuleiro[vertical + 3] and tabuleiro[vertical] == tabuleiro[aux + 3] and tabuleiro[aux + 3] == simbolo_jogador_servidor: #ganhou na vertical
            horizontal = 1
            return 'servidor'
            break

        if tabuleiro[7] == tabuleiro[5] and tabuleiro[5] == tabuleiro[3] and tabuleiro[3] == simbolo_jogador_cliente: #ganhou na diagonal 1
            horizontal = 1
            return 'cliente'
            break

        elif tabuleiro[7] == tabuleiro[5] and tabuleiro[5] == tabuleiro[3] and tabuleiro[3] == simbolo_jogador_servidor: #ganhou na diagonal 1
            horizontal = 1
            return 'servidor'
            break

        if tabuleiro[9] == tabuleiro[5] and tabuleiro[5] == tabuleiro[1] and tabuleiro[1] == simbolo_jogador_cliente: #ganhou na diagonal 2
            horizontal = 1
            return 'cliente'
            break

        elif tabuleiro[9] == tabuleiro[5] and tabuleiro[5] == tabuleiro[1] and tabuleiro[1] == simbolo_jogador_servidor: #ganhou na diagonal 2
            horizontal = 1
            return 'servidor'
            break

        horizontal += 3
        vertical += 1

def jogar_novamente(): #como estava repetindo muito criei está função
    '''Verifica se os jogadores querem jogar novamente'''

    print('')
    escolha = input("Digite S se quer jogar novamente? Caso contrário, aperte outra tecla: ")

    print('')
    print('Esperando a resposta de %s! Aguarde...' %jogador_servidor)
    resposta = conecxao.recv(1024)

    envia_escolha = bytes(escolha)
    conecxao.send(envia_escolha)

    if escolha.upper() == 'S' and resposta == 'S':
        
        global jogadasjogadas #Renova a contagem de jogadas
        jogadas = 1
        
        return True

    else:

        print('O outro jogador desistiu. Fim de Jogo')
        print('')
        print('Resultado do game: ')
        print('')
        print('Empates: ', empates)
        print('Vitórias de %s = %d' %(jogador_servidor, vitorias_servidor))
        print('Vitórias de %s = %d' %(jogador_cliente, vitorias_cliente))

while True:
    
    while True:

        
        jogador_cliente = input('Informe o nome do jogar que vai jogar primeiro: ')

        if not jogador_cliente.isalpha():

            print('Informe seu nome corretamente.')
            print('')

        else:

            print('')
            print('Esperando o nome do jogador adversário! Aguarde...')
            jogador_servidor = conecxao.recv(1024)
            jogador_servidor = str(jogador_cliente,'utf-8')

            envia_nome = jogador_cliente
            envia_nome = bytes(envia_nome)
            conecxao.send(envia_nome)

            break
    
    while True:

        simbolo_jogador_cliente = input('%s Informe se você vai jogar: '%(jogador_cliente))
        simbolo_jogador_cliente = simbolo_jogador_cliente.upper()

        print('Esperando o símbolo que será usado pelo adversário! Aguarde...')
        simbolo_jogador_servidor = conecxao.recv(1024)
        simbolo_jogador_servidor = str(simbolo_jogador_servidor, 'utf-8')

        enviar_simbolo = simbolo_jogador_cliente
        enviar_simbolo = bytes(enviar_simbolo)
        conecxao.send(enviar_simbolo)

    
        if simbolo_jogador_cliente == simbolo_jogador_servidor:

            print('O outro jogador escolheu o mesmo Símbolo que você. Informe outro símbolo para continuar o jogo.')
            print('')

        else:

            simbolo_jogador_cliente = colored(simbolo_jogador_cliente, 'red')
            simbolo_jogador_servidor = colored(simbolo_jogador_servidor, 'blue')
            print('')
            break

    print('Esperando o %s jogar! Aguarde...'%jogador_servidor)
    posicao_adversario = conecxao.recv(1024)  #recebe a posição que o adversário vai jogar
    posicao_adversario = str(posicao_adversario, 'utf-8')
    posicao_adversário = int(posicao_adversario)

    jogada(posicao_adversario, jogador_vez)
    jogadas += 1
    
    imprime(tabuleiro_aux)
    imprime(tabuleiro)

    venceu = vencedor() 
    
    if venceu == 'servidor':

        imprime(tabuleiro_aux)
        imprime(tabuleiro)
        print('O jogador %s Ganhou! Você Perdeu!!' %jogador_cliente)
        vitorias_servidor += 1

        if jogar_novamente() == True:

            continue

        else:
            break

    elif jogadas == 9:

        imprime(tabuleiro_aux)
        imprime(tabuleiro)
        print('Partida empatada,nenhum vencendor!')
        empates += 1

        if jogar_novamente() == True:

            continue
        else:
            break

    jogador_vez = tcp.recv(1024)
    jogador_vez = str(jogador_vez,'utf-8')

    while jogador_vez == 'cliente':

        imprime(tabuleiro_aux)
        imprime(tabuleiro)

        posicao = input('Escolha, utilizando os números de 1 a 9, em qual posição vai jogar %s: ' %jogador_cliente)

        if posicao in jogadas_possiveis and jogada(posicao, jogador_vez) == True:

            posicao = int(posicao)
            posicao_enviada = str(posicao)
            posicao_enviada = bytes(posicao_enviada)
            conecxao.send(posicao_enviada)  #O cliente vai receber a posição, verificar em vencedor() e retornar o resultado

            break

        else:

            imprime(tabuleiro_aux)
            imprime(tabuleiro)
            print('Posição Inválida. Informe um número de 1 a 9.')
            continue

    imprime(tabuleiro_aux)
    imprime(tabuleiro)
    jogadas += 1

    venceu = vencedor()

    if venceu == 'cliente':

        imprime(tabuleiro_aux)
        imprime(tabuleiro)
        print('Parabéns %s! Você GANHOU!!' %jogador_cliente)
        vitorias_cliente += 1

        if jogar_novamente() == True:

            continue

        else:
            break

    elif jogadas == 9:

        imprime(tabuleiro_aux)
        imprime(tabuleiro)
        print('Partida empatada,nenhum vencendor!')
        empates += 1

        if jogar_novamente() == True:

            continue

        else:
            break