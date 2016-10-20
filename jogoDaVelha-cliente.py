from socket import *
from termcolor import colored
from minmax import *



tabuleiro = [['1','2','3'],['4','5','6'],['7','8','9']]
jogadas = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
transposta = [['1','2','3'],['4','5','6'],['7','8','9']]
diagonal0 = [] 
diagonal1 = []
acabou = 0

    
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
    print('')
 
def gameWin(simbolo,tabuleiro):
    diagonal0 = [tabuleiro[0][0],tabuleiro[1][1], tabuleiro[2][2]] 
    diagonal1 = [tabuleiro[2][0], tabuleiro[1][1], tabuleiro[0][2]]
    for r in tabuleiro:
        if r == [simbolo] * 3:
            return True
        elif diagonal0 == [simbolo]*3 or diagonal1 == [simbolo] * 3:
            return True
    else: return False
                
        
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
    #print('Esperando a resposta de %s' % down_nome)
    resposta_adversario = tcp.recv(1024)
    resposta_adversario = str(resposta_adversario, 'utf-8')
    resposta = bytes(resposta, 'utf-8')
    tcp.send(resposta)
    if resposta_adversario.upper() == 'S':
        return True
    return False


while True:

    print('1 - Jogo Online')
    print('2 - Jogo contra o PC')
    try:
        modo_jogo = int(input('Conforme acima, informe 1 ou 2, e escolha o modo para jogar: '))

        if modo_jogo not in [1,2]:
            continue
        print('')
        break
    except:
          print('Opção inválida!')


while modo_jogo == 1:
    host = "192.168.0.107"
    port = 3000
    tcp = socket(AF_INET, SOCK_STREAM)
    dest = (host, port)
    tcp.connect(dest)
    while True:
        nome = input('digite seu nome: ')
        simbolo = input('%s digite o simbolo: ' %nome)
        simbolo = simbolo.upper()

        envia_nome = bytes(nome, 'utf-8')
        tcp.send(envia_nome)

        print('Esperando o nome do adversário... Aguarde...')
        down_nome = tcp.recv(1024)
        down_nome = str(down_nome, 'utf-8')

        simb = bytes(simbolo, 'utf-8')
        tcp.send(simb)

        print('Esperando o símbolo do adversário... Aguarde...')
        down_simb = tcp.recv(1024)
        down_simb = str(down_simb, 'utf-8')
        break
    cont = 0
    while True:
        if cont % 2 == 0:
            imprime(tabuleiro)
            print('Esperando a jogada de %s...' %down_nome)
            recb_posicao = tcp.recv(1024)
            recb_posicao = str(recb_posicao, 'utf-8')
            recb_posicao = int(recb_posicao)
            posicao_lista = jogadas[recb_posicao]
            jogada(posicao_lista, tabuleiro, down_simb)
            imprime (tabuleiro)
            transposta_matriz(tabuleiro, transposta)
            if gameWin(down_simb, tabuleiro) == True or gameWin(down_simb, transposta) == True:
                print ('%s ganhou!' %down_nome)
                resposta = input('Deseja continuar jogando("s" ou "n")? ')
                print('Esperando a resposta de %s'%down_nome)
                if resposta.upper() != 'S':
                    tcp.close()
                    print('O jogo acabou!')
                    acabou = 1
                    break


                if gameOver(resposta) == True:
                    cont = 0
                    tabuleiro = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
                    transposta = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
                    imprime(tabuleiro)
                else:
                    print('%s parou de jogar.'%down_nome)
                    tcp.close()
                    acabou = 1
                    break

        else:

            while True:

                try:

                    posicao = int(input('Digite a posição(1 a 9) da jogada: ')) - 1
                    if posicao < 0 or posicao > 8:
                       print('Posição inexistente. Informe um número de 1 a 9.')
                       continue
                except:
                    print('Posição inexistente. Informe um número de 1 a 9.')
                    continue

                posicao_lista = jogadas[posicao]
                if jogada(posicao_lista, tabuleiro, simbolo) == False:
                    print('Jogada Inválida! Posição já selecionada!')
                    continue
                break

            transposta_matriz(tabuleiro, transposta)
            posicao_lista = jogadas[posicao]
            posicao = bytes(str(posicao), 'utf-8')
            tcp.send(posicao)

            if gameWin(simbolo, tabuleiro) == True or gameWin(simbolo, transposta) == True:
                imprime(tabuleiro)
                print('%s ganhou!' %nome)
                resposta = input('Deseja continuar jogando ("s" ou "n")?')

                if resposta.upper() != 'S':
                    tcp.close()
                    print('O jogo acabou!')
                    acabou = 1
                    break

                if gameOver(resposta) == True:
                    imprime(tabuleiro)
                    cont = 0
                    tabuleiro = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
                    transposta = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]

                else:
                    print('%s parou de jogar.' % down_nome)
                    tcp.close()
                    acabou = 1
                    break
        cont += 1
    if acabou == 1:
        break

while modo_jogo == 2:

    GUI().mainloop()
    while True:
        print('1 - Jogo Online')
        print('2 - Jogo contra o PC')
        try:
            modo_jogo = int(input('Conforme acima, informe 1 ou 2, e escolha o modo para jogar: '))

            if modo_jogo == '1' or modo_jogo == '2':
                continue
            break
        except:
            print('Opção inválida!')

                
            
        
            
    
