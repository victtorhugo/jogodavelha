from socket import *
from termcolor import colored
from minmax import *

host = 'localhost'
port = 5000
tcp = socket(AF_INET, SOCK_STREAM)
dest = (host, port)
tcp.bind(dest)
tcp.listen(1)
tabuleiro = [['1','2','3'],['4','5','6'],['7','8','9']]
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
    if tabuleiro[posicao_lista[0]][posicao_lista[1]] in ['1','2','3','4','5','6','7','8','9']:
        tabuleiro[posicao_lista[0]][posicao_lista[1]] = simbolo
        return True
    return False
    
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

print('1 - Jogo Online')
print('2 - Jogo contra o PC')

modo_jogo = int(input('Conforme acima, informe 1 ou 2, e escolha o modo para jogar: '))

print('')
print('Obs.: Caso tenha escolhido contra o PC, mas queira mudar o modo do jogo, '
      'feche a janela e a opção para mudar o modo irar aparecer!')

while modo_jogo == 1:

    while True:
        conecxao, cliente = tcp.accept()
        nome = input('digite seu nome: ')
        simbolo = input('%s digite o simbolo: ' % nome)

        print('Esperando o nome do adversário... Aguarde...')
        down_nome = conecxao.recv(1024)
        down_nome = str(down_nome, 'utf-8')

        envia_nome = bytes(envia_nome, 'utf-8')
        tcp.send(envia_nome)

        print('Esperando o símbolo do adversário... Aguarde...')
        down_simb = conecxao.recv(1024)
        down_simb = str(down_simb, 'utf-8')

        while True:
            if down_simb == simbolo:
                print('Os símbolos iguais. Escolha outro símbolo.')
                simbolo = input('%s digite o simbolo: ' %nome)
                continue
            else:
                break

        simb = bytes(simbolo, 'utf-8')
        conecxao.send(simb)
        while True:
            if cont % 2 == 0:

                while True:
                    posicao = int(input('Digite a posição(1 a 9) da jogada: ')) - 1
                    if jogada(posicao_lista, tabuleiro, simbolo) == False:
                        continue
                    break

                imprime(tabuleiro)
                posicao_lista = jogadas[posicao]
                posicao = bytes(str(posicao),'utf-8')
                conecxao.send(posicao)
                transposta_matriz(tabuleiro, transposta)

                if gameWin(simbolo, tabuleiro)== True or gameWin(simbolo, transposta) == True:
                    print('%s ganhou' %nome)
                    resposta = input('Deseja continuar "s" ou "n": ')
                    if gameOver(resposta) == True:
                        tabuleiro = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
                        transposta = [['', '', ''], ['', '', '', ], ['', '', '']]
                        break
                    else:
                        conecxao.close()
                        break
                    break
            else:
                print('Esperando a jogada de %s...' %down_nome)
                recb_posicao = conecxao.recv(1024)
                recb_posicao = str(recb_posicao, 'utf-8')
                recb_posicao = int(recb_posicao)
                posicao_lista = jogadas[recb_posicao]
                jogada(posicao_lista,tabuleiro,down_simb)
                imprime(tabuleiro)
                transposta_matriz(tabuleiro, transposta)
                if gameWin(down_simb, tabuleiro)== True or gameWin(down_simb, transposta) == True:
                    print('%s ganhou' %down_nome)
                    resposta = input('Deseja continuar "s" ou "n": ')
                    if gameOver(resposta)== True:
                        tabuleiro = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
                        transposta = [['', '', ''], ['', '', '', ], ['', '', '']]
                        break
                    else:
                        conecxao.close()
                        break
            cont +=1

while modo_jogo == 2:

    GUI().mainloop()
    print('')
    print('1 - Jogo Online')
    print('2 - Jogo contra o PC')
    print('')
    modo_jogo = int(input('Conforme acima, informe 1 ou 2, e escolha o modo para jogar: '))