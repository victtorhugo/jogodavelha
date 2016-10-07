
tabuleiro=['','1','2','3',
           '4','5', '6', '7',
           '8','9', '2', ' ',]

jogadas_possiveis=['1','2','3','4','5','6','7','8','9']

jogadas=1
jogador_da_vez=0

vitorias_um=0
vitorias_dois=0
empates=0

jogadores=[]

def imprime():
    print("")
    print("\t\t      |     |     ")
    print("\t\t   %s  |  %s  |  %s "%(tabuleiro[7],tabuleiro[8],tabuleiro[9]))
    print("\t\t _____|_____|_____")
    print("\t\t      |     |     ")
    print("\t\t   %s  |  %s  |  %s "%(tabuleiro[4],tabuleiro[5],tabuleiro[6]))
    print("\t\t _____|_____|_____")
    print("\t\t      |     |     ")
    print("\t\t   %s  |  %s  |  %s "%(tabuleiro[1],tabuleiro[2],tabuleiro[3]))
    print("\t\t      |     |     ")
    print("")

def limpar_tabuleiro():
    for l in range(11):
        tabuleiro[l]=" "

def jogada(pos,jogador_da_vez):
    while True:
        if  tabuleiro[pos]==' ':
            print(jogador_da_vez)
            if jogador_da_vez==0:
                tabuleiro[pos] ='X'
                return 1
            elif jogador_da_vez==1:
                tabuleiro[pos] ="O"
                return 0
            break
        else:
            print("\n" * 80)
            imprime()
            pos=int(input("ops posicao ocupada, tente novamente:  \n"))
    print("\n" * 60)

def vencedor():
    i=1
    v=1
    while i<=7:
        if tabuleiro[i] ==tabuleiro[i+1] and tabuleiro[i+1] ==tabuleiro[i+2]and tabuleiro[i+2]=="X":#ganhou na orizontal
            return 1
            i = 1
            break

        elif tabuleiro[i] ==tabuleiro[i+1] and tabuleiro[i+1] ==tabuleiro[i+2]and tabuleiro[i+2] =="O":#ganhou na orizontal
            i = 1
            return 2
            break
        aux=v+3
        if tabuleiro[v] == tabuleiro[v+3] and tabuleiro[v] == tabuleiro[aux+3] and  tabuleiro[aux+3] == "X":
            i = 1
            return 1

            break
        elif tabuleiro[v] == tabuleiro[v+3] and tabuleiro[v] == tabuleiro[aux+3] and  tabuleiro[aux+3]  == "O":
            i = 1
            return 2
            break
        #diagonal 1
        if tabuleiro[7] == tabuleiro[5] and tabuleiro[5] == tabuleiro[3] and tabuleiro[3] == "X":

            i = 1
            return 1
            break
        elif tabuleiro[7] == tabuleiro[5] and tabuleiro[5] == tabuleiro[3] and tabuleiro[3] == "O":
            i = 1
            return 2
            break
        #diagonal 2
        if tabuleiro[9] == tabuleiro[5] and tabuleiro[5] == tabuleiro[1] and tabuleiro[1] == "X":
            i = 1
            return 1
            break
        elif tabuleiro[9] == tabuleiro[5] and tabuleiro[5] == tabuleiro[1] and tabuleiro[1] ==  "O":
            i = 1

            return 2
            break

        i+=3
        v+=1

jodaor1=''
jogador2=''
jogador1 = input("Nome do primeiro jogador: \n ")
jogador2 = input("Nome do segundo jogador:  \n")
jogadores = jogador1, jogador2

while True:

    imprime()
    limpar_tabuleiro()
    imprime()

    while True:


        if jogadas<=9:

            while True:
                pos=input(" Uma jogada %s: "%jogadores[jogador_da_vez])

                if pos in jogadas_possiveis:
                    pos=int(pos)
                    break
                else:
                    print("\n"*80)
                    imprime()
                    print("***POSICAO INVALIDA*** Jogue novamente" )


            jogador_da_vez=jogada(pos,jogador_da_vez)
            imprime()
            venceu=vencedor()
            if venceu==1:
                print("parabens %s"%jogadores[0])
                vitorias_um+=1
                break
            elif venceu==2:
                print("parabens %s" % jogadores[1])
                vitorias_dois += 1
                break
            elif jogadas>9:

                break
            else:
             jogadas+=1
        else:
            print("Partida empatada,nenhum vencendor")
            empates+=1
            break

    escolha=input("Deseja jogar novamente com os mesmos jogadores S/N, se deseja sair aperte outra tecla")
    if escolha.upper()=='N':
        jogador1 = input("Nome do primeiro jogador:  ")
        jogador2 = input("Nome do segundo jogador:  ")
        jogadores = jogador1, jogador2
        jogadas=1
    elif escolha.upper()=='S':
        print("")

        jogadas = 1
    else:
        break

print("\n"*60)

print("Fim de Jogo")
print()
print("empates ",empates)
print("Vidorias de %s = %d"%(jogadores[0],vitorias_um))
print("Vidorias de %s = %d"%(jogadores[1],vitorias_dois))
