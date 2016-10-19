from socket import *


host = 'localhost'
port = 5000
tcp = socket(AF_INET, SOCK_STREAM)
dest = (host, port)
tcp.connect(dest)
tabuleiro = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
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
    tabuleiro[posicao_lista[0]][posicao_lista[1]] = simbolo
    
def gameOver(resposta):
    resposta_adversario = tcp.recv(1024)
    resposta_adversario = str(resposta_adversario, 'utf-8')
    print(resposta_adversario)
    resposta = bytes(resposta, 'utf-8')
    tcp.send(resposta)
    if resposta_adversario == 's':
        return True
    else: return False


#################Interface MinMax##############################
class GUI:
    def __init__(self):
        self.app = Tk()
        self.app.title('Jogo da Velha - MinMax')
        self.app.resizable(width=False, height=False)
        self.board = Board()
        self.font = Font(family="Helvetica", size=32)
        self.buttons = {}
        for x, y in self.board.fields:
            handler = lambda x=x, y=y: self.move(x, y)
            button = Button(self.app, command=handler, font=self.font, width=2, height=1)
            button.grid(row=y, column=x)
            self.buttons[x, y] = button
        handler = lambda: self.reset()
        button = Button(self.app, text='reset', command=handler)
        button.grid(row=self.board.size + 1, column=0, columnspan=self.board.size, sticky="WE")
        self.update()

    def reset(self):
        self.board = Board()
        self.update()

    def move(self, x, y):
        self.app.config(cursor="watch")
        self.app.update()
        self.board = self.board.move(x, y)
        self.update()
        move = self.board.best()
        if move:
            self.board = self.board.move(*move)
            self.update()
        self.app.config(cursor="")

    def update(self):
        for (x, y) in self.board.fields:
            text = self.board.fields[x, y]
            self.buttons[x, y]['text'] = text
            self.buttons[x, y]['disabledforeground'] = 'black'
            if text == self.board.empty:
                self.buttons[x, y]['state'] = 'normal'
            else:
                self.buttons[x, y]['state'] = 'disabled'
        winning = self.board.won()
        if winning:
            for x, y in winning:
                self.buttons[x, y]['disabledforeground'] = 'red'
            for x, y in self.buttons:
                self.buttons[x, y]['state'] = 'disabled'
        for (x, y) in self.board.fields:
            self.buttons[x, y].update()

    def mainloop(self):
        self.app.mainloop()

print('1 - Jogo Online')
print('2 - Jogo contra o PC')

modo_jogo = input('Conforme acima, informe 1 ou 2, e escolha o modo para jogar: ')

print('')
print('Obs.: Caso tenha escolhido contra o PC, mas queira mudar o modo do jogo, '
      'feche a janela e a opção para mudar o modo irar aparecer!')

while modo_jogo == 1:

    while True:
        nome = input('digite seu nome: ')
        simbolo = input('%s digite o simbolo: ' % nome)
        simb = bytes(simbolo, 'utf-8')
        tcp.send(simb)
        down_simb = tcp.recv(1024)
        down_simb = str(down_simb, 'utf-8')
        break
    cont = 0
    while True:
        if cont % 2 == 0:
            recb_posicao = tcp.recv(1024)
            recb_posicao = str(recb_posicao, 'utf-8')
            recb_posicao = int(recb_posicao)
            posicao_lista = jogadas[recb_posicao]
            jogada(posicao_lista, tabuleiro, down_simb)
            imprime (tabuleiro)
            transposta_matriz(tabuleiro, transposta)
            if gameWin(down_simb, tabuleiro) == True or gameWin(down_simb, transposta) == True:
                print ('o outro ganhou')
                resposta = input('deseja contiuar "s" ou "n": ')
                if gameOver(resposta) == True:
                    tabuleiro = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' '], ]
                    transposta = [['', '', ''], ['', '', '', ], ['', '', '']]
                    break
                else:
                    print('gameover')
                    tcp.close()
                    break
                break
        else:
            posicao = int(input('digite o numero: ')) -1
            posicao_lista = jogadas[posicao]

            posicao = bytes(str(posicao), 'utf-8')
            tcp.send(posicao)
            jogada(posicao_lista, tabuleiro, simbolo)
            imprime(tabuleiro)
            transposta_matriz(tabuleiro, transposta)
            if gameWin(simbolo, tabuleiro) == True or gameWin(simbolo, transposta) == True:
                print("ganhou")
                resposta = input('deseja continuar "s" ou "n": ')
                if gameOver(resposta) == True:
                    tabuleiro = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' '], ]
                    transposta = [['', '', ''], ['', '', '', ], ['', '', '']]
                    break
                else:
                    print('gameover')
                    tcp.close()
                    break
        cont +=1

while modo_jogo == 2:

    GUI().mainloop()
    print('')
    print('1 - Jogo Online')
    print('2 - Jogo contra o PC')
    print('')
    modo_jogo = input('Conforme acima, informe 1 ou 2, e escolha o modo para jogar: ')

                
            
        
            
    
