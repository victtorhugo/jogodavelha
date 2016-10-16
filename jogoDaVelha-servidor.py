from socket import *
from termcolor import colored
host = 'localhost'
port = 5000
tcp = socket(AF_INET, SOCK_STREAM)
dest = (host, port)
tcp.bind(dest)
tcp.listen(1)
tabuleiro = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' '],]
jogadas = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
transposta = [['','',''],['','','',],['','','']]
diagonal0 = [] 
diagonal1 = []

def imprime(tabuleiro):
    '''Interface'''

    print('')
    print('\t\t      |     |     ')
    print('\t\t   %s  |  %s  |  %s '%(tabuleiro[2][0],tabuleiro[2][1],tabuleiro[2][2]))
    print('\t\t _____|_____|_____')
    print('\t\t      |     |     ')
    print('\t\t   %s  |  %s  |  %s '%(tabuleiro[1][0],tabuleiro[1][1],tabuleiro[1][2]))
    print('\t\t _____|_____|_____')
    print('\t\t      |     |     ')
    print('\t\t   %s  |  %s  |  %s '%(tabuleiro[0][0],tabuleiro[0][1],tabuleiro[0][2]))
    print('\t\t      |     |     ')

def gameWin(simbolo, tabuleiro):
    diagonal0 = [tabuleiro[0][0], tabuleiro[1][1], tabuleiro[2][2]]
    diagonal1 = [tabuleiro[2][0], tabuleiro[1][1], tabuleiro[0][2]]
    for r in tabuleiro:
        if r == [simbolo] * 3:
            return True
        elif diagonal0 == [simbolo] * 3 or diagonal1 == [simbolo] * 3:
            return True
    else:
        return False
        
def transposta_matriz(tabuleiro, transposta):
    for a in range(3):
        for b in range(3):
            transposta[a][b] = tabuleiro[b][a]
              
def jogada(posicao_lista, tabuleiro, simbolo):
    tabuleiro[posicao_lista[0]][posicao_lista[1]] = simbolo
    
def gameOver(resposta):
    resposta = bytes(resposta, 'utf-8')
    conecxao.send(resposta)
    resposta_adversario = conecxao.recv(1024)
    print(resposta_adversario)
    resposta_adversario = str(resposta_adversario, 'utf-8')
    if resposta_adversario == 's':
        return True
    else: return False
cont = 0
while True:
    conecxao, cliente = tcp.accept()
    while True:
        down_simb = conecxao.recv(1024)
        nome = input('digite seu nome: ')
        simbolo = input('%s digite o simbolo: ' % nome)
        down_simb = str(down_simb, 'utf-8')
        while True:
            if down_simb ==simbolo:
                print('simbolos iguas')
                simbolo = input('%s digite o simbolo: ' % nome)
                print('simbolos iguas')
                continue
            else:
                break
            break
        simb = bytes(simbolo, 'utf-8')
        conecxao.send(simb)
        while True:
            if cont % 2==0:
                imprime(tabuleiro)
                posicao = int(input('digite o numero: ')) -1
                posicao_lista = jogadas[posicao]
                posicao = bytes(str(posicao),'utf-8')
                conecxao.send(posicao)
                jogada(posicao_lista,tabuleiro,simbolo)
                imprime(tabuleiro)
                transposta_matriz(tabuleiro, transposta)
                if gameWin(simbolo, tabuleiro)== True or gameWin(simbolo, transposta) == True:
                    print('ganhou')
                    resposta = input('deseja continuar "s" ou "n": ')
                    if gameOver(resposta)== True:
                        tabuleiro = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' '], ]
                        transposta = [['', '', ''], ['', '', '', ], ['', '', '']]
                        break
                    else:
                        conecxao.close()
                        break
                    break
            else:
                recb_posicao = conecxao.recv(1024)
                recb_posicao = str(recb_posicao, 'utf-8')
                recb_posicao = int(recb_posicao)
                posicao_lista = jogadas[recb_posicao]
                jogada(posicao_lista,tabuleiro,down_simb)
                imprime(tabuleiro)
                transposta_matriz(tabuleiro, transposta)
                if gameWin(down_simb, tabuleiro)== True or gameWin(down_simb, transposta) == True:
                    print('o outro ganhou')
                    resposta = input('deseja contiuar "s" ou "n": ')
                    if gameOver(resposta)== True:
                        tabuleiro = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' '], ]
                        transposta = [['', '', ''], ['', '', '', ], ['', '', '']]
                        break
                    else:
                        conecxao.close()
                        break
                    break
            cont +=1