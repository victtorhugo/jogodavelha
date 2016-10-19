from minmax import *
escolha  = ''
while escolha != 4:
    print('MENU DE JOGO\n OPÇÔES DE JOGO\n 1 --> single mode\n 2 --> Multiplayer Mode (Online)\n 3 --> Multiplayer Mode (locally)\n 4 --> sair')
    while True:
        try:
            escolha  = int(input())
            break
        except:
            print('invalido')
            continue
    if escolha == 1:
        """vai chamar a parada do minmax"""
    elif escolha == 2:
        """vai chamar o jogo online"""
    elif escolha == 3:
        """vai chamar o jogo para ser jogado em uma maquina"""
        
