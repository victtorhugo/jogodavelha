from socket import *
from termcolor import colored

'''
host = '192.168.0.103'
port = 5000
tcp = socket(AF_INET, SOCK_STREAM)
dest = (host, port)
tcp.bind(dest)
tcp.listen(1)
'''

tabuleiro = ['','1','2','3','4','5','6','7','8','9','2',' ']
tabuleiro_aux = ['','1','2','3','4','5','6','7','8','9','2',' ']

jogadas_possiveis=['1','2','3','4','5','6','7','8','9']

jogadas = 1
jogador_da_vez = 0
vitorias_um = 0
vitorias_dois = 0
empates = 0

jogadores = []

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

def limpar_tabuleiro():
    for k in range(11):
        tabuleiro[k] = ' '

def jogada(pos,jogador_da_vez):
    while True:
        if tabuleiro[pos] not in [simbolo_jogador1,simbolo_jogador2]:

            if jogador_da_vez == 0:
                tabuleiro[pos] = simbolo_jogador1
                return 1
            elif jogador_da_vez == 1:
                tabuleiro[pos] = simbolo_jogador2
                return 0
            break
        else:
            print('\n' * 80)
            imprime(tabuleiro_aux)
            imprime(tabuleiro)
            pos = int(input("Posição ocupada, tente outra posição:  \n"))

    print('\n' * 60)

def vencedor():
    X = simbolo_jogador1
    O = simbolo_jogador2
    i = 1
    v = 1
    while i <= 7:
        if tabuleiro[i] == tabuleiro[i+1] and tabuleiro[i+1] == tabuleiro[i+2] and tabuleiro[i+2] == X:#ganhou na horizontal
            return 1
            i = 1
            break

        elif tabuleiro[i] ==tabuleiro[i+1] and tabuleiro[i+1] ==tabuleiro[i+2] and tabuleiro[i+2] == O:#ganhou na horizontal
            i = 1
            return 2
            break

        aux = v + 3
        if tabuleiro[v] == tabuleiro[v+3] and tabuleiro[v] == tabuleiro[aux+3] and tabuleiro[aux+3] == X:
            i = 1
            return 1
            break

        elif tabuleiro[v] == tabuleiro[v+3] and tabuleiro[v] == tabuleiro[aux+3] and tabuleiro[aux+3]  == O:
            i = 1
            return 2
            break

        #diagonal 1
        if tabuleiro[7] == tabuleiro[5] and tabuleiro[5] == tabuleiro[3] and tabuleiro[3] == X:
            i = 1
            return 1
            break

        elif tabuleiro[7] == tabuleiro[5] and tabuleiro[5] == tabuleiro[3] and tabuleiro[3] == O:
            i = 1
            return 2
            break

        #diagonal 2
        if tabuleiro[9] == tabuleiro[5] and tabuleiro[5] == tabuleiro[1] and tabuleiro[1] == X:
            i = 1
            return 1
            break

        elif tabuleiro[9] == tabuleiro[5] and tabuleiro[5] == tabuleiro[1] and tabuleiro[1] == O:
            i = 1
            return 2
            break

        i += 3
        v += 1

while True:

    jogador1 = input('Informe o nome do jogar que vai jogar primeiro: ')

    if not jogador1.isalpha():
        print('Informe seu nome corretamente.')
        print('')
    else:
        break

while True:

    simbolo_jogador1 = input('%s Informe se vc vai jogar com X ou com O: '%(jogador1))
    simbolo_jogador1 = simbolo_jogador1.upper()

    if simbolo_jogador1 not in ['X','O']:
        print('Informe X ou O, para continuar o jogo.')
        print('')
    else:
        simbolo_jogador1 = colored(simbolo_jogador1, 'red')
        print('')
        break

while True:

    jogador2 = input('Informe o nome do jogar que vai jogar em seguida: ')

    if not jogador1.isalpha():
        print('Informe seu nome corretamente.')
        print('')
    else:
        if simbolo_jogador1 == colored('X','red'):
            print('%s jogará utilizado o símbolo: %s'%(jogador2, colored('O','blue')))
            simbolo_jogador2 = colored('O','blue')
        else:
            print('%s jogará utilizado o símbolo: %s' % (jogador2, colored('X','blue')))
            simbolo_jogador2 = colored('X', 'blue')
        break

jogadores = jogador1, jogador2

while True:

    imprime(tabuleiro_aux)
    limpar_tabuleiro()
    imprime(tabuleiro)

    while True:


        if jogadas <= 9:

            while True:
                pos = input("Escolha, utilizando os números de 1 a 9, em qual posição vai jogar %s: " %jogadores[jogador_da_vez])

                if pos in jogadas_possiveis:
                    pos = int(pos)
                    break
                else:
                    print("\n"*80)
                    imprime(tabuleiro_aux)
                    imprime(tabuleiro)
                    print("***POSICAO INVÁLIDA*** Jogue novamente" )

            jogador_da_vez=jogada(pos,jogador_da_vez)
            imprime(tabuleiro_aux)
            imprime(tabuleiro)

            venceu=vencedor()

            if venceu == 1:
                print("Parabéns %s!!!" %jogadores[0])
                vitorias_um += 1
                break
            elif venceu==2:
                print("parabens %s !!!" %jogadores[1])
                vitorias_dois += 1
                break
            elif jogadas>9:

                break
            else:
             jogadas+=1
        else:
            print("Partida empatada,nenhum vencendor!")
            empates+=1
            break

    escolha = input("Deseja jogar novamente com os mesmos jogadores S/N? Se deseja parar o game aperte outra tecla! ")

    if escolha.upper() == 'N':

        jogador1 = input("Nome do primeiro jogador:  ")
        jogador2 = input("Nome do segundo jogador:  ")
        jogadores = jogador1, jogador2
        jogadas = 1

    elif escolha.upper() == 'S':

        print('')
        jogadas = 1

    else:
        break

print("\n"*60)

print("Fim de Jogo")
print()
print("empates ",empates)
print("Vidorias de %s = %d"%(jogadores[0],vitorias_um))
print("Vidorias de %s = %d"%(jogadores[1],vitorias_dois))
