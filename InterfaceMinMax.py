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